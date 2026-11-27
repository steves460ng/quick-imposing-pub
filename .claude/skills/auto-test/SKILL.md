---
name: auto-test
description: Use only when a new source file with public functions has just been created and no corresponding test file exists, or when the user asks how to test something. Suggest tests once; do not write them without approval.
version: 1.1.0
---

# Auto Test Skill

This skill automatically suggests test generation when new code is written or modified.

## When This Skill Applies

Activate when:
- A new source file (not a test file) with public functions has just been created and has no corresponding test file
- The user asks "how should I test this?" or similar

Do NOT activate when:
- The user is editing a test file
- The user is writing configuration, documentation, or migrations
- The user explicitly says they don't want tests
- You already suggested tests for the same file in this session

## Behavior

### After new code is written

1. **Check for existing tests** - Look for a corresponding test file
2. **If no test file exists**, suggest:
   ```
   This file doesn't have tests yet. Want me to generate them?
   Detected framework: <framework>
   Test file would be: <path>
   Public methods to cover: <list>
   ```
3. **If test file exists but doesn't cover new code**, suggest:
   ```
   The existing test file at <path> doesn't cover these new methods:
   - <method_name>
   Want me to add tests for them?
   ```

### Test generation approach

When generating tests:

1. **Read the source file** to understand the code
2. **Read existing tests** in the project to match style and conventions
3. **Detect the framework** from project config files
4. **Generate tests** covering:
   - Happy path for each public method
   - Edge cases (nil, empty, boundary values)
   - Error cases (invalid input, exceptions)
5. **Show the tests** before writing, let the user approve

### Framework detection priority

1. Check project root for config files (Gemfile, package.json, pyproject.toml, etc.)
2. Check existing test directories (spec/, test/, __tests__/, tests/)
3. Look at existing test file imports to confirm the framework
4. Default to the most common framework for the language if ambiguous

### Response format

When suggesting tests:

```
**Test suggestion for <source_file>**
Framework: <detected>
Test file: <target_path>
Coverage: <N> methods, <M> tests

Want me to generate the full test file?
```

When writing tests:

```
**Generated tests for <source_file>**
Framework: <detected>
Tests: <count>
Covers: <method list>

<test code>
```

## References

Framework detection, test path conventions, source-to-test file mapping and per-framework patterns are in `references/frameworks.md`. Read it before choosing a framework or a test file path.
