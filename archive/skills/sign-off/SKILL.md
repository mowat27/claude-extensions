---
name: sign-off
description: Final validation before merge/deploy. Runs acceptance checks, then code review and security review. Use when user asks to "sign off", "final check", "ready to merge", or validate a task is complete and reviewed.
---

# Sign-Off

**DIAGNOSTIC ONLY: This skill validates and reports. Never attempt to fix issues. Report findings and stop.**

Run acceptance checks, then code and security reviews. Report all results.

## Usage

```
/sign-off <task_number>
```

Example: `/sign-off 001.001`

## Workflow

### Phase 1: Acceptance Check

Run the acceptance-check skill with the task number:

```
/acceptance-check <task_number>
```

**If acceptance check FAILS**: Stop here. Report the failure and do not proceed to Phase 2.

### Phase 2: Code Reviews (concurrent)

Only if Phase 1 passes, run two review agents **in parallel** using the Task tool:

#### Agent 1: Code Review

**Prompt:**
> DIAGNOSTIC ONLY: Run the code review and report findings. Do not fix issues.
>
> Run: `/review`
>
> Report all findings with their priority levels.

#### Agent 2: Security Review

**Prompt:**
> DIAGNOSTIC ONLY: Run the security review and report findings. Do not fix issues.
>
> Run: `/security review`
>
> Report all findings with their priority levels.

## Output Format

```
## Sign-Off: <task_number>

### Acceptance Check
[PASS/FAIL summary from acceptance-check]

### Code Review
[Findings from /review]

### Security Review
[Findings from /security review]

## RESULT: PASS/FAIL
```

## Pass/Fail Criteria

**FAIL** if ANY of these conditions:
- Acceptance check failed
- Code review reported HIGH or CRITICAL priority issues
- Security review reported HIGH or CRITICAL priority issues

**PASS** only if:
- Acceptance check passed
- No HIGH or CRITICAL issues from either review

Medium/low priority issues do not block sign-off but should be reported.

**DIAGNOSTIC ONLY: Report results. Never fix, resolve, or remediate issues.**
