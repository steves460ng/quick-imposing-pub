#!/usr/bin/env python3
"""PreToolUse(Bash) 훅. 막을 명령이면 종료 코드 2와 함께 대신 쓸 방법을 stderr에 한 줄로 알린다.

막는 것
- 테스트 러너(unittest, pytest)를 검사 명령 없이 직접 실행
- cat/head/tail 등으로 읽기 차단 대상(바이너리 자원, 캐시)을 읽기
- git push로 기본 브랜치(main)에 직접 push
"""
import json
import re
import shlex
import subprocess
import sys

DEFAULT_BRANCH = "main"
CHECK = "python scripts/check.py [경로...]"
READERS = {"cat", "head", "tail", "less", "more", "bat", "xxd", "hexdump", "strings", "od"}
BLOCKED_READ = re.compile(
    r"(__pycache__/|\.pyc$|\.(png|jpe?g|gif|webp|ico|pdf|zip|woff2?|ttf|otf|mp4|webm)$)", re.I)


def segments(cmd):
    """&&, ||, ;, | 로 나눈 각 명령을 토큰 목록으로."""
    for part in re.split(r"&&|\|\||[;|\n]", cmd):
        try:
            toks = shlex.split(part)
        except ValueError:
            toks = part.split()
        while toks and re.match(r"^\w+=", toks[0]):  # VAR=값 접두어
            toks = toks[1:]
        if toks:
            yield toks


def current_branch():
    try:
        return subprocess.run(["git", "branch", "--show-current"], capture_output=True,
                              text=True, timeout=5).stdout.strip()
    except Exception:
        return ""


def check(toks):
    prog = toks[0].rsplit("/", 1)[-1]
    if prog in {"pytest", "py.test"}:
        return f"테스트 러너를 직접 실행하지 말고 {CHECK}를 쓰세요."
    if re.match(r"python3?(\.\d+)?$", prog) and len(toks) > 2 and toks[1] == "-m" \
            and toks[2] in {"unittest", "pytest"}:
        return f"테스트 러너를 직접 실행하지 말고 {CHECK}를 쓰세요."
    if prog in READERS and any(BLOCKED_READ.search(t) for t in toks[1:]):
        return "읽기 차단 대상 파일(바이너리 자원·캐시)입니다. 읽지 마세요."
    if prog == "git" and "push" in toks:
        args = [t for t in toks[toks.index("push") + 1:] if not t.startswith("-")]
        if len(args) >= 2:
            targets = [r.split(":")[-1].removeprefix("+").removeprefix("refs/heads/") for r in args[1:]]
        else:
            targets = [current_branch()]
        if DEFAULT_BRANCH in targets:
            return f"{DEFAULT_BRANCH}에 직접 push하지 말고 작업 브랜치에 push한 뒤 PR로 합치세요."
    return None


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    cmd = (data.get("tool_input") or {}).get("command") or ""
    for toks in segments(cmd):
        msg = check(toks)
        if msg:
            print(msg, file=sys.stderr)
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
