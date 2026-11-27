# quick-imposing-pub

quick-imposing의 GitHub Pages 사이트입니다.

## 구조

| 경로 | 내용 |
|---|---|
| `site/` | 공개되는 사이트 파일 (순수 HTML/CSS/JS, 빌드 없음) |
| `scripts/check.py` | 검사 명령 (Python 표준 라이브러리만 사용) |
| `tests/` | 검사 스크립트 테스트 (unittest) |
| `.github/workflows/ci.yml` | PR·main push 때 검사, main이면 `site/`를 Pages에 배포 |

## 검사

```sh
python scripts/check.py              # 전체
python scripts/check.py site/a.html  # 해당 경로만
```

성공하면 한 줄, 실패하면 `파일:행: 문제`만 출력합니다.

## 로컬 미리보기

```sh
python -m http.server -d site 8000
```

## 배포

저장소 설정 > Pages > Source를 **GitHub Actions**로 한 번 설정하면, main에 합쳐질 때마다 자동 배포됩니다.

## 라이선스

[LICENSE](LICENSE)
