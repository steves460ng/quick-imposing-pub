#!/usr/bin/env python3
"""조용한 검사 명령. 성공하면 한 줄, 실패하면 문제만 출력한다.

    python scripts/check.py            전체 검사 (site/의 HTML 전부 + tests/ 전부)
    python scripts/check.py <경로>...  그 경로와 관련된 것만 검사
    python scripts/check.py --ci       CI용 (지금은 전체 검사와 같다)

HTML 검사 항목
- <html lang>, <title>, <meta charset>, <meta name="viewport">
- 닫히지 않았거나 짝이 맞지 않는 태그, 중복 id
- <img>의 alt 속성
- 내부 링크·자원 경로가 실제로 있는지, 같은 페이지 #앵커가 있는지
- "/"로 시작하는 루트 절대경로 (GitHub Pages 프로젝트 사이트에서는 깨진다)
"""
import io
import sys
import traceback
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
TESTS = ROOT / "tests"
MAX_SHOWN = 20

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
        "meta", "source", "track", "wbr"}
# 끝 태그를 생략할 수 있는 요소. 짝 검사에서 너그럽게 본다.
OPTIONAL_END = {"p", "li", "dt", "dd", "tr", "td", "th", "thead", "tbody",
                "tfoot", "option", "optgroup", "colgroup", "caption", "rt", "rp"}
LINK_ATTRS = {("a", "href"), ("link", "href"), ("script", "src"), ("img", "src"),
              ("source", "src"), ("video", "src"), ("audio", "src"),
              ("iframe", "src"), ("video", "poster")}


class _Collector(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.problems = []  # (line, msg)
        self.stack = []  # (tag, line)
        self.ids = {}
        self.links = []  # (line, url)
        self.lang = None
        self.title = None
        self.in_title = False
        self.charset = False
        self.viewport = False

    def _line(self):
        return self.getpos()[0]

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        line = self._line()
        if tag == "html":
            self.lang = a.get("lang")
        elif tag == "title":
            self.in_title = True
            self.title = ""
        elif tag == "meta":
            if "charset" in a:
                self.charset = True
            if (a.get("name") or "").lower() == "viewport":
                self.viewport = True
        elif tag == "img" and "alt" not in a:
            self.problems.append((line, "<img>에 alt 속성이 없음"))
        if a.get("id"):
            if a["id"] in self.ids:
                self.problems.append((line, f"중복 id: {a['id']} (처음 {self.ids[a['id']]}행)"))
            else:
                self.ids[a["id"]] = line
        for t, attr in LINK_ATTRS:
            if tag == t and a.get(attr):
                self.links.append((line, a[attr]))
        if tag not in VOID:
            self.stack.append((tag, line))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID and self.stack and self.stack[-1][0] == tag:
            self.stack.pop()

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        if tag in VOID:
            return
        names = [t for t, _ in self.stack]
        if tag not in names:
            self.problems.append((self._line(), f"여는 태그 없는 </{tag}>"))
            return
        while self.stack:
            t, line = self.stack.pop()
            if t == tag:
                break
            if t not in OPTIONAL_END:
                self.problems.append((line, f"<{t}>가 닫히지 않음"))

    def handle_data(self, data):
        if self.in_title:
            self.title += data


def check_html(path, site_root=SITE):
    """HTML 파일 하나를 검사해 [(경로, 행, 메시지)]를 돌려준다."""
    path = Path(path)
    text = path.read_text(encoding="utf-8")
    p = _Collector()
    p.feed(text)
    p.close()
    out = [(path, line, msg) for line, msg in p.problems]
    for t, line in p.stack:
        if t not in OPTIONAL_END and t not in {"html", "body", "head"}:
            out.append((path, line, f"<{t}>가 닫히지 않음"))
    if not p.lang:
        out.append((path, 1, "<html>에 lang 속성이 없음"))
    if not (p.title or "").strip():
        out.append((path, 1, "<title>이 없거나 비어 있음"))
    if not p.charset:
        out.append((path, 1, '<meta charset>이 없음'))
    if not p.viewport:
        out.append((path, 1, '<meta name="viewport">가 없음'))
    for line, url in p.links:
        msg = _check_link(path, url, p.ids, Path(site_root))
        if msg:
            out.append((path, line, msg))
    return out


def _check_link(page, url, ids, site_root):
    parts = urlsplit(url)
    if parts.scheme or parts.netloc or url.startswith("//"):
        return None  # 외부 링크, mailto:, data: 등
    if url.startswith("/"):
        return f"루트 절대경로는 Pages에서 깨짐, 상대경로로: {url}"
    target_path = unquote(parts.path)
    if not target_path:
        if parts.fragment and parts.fragment not in ids:
            return f"페이지 안에 없는 앵커: #{parts.fragment}"
        return None
    target = (page.parent / target_path).resolve()
    if target.is_dir():
        target = target / "index.html"
    if not target.exists():
        return f"없는 파일: {url}"
    try:
        target.relative_to(site_root.resolve())
    except ValueError:
        return f"site/ 밖을 가리킴: {url}"
    return None


class _Result(unittest.TestResult):
    def __init__(self):
        super().__init__()
        self.items = []

    def _add(self, test, err):
        tb = traceback.extract_tb(err[2])
        frame = next((f for f in reversed(tb) if Path(f.filename).is_relative_to(ROOT)), tb[-1])
        last = "".join(traceback.format_exception_only(err[0], err[1])).strip().splitlines()[0]
        rel = Path(frame.filename).resolve().relative_to(ROOT) if Path(frame.filename).is_relative_to(ROOT) else frame.filename
        self.items.append((rel, frame.lineno, f"{test.id()}: {last}"))

    def addFailure(self, test, err):
        self._add(test, err)

    def addError(self, test, err):
        self._add(test, err)


def run_tests(files):
    """테스트 파일 목록을 실행해 (실행 수, [(경로, 행, 메시지)])를 돌려준다."""
    sys.path.insert(0, str(TESTS))
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    for f in files:
        suite.addTests(loader.loadTestsFromName(Path(f).stem))
    result = _Result()
    out, err = sys.stdout, sys.stderr
    sys.stdout = sys.stderr = io.StringIO()  # 테스트가 찍는 출력은 숨긴다
    try:
        suite.run(result)
    finally:
        sys.stdout, sys.stderr = out, err
    return result.testsRun, result.items


def select(args):
    """인자 경로를 (HTML 파일, 테스트 파일)로 나눈다. 인자가 없으면 전체."""
    all_html = sorted(SITE.rglob("*.html"))
    all_tests = sorted(TESTS.glob("test_*.py"))
    if not args:
        return all_html, all_tests
    html, tests = set(), set()
    for a in args:
        p = (Path.cwd() / a).resolve()
        if p.is_dir():
            html |= {h for h in all_html if h.is_relative_to(p)}
            tests |= {t for t in all_tests if t.is_relative_to(p)}
            if p == ROOT / "scripts" or p.is_relative_to(ROOT / "scripts"):
                tests |= set(all_tests)
        elif p.suffix == ".html":
            html.add(p)
        elif p in all_tests:
            tests.add(p)
        elif p.is_relative_to(ROOT / "scripts"):
            t = TESTS / f"test_{p.stem}.py"
            tests |= {t} if t.exists() else set(all_tests)
    return sorted(html), sorted(tests)


def main(argv):
    args = [a for a in argv if a != "--ci"]
    html, tests = select(args)
    problems = []
    for h in html:
        if not h.exists():
            problems.append((h, 0, "파일 없음"))
            continue
        problems += check_html(h)
    ran = 0
    if tests:
        ran, items = run_tests(tests)
        problems += items
    if not problems:
        print(f"OK: HTML {len(html)}개, 테스트 {ran}개")
        return 0
    for path, line, msg in problems[:MAX_SHOWN]:
        rel = path.relative_to(ROOT) if isinstance(path, Path) and path.is_relative_to(ROOT) else path
        print(f"{rel}:{line}: {msg}")
    if len(problems) > MAX_SHOWN:
        print(f"... 외 {len(problems) - MAX_SHOWN}개")
    print(f"FAIL: 문제 {len(problems)}개")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
