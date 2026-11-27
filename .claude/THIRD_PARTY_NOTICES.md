# 서드파티 고지

## test-generator

다음 파일은 [a-abdellatif98/test-generator](https://github.com/a-abdellatif98/test-generator) v1.1.0(커밋 `9f11c7ff54d077b6dcf63f793bf3a7b5696845ea`)에서 가져왔다.

| 이 저장소 경로 | 원본 경로 |
|---|---|
| `.claude/skills/auto-test/SKILL.md` | `skills/auto-test/SKILL.md` |
| `.claude/skills/auto-test/references/frameworks.md` | `skills/auto-test/references/frameworks.md` |
| `.claude/commands/generate-tests.md` | `commands/generate-tests.md` |
| `.claude/agents/test-writer.md` | `agents/test-writer.md` |

변경 사항:
- `auto-test/SKILL.md`: description과 활성 조건을 좁혔다. 테스트 없는 새 소스 파일이 생겼을 때와 사용자가 테스트 방법을 물을 때만 한 번 제안한다.
- `generate-tests.md`: 7단계를 추가했다. 쓴 테스트 파일을 프로젝트의 조용한 검사 명령으로 실행해 확인한다. 검사 명령은 groundwork 세팅 때 채운다.
- `test-writer.md`: 직접 테스트를 실행할 수 없고 호출한 쪽이 검사한다는 안내를 6단계에 추가했다.
- groundwork 세팅 때 인터뷰 답에 따라 일부 또는 전부를 삭제할 수 있다.
- 원본의 PostToolUse 훅(`hooks/hooks.json`)은 모든 파일 수정에 끼어들고 이 저장소를 쓰는 모든 사람의 로컬 세션에서도 실행되므로 가져오지 않았다.

```
MIT License

Copyright (c) 2026 Ahmed

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
