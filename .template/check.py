#!/usr/bin/env python3
"""템플릿 저장소 검사. 성공하면 한 줄, 실패하면 문제만 출력한다.

검사 항목
- .claude/skills/*/SKILL.md 의 frontmatter (name, description)
- .template/MANIFEST 에 적힌 경로가 실제로 있는지
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / ".claude" / "skills"
MANIFEST = ROOT / ".template" / "MANIFEST"
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

errors = []


def err(path, line, msg):
    errors.append(f"{path.relative_to(ROOT)}:{line}: {msg}")


def unquote(v):
    v = v.strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        return v[1:-1]
    return v


def check_skill(md):
    lines = md.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        err(md, 1, "frontmatter가 '---'로 시작하지 않음")
        return
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        err(md, 1, "frontmatter 닫는 '---' 없음")
        return

    fields = {}
    for i in range(1, end):
        if ":" in lines[i]:
            key, val = lines[i].split(":", 1)
            fields[key.strip()] = (unquote(val), i + 1)

    name, nline = fields.get("name", ("", 1))
    if not name:
        err(md, 1, "name 없음")
    else:
        if not NAME_RE.match(name):
            err(md, nline, f"name '{name}'이 kebab-case가 아님")
        if len(name) > 64:
            err(md, nline, "name이 64자를 넘음")
        if "claude" in name or "anthropic" in name:
            err(md, nline, "name에 'claude'나 'anthropic'을 쓸 수 없음")
        if name != md.parent.name:
            err(md, nline, f"name '{name}'과 폴더명 '{md.parent.name}'이 다름")

    desc, dline = fields.get("description", ("", 1))
    if not desc:
        err(md, 1, "description 없음")
    else:
        if len(desc) > 1024:
            err(md, dline, f"description이 1024자를 넘음 ({len(desc)}자)")
        if "<" in desc or ">" in desc:
            err(md, dline, "description에 꺾쇠괄호(<, >)를 쓸 수 없음")

    if not any(l.strip() for l in lines[end + 1:]):
        err(md, end + 1, "본문이 비어 있음")


def check_manifest():
    if not MANIFEST.exists():
        errors.append(".template/MANIFEST: 파일 없음")
        return
    for n, raw in enumerate(MANIFEST.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split(None, 1)
        if len(parts) != 2 or parts[0] not in ("delete", "replace"):
            err(MANIFEST, n, f"형식 오류: '{line}'")
            continue
        if not (ROOT / parts[1]).exists():
            err(MANIFEST, n, f"경로 없음: {parts[1]}")


def main():
    skills = sorted(SKILLS.glob("*/SKILL.md"))
    if not skills:
        errors.append(".claude/skills: SKILL.md가 하나도 없음")
    for md in skills:
        check_skill(md)
    check_manifest()

    if errors:
        print(f"FAIL ({len(errors)}건)")
        for e in errors:
            print(f"- {e}")
        return 1
    print(f"OK: 스킬 {len(skills)}개, MANIFEST 검사 통과")
    return 0


if __name__ == "__main__":
    sys.exit(main())
