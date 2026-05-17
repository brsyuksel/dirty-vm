# dirty-vm Agentic Development Guide

This document defines the agentic development workflow for the dirty-vm project.

## Project Overview

dirty-vm is a [shellican](https://github.com/brsyuksel/shellican) collection for managing disposable virtual machines with QEMU/KVM on Linux. All scripts use only the Python standard library or shell builtins — no external dependencies.

## Testing Environment

To test the collection in-place without importing:

```bash
export SHELLICAN_HOME=/path/to/dirty-vm/repo/root
shellican run dirty-vm <command> [args...]
```

This lets agents and developers run commands directly against the working tree.

## Agent Roles

### Kimi K2.6 (Leader)
- **Role**: Orchestrator, architect, final approver.
- **Responsibilities**:
  - Decompose user requests into discrete tasks.
  - Assign tasks to the appropriate agent.
  - Review agent outputs before applying to the codebase.
  - Handle complex, ambiguous, or high-stakes changes directly.
  - Ensure all code uses only stdlib and follows project conventions.
- **When to use**: Strategy decisions, final code review, complex refactors, direct user interaction.

### Minimax M2.5 Free (Implementation Agent)
- **Role**: Primary coder.
- **Responsibilities**:
  - Implement new runnables (scripts, YAML configs, hooks).
  - Refactor existing scripts.
  - Write unit tests using `unittest` and `unittest.mock` (stdlib only).
  - Iterate on features based on review feedback.
- **When to use**: Clear, well-specified coding tasks with defined inputs/outputs.
- **Constraints**: Must use only Python stdlib. Must not run git commands. Must not modify `AGENTS.md`.

### Nemotron 3 Super Free (Review & Analysis Agent)
- **Role**: Code reviewer, logic verifier, root-cause analyst.
- **Responsibilities**:
  - Review diffs and script logic for correctness.
  - Identify edge cases in QEMU networking, cloud-init, and VM lifecycle code.
  - Analyze bugs and suggest fixes.
  - Validate design alternatives.
- **When to use**: Before merging agent-written code, when investigating bugs, or when validating architectural decisions.
- **Constraints**: Read-only analysis; does not apply edits directly.

### Big Pickle Free (Documentation & Research Agent)
- **Role**: Documentation writer, script summarizer, low-risk analysis.
- **Responsibilities**:
  - Update README.md and runnable help texts.
  - Summarize existing scripts for other agents or users.
  - Draft documentation for new features.
  - Simple research and fact-checking.
- **When to use**: Non-destructive tasks that require structured output and summarization.
- **Constraints**: **Never assigned critical code, git operations, or direct file edits to production scripts.** Always requires Kimi review before any output is committed.

## Workflow

```
User Request
    │
    ▼
Kimi K2.6 (Leader)
    │
    ├─► [New Feature / Refactor] ──► Minimax M2.5 (implement)
    │                                    │
    │                                    ▼
    │                              Nemotron 3 Super (review)
    │                                    │
    │                                    ▼
    │                              Kimi (approve & apply)
    │
    ├─► [Bug Fix] ──► Nemotron 3 Super (root cause)
    │                      │
    │                      ▼
    │                 Minimax M2.5 (implement fix)
    │                      │
    │                      ▼
    │                 Kimi (verify & apply)
    │
    ├─► [Documentation] ──► Big Pickle (draft)
    │                          │
    │                          ▼
    │                     Kimi (review & polish)
    │
    └─► [Complex / Unclear] ──► Kimi (handle directly)
```

## Coding Conventions

- **Python**: Use only the standard library. No `pip`, no `requirements.txt`.
- **Bash**: Use `#!/bin/bash` or `#!/usr/bin/env bash`. Prefer `set -euo pipefail` for safety.
- **YAML**: `collection.yml` and `runnable.yml` must remain parseable by shellican.
- **Commits**: Follow [Conventional Commits](https://www.conventionalcommits.org/).
  - `feat:` new runnable or feature
  - `fix:` bug fix
  - `refactor:` code restructuring without behavior change
  - `test:` adding or updating tests
  - `docs:` README, help text, or documentation changes
  - `chore:` tooling, configuration, or maintenance tasks
- **Git**: Agents must never run `git commit`, `git push`, `git rebase`, etc. Only Kimi performs git mutations when explicitly requested by the user.

## Safety Rules

1. No external Python dependencies.
2. No destructive git operations by agents.
3. `AGENTS.md` is local-only — it is gitignored. Each developer may customize their agent setup.
4. All agent-generated code affecting VM lifecycle (create, start, stop, delete) must pass Nemotron review before Kimi applies it.
5. Never hardcode paths that assume a specific user's home directory structure outside of `~/.dirty-vm`.
