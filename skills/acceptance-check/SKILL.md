---
name: acceptance-check
description: Validate task completion against acceptance criteria from TASKS.md. Use when user asks to validate/check/verify a task (e.g., "check task 001.001"), run acceptance tests, or confirm a feature is complete. Input is a task number like 001.001.
---

# Acceptance Check

**DIAGNOSTIC ONLY: This skill runs validation scripts and reports results. Never attempt to fix, resolve, or work around failures. Never run commands manually if scripts fail. Report what happened and stop.**

Validate task completion by running baseline checks, app validation, and verifying acceptance criteria.

## Usage

```
/acceptance-check <task_number>
```

Example: `/acceptance-check 001.001`

## Workflow

Run validation agents in parallel using the Task tool:

- **Agent 1**: Baseline Acceptance Checks
- **Agent 2**: Task-specific Acceptance Checks

### Agent 1: Baseline Acceptance Checks

2 steps that must run sequentially

### Agent 1, Step 1

**Prompt the agent with:**
> Run this single command and report the output:
>
> python3 <skill_dir>/scripts/validate_baseline.py <project_dir>
>
> Do not run any other commands. Report PASS/FAIL based on script output.

Validates:
- `pnpm check` passes
- `pnpm test` passes with no errors in output

### Agent 1, Step 2

**Prompt the agent with:**
> Run this single command and report the output:
>
> python3 <skill_dir>/scripts/validate_app.py <project_dir>
>
> Do not run any other commands. Report PASS/FAIL based on script output.

Validates:
- `pnpm dev` runs on port 3030
- Main route (`/`) responds 200
- Health route (`/api/health`) responds 200
- `logs/` directory contains .log files

### Agent 3: Acceptance Criteria

**Prompt the agent with:**
> DIAGNOSTIC ONLY: Verify acceptance criteria by reading files and examining code. Do not attempt fixes if criteria fail.

1. Find TASKS.md in `docs/features/` matching task prefix (e.g., `001` → `docs/features/001-*/TASKS.md`)
2. Extract acceptance criteria for the specific task number
3. **Skip criteria already validated by Agents 1 and 2** - these are covered:
   - Lint/typecheck passing (`pnpm check`, `pnpm lint`, `pnpm typecheck`)
   - Tests passing (`pnpm test`, `pnpm test:unit`, `pnpm test:e2e`)
   - Dev server starting (`pnpm dev`)
   - Routes responding (main route `/`, health route `/api/health`)
   - Log files existing in `logs/`
4. Verify **only the remaining criteria** by examining code (read-only)
5. Report pass/fail for each non-skipped criterion

> Do not run commands to fix issues. Report findings only.

## Output Format

Report results clearly:

```
## Acceptance Check: <task_number>

### Baseline Validation
- pnpm check: PASS/FAIL
- pnpm test: PASS/FAIL

### App Validation
- Dev server: PASS/FAIL
- Main route: PASS/FAIL
- Health route: PASS/FAIL
- Logs exist: PASS/FAIL

### Acceptance Criteria
- [criterion 1]: PASS/FAIL (evidence)
- [criterion 2]: PASS/FAIL (evidence)
...

## RESULT: PASS/FAIL
```

## Constraints

- Use port 3030 for dev server (avoid conflicts with user's dev)
- Non-destructive: never delete logs or modify files
- FAIL if ANY check fails
- Run agents in parallel for speed
- **Report only**: On failure, report the error output and stop. Never suggest fixes, remediation steps, or root cause analysis. The skill's job is validation, not troubleshooting.
- **Script-only for Agents 1 & 2**: These agents run their Python script and report output. If the script fails, report failure - do not run manual commands as fallback.

**DIAGNOSTIC ONLY: This skill validates and reports. It never fixes, resolves, or works around issues. Subagents must not attempt remediation.**
