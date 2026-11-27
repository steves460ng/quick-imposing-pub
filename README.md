# groundwork

**English** | [한국어](README.ko.md)

A Claude Code skill that sets up a project baseline (CI, a check command, and working rules) for a new repository in one go, packaged as a GitHub template repository.

## Why

When you build alone, basics like CI, consistent checks, and working rules tend to get pushed to "later" and never happen. groundwork puts them in place on day one.

**Main benefit: solid project basics**
- CI runs the same checks on every push and PR, so regressions get caught
- A single check command runs format, lint, type, and test checks
- You can merge refactors and Claude-made changes with confidence

**Side benefit: a structure where Claude Code wastes less effort**
- Check output is short, and CI results come back as failures only
- Full test runs are left to CI; Claude runs only the related tests
- Files that never need reading are blocked by permissions, and formatting is handled by hooks
- A notes file carries context across sessions in a few lines

This can also cut token usage. How much depends on the project and your habits, so treat it as a bonus.

Setup itself takes time and tokens, so groundwork suits **long-lived projects**. It isn't recommended for throwaway repositories you'll use for a few days.

## What it does

Run `/groundwork` and Claude asks you questions one at a time: seven at most, each with a recommended default. When you're done, it creates the files below, verifies that the checks and hooks work, and opens a PR.

| Output | Purpose |
|---|---|
| Quiet check command | Format → lint → types → tests. Prints one line on success; on failure, only `file:line` and the error. Pass a path to run only related tests |
| CI result check | Uses whatever actually works in your environment (GitHub MCP tools or a `ci-status` command) to fetch only the failing part. No more pasting logs |
| `.claude/settings.json` + hooks | Blocks reading lock files and build output, blocks running test runners directly, auto-formats after edits |
| `.claude/notes.md` | Work notes, 20 lines max. Skipped if the repository already has a handoff document such as HANDOFF |
| `CLAUDE.md` | 60 lines max. Use only the check command, check CI results after pushing, work on a branch and merge PRs only with your approval, read the handoff notes first (recommended), and so on |
| `CONTEXT.md` + generator script | Optional, for larger projects. Holds only what a script can extract reliably: structure, entry points, exported names |
| `ci.yml` | Full checks run in CI. Docs-only changes are skipped |

It never adds tools or dependencies you weren't asked about. Run it again on an already set-up repository and it asks only about what changed, showing a diff before touching existing files.

It also works on repositories that already have code. In that case it first reviews each output as "add as is / add with changes / skip" and builds only what you pick. Existing handoff docs, test commands, and formatting policies take priority.

## Usage

1. On this repository's page, click **Use this template → Create a new repository**.
2. Open a Claude Code on the web session for the new repository. If you make a change request before setup, Claude suggests running `/groundwork` first.
3. Run `/groundwork` and answer the questions.
4. Review and merge the PR Claude opens.

After setup, the template-only files (`.template/`, `.github/workflows/skill-check.yml`, `README.ko.md`) are removed and this README and `CLAUDE.md` are rewritten for the new project. `.claude/skills/groundwork/` stays so you can run it again later.

> The skill instructions are written in Korean, but Claude replies in the language you use. If it doesn't, just ask it to use English.

## Contents

| Path | Purpose |
|---|---|
| `.claude/skills/groundwork/SKILL.md` | The skill itself |
| `.claude/skills/auto-test/`, `.claude/commands/generate-tests.md`, `.claude/agents/test-writer.md` | Test generation tools. Suggests tests for code that has none, and `/generate-tests <path>` writes test files. New tests are run with the quiet check command. Adapted from [test-generator](https://github.com/a-abdellatif98/test-generator) (MIT) without its hook. The interview asks whether to keep them as a command only (recommended), with auto suggestions, or not at all |
| `.claude/THIRD_PARTY_NOTICES.md` | Source and license of the imported files |
| `CLAUDE.md` | Temporary rules for repositories created from the template: suggests running `/groundwork` once before the first change, and keeps work on branches with merges only on your approval. Replaced during setup |
| `.template/MANIFEST` | Template-only files to clean up in new repositories |
| `.template/check.py` | Skill format checker (Python standard library only) |
| `.github/workflows/skill-check.yml` | CI that checks the skill when it changes. Runs only in this origin repository |
