import importlib.util
import tempfile
import unittest
from pathlib import Path

_spec = importlib.util.spec_from_file_location(
    "check", Path(__file__).resolve().parent.parent / "scripts" / "check.py")
check = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(check)

GOOD = """<!doctype html>
<html lang="ko">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width">
<title>t</title><link rel="stylesheet" href="style.css"></head>
<body><p id="a">x<p><a href="#a">a</a> <a href="https://example.com">e</a>
<img src="style.css" alt=""></body></html>
"""


class CheckHtmlTest(unittest.TestCase):
    def _run(self, html):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "style.css").write_text("")
            page = root / "index.html"
            page.write_text(html, encoding="utf-8")
            return [msg for _, _, msg in check.check_html(page, root)]

    def test_good_page_has_no_problems(self):
        self.assertEqual(self._run(GOOD), [])

    def test_missing_lang_and_alt(self):
        msgs = self._run(GOOD.replace(' lang="ko"', "").replace(' alt=""', ""))
        self.assertTrue(any("lang" in m for m in msgs))
        self.assertTrue(any("alt" in m for m in msgs))

    def test_broken_links(self):
        msgs = self._run(GOOD.replace('href="#a"', 'href="#nope"')
                         .replace('href="style.css"', 'href="/style.css"')
                         .replace('src="style.css"', 'src="missing.png"'))
        self.assertTrue(any("#nope" in m for m in msgs))
        self.assertTrue(any("루트 절대경로" in m for m in msgs))
        self.assertTrue(any("missing.png" in m for m in msgs))

    def test_unclosed_tag(self):
        msgs = self._run(GOOD.replace("<body>", "<body><div>"))
        self.assertTrue(any("<div>" in m for m in msgs))


if __name__ == "__main__":
    unittest.main()
