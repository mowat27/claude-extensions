# Baseline Non-Negotiables

These requirements apply to ALL tasks regardless of fidelity level. Even a level-1 skeleton must meet these.

## Observability

- Key operations are logged (not just errors)
- Logs include enough context to debug issues
- Use structured logging (not console.log)

## Deployability

- All config via environment variables
- No hardcoded secrets, URLs, or environment-specific values
- Works in CI pipeline
- Database migrations included if schema changes

## Testability

Requirements vary by testing level (see `testing-levels.md`):

**If testing level 2, 4, or 5:**
- Unit tests for non-trivial logic
- Tests follow existing patterns in codebase

**If testing level 3, 4, or 5:**
- E2E test for user journey written BEFORE implementation
- Test must fail before feature is built (proves it tests the right thing)
- Test documents the intended user flow

**If testing level 5:**
- Additional acceptance tests as specified (perf, security, etc.)

**If testing level 1:**
- No automated tests required (spike/prototype only)

## Code Quality

- Linting passes (no new lint errors introduced)
- Type checking passes (no type errors)

## Security

- Auth checks on protected routes/endpoints
- User input sanitized before use
- No secrets in client-side code
- RLS policies on new tables

## Reliability

- Happy path completes without error
- Errors surface to user (no silent failures)
- Data persists correctly
- No broken dependencies introduced
