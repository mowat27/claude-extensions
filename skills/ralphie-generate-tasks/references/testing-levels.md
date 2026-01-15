# Testing Levels

Single 1-5 scale controlling testing depth for generated tasks.

## Levels

| Level | Name | Includes | Use When |
|-------|------|----------|----------|
| 1 | **None** | No automated tests | Spikes, throwaway prototypes |
| 2 | **Unit only** | Unit tests, no e2e | Library code, pure functions, backend logic |
| 3 | **E2E only** | E2E tests, no unit | Walking skeletons, integration validation |
| 4 | **Unit + E2E** | Both unit and e2e | Most features (default) |
| 5 | **Full suite** | Unit + e2e + acceptance | High-risk features (perf, security, load tests) |

## How It Affects Task Generation

### Level 1 (None)
- Skip e2e test task entirely
- Skip unit test requirements
- Acceptance criteria: "Manual verification that [feature] works"
- Baseline testing requirement removed (lint/typecheck remain)

### Level 2 (Unit only)
- No e2e test task
- Implementation tasks include: "Unit tests for [component/logic]"
- Acceptance criteria: "Unit tests pass"
- Follow existing unit test patterns in codebase

### Level 3 (E2E only)
- E2E test task for each user journey (first task)
- No unit test requirements in implementation tasks
- Acceptance criteria reference e2e test only
- Good for walking skeletons proving integration works

### Level 4 (Unit + E2E) - Default
- E2E test task for each user journey
- Implementation tasks include: "Unit tests for [component/logic]"
- Acceptance criteria: "Unit tests pass" + "E2E test passes"

### Level 5 (Full suite)
- All of level 4
- Prompt user for specific acceptance test types needed:
  - Performance: "Response time under X ms"
  - Security: "No SQL injection, XSS vulnerabilities"
  - Load: "Handles N concurrent users"
  - Accessibility: "WCAG AA compliance"
  - Other: User specifies

## Codebase Detection

Before prompting for testing level, inspect the codebase:

### 1. Check for test framework configs

Glob for config files in project root:
- `vitest.config.*` → Vitest available
- `playwright.config.*` → Playwright available
- `jest.config.*` → Jest available
- `cypress.config.*` → Cypress available

### 2. Count existing test files

Glob (excluding node_modules):
- `**/*.test.{ts,tsx,js,jsx}` → unit test count
- `**/*.spec.{ts,tsx,js,jsx}` → spec test count
- `e2e/**/*` → e2e test count

### 3. Check for test infrastructure

Look for:
- `e2e/` directory → e2e tests present
- `__tests__/` directory → jest-style tests
- `tests/` or `test/` directory → test directory
- `**/test-utils/**` → test utilities
- `**/fixtures/**` → test fixtures
- `**/__mocks__/**` → mocks present

### 4. Check documentation

Read `.claude/docs/testing.md` if exists for framework details.

### 5. Report findings and suggest default

Example output:
```
Detected testing infrastructure:
- Frameworks: Vitest, Playwright
- Test files: 12 unit tests, 5 e2e tests
- Utilities: e2e/fixtures/, lib/test-utils/

Suggested level: 4 (unit + e2e)
```

**Suggestion logic:**
- No test infrastructure → suggest level 3 (e2e only, simpler to set up)
- Unit tests only → suggest level 2 or 4 depending on if e2e framework exists
- Mature infrastructure (both frameworks, utilities) → suggest level 4
- User explicitly says "spike" → suggest level 1
