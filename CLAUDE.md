# quick-imposing-pub

quick-imposing(카드 PDF를 인쇄용 판 PDF에 배치하는 Windows 프로그램)의 GitHub Pages 사이트다.
빌드 단계 없는 순수 HTML/CSS/JS이고, 공개되는 파일은 `site/` 아래에만 둔다.
main에 push되면 CI가 검사를 통과한 `site/`를 Pages에 배포한다.

## 세션 (권장)
- 시작하면 `.claude/notes.md`를 먼저 읽는다. 저장소 전체 탐색은 필요할 때만 한다.
- 작업이 일단락되면 `.claude/notes.md`를 짧게 갱신한다 (20줄 이하, 덮어쓰기).

## 검사
- 검사는 `python scripts/check.py <경로>...`만 쓴다. 바뀐 경로만 넘긴다. 전체 검사는 CI가 한다.
- 테스트 러너(unittest, pytest)를 직접 실행하지 않는다. 훅이 막는다.
- 검사 내용: HTML 구조, lang/title/charset/viewport, img alt, 내부 링크·자원 경로, 같은 페이지 앵커, 중복 id, 그리고 `tests/`의 unittest.
- 사이트 안 링크는 상대경로로 쓴다. "/"로 시작하는 경로는 프로젝트 Pages에서 깨지므로 검사가 실패시킨다.

## CI
- CI 결과는 GitHub MCP 도구(`actions_list`, `get_job_logs`)로 확인하고, 실패한 단계의 출력만 본다.
- push한 뒤 결과를 확인한다. 진행 중이면 잠시 기다렸다가 최대 3번까지만 다시 확인하고, 그래도 끝나지 않으면 사용자에게 넘긴다.

## 브랜치와 PR
- 기본 브랜치(main)에 직접 push하지 않는다. 작업 브랜치에서 하고 PR로 합친다. 훅이 막는다.
- PR 병합은 사용자가 대화에서 해당 PR을 명시적으로 승인했을 때만 한다. 리뷰 승인, CI 통과, 다른 PR에 대한 이전 승인은 허가가 아니다.

## 지킬 것
- 권한으로 막힌 파일(이미지·글꼴·PDF 등 바이너리 자원, 캐시)을 우회해서 읽지 않는다.
- 포맷 도구는 쓰지 않는다. 기존 파일의 들여쓰기·스타일을 따른다.
