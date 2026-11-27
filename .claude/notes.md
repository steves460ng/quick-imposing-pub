# 작업 노트 (20줄 이하, 매번 덮어쓴다)
## 현재 상태
- 디자인 시안(인쇄판 콘셉트)을 반영: site/index.html(홈), site/guide.html(사용법), style.css.
- 패치 소식은 Releases가 비어 있어 "아직 공개된 버전이 없습니다"로 둠.
- 스크린샷은 넣지 않음(원본 저장소 파일을 옮기지 않는 규칙). 공개용 캡처를 받으면 홈 "화면 보기"와 사용법에 추가.
## 다음 할 일 (사용자)
- Settings > Pages > Source를 "GitHub Actions"로, Discussions 켜기
- 첫 빌드 파일을 Releases에 올리기
## 다음 할 일 (Claude)
- 첫 Release가 올라오면 홈 패치 소식 채우기
- 공개용 스크린샷을 받으면 site/images/에 넣기
## 주의할 점
- 사이트 안 링크는 상대경로로 쓴다. 프로젝트 Pages 주소가 /quick-imposing-pub/ 아래라서 "/..."는 깨진다.
- 구현 관련 기술 내용은 쓰지 않는다. 배포 파일은 커밋하지 않는다(Releases로).
