# 작업 노트 (20줄 이하, 매번 덮어쓴다)
## 현재 상태
- groundwork 초기 세팅 완료. site/에는 자리표시 index.html(소개·내려받기·의견 링크)과 style.css만 있다.
- 이슈 양식(버그 제보·개선 요구)과 Discussions 안내를 만들었다.
## 다음 할 일 (사용자)
- Settings > Pages > Source를 "GitHub Actions"로
- Settings > General > Features에서 Discussions 켜기
- 첫 빌드 파일을 Releases에 올리기
## 다음 할 일 (Claude)
- 사이트 내용(소개 · 사용법 · 패치 소식) 기획
## 주의할 점
- 사이트 안 링크는 상대경로로 쓴다. 프로젝트 Pages 주소가 /quick-imposing-pub/ 아래라서 "/..."는 깨진다.
- 구현 관련 기술 내용은 쓰지 않는다. 배포 파일은 커밋하지 않는다(Releases로).
