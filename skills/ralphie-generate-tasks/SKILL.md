---
name: ralphie-generate-tasks
description: Generate executable tasks from a PRD. Use when user wants to break down a PRD into tasks, create a task list from requirements, or turn a feature spec into implementation steps. Also use when user asks about fidelity settings, fidelity levels, what the fidelity dial means, or testing levels.
---

# Ralphie Generate Tasks

Generate a structured task list from a Product Requirements Document.

## Input

- **PRD path** - Path to the PRD markdown file (required)
- **Fidelity level** - 1-10 scale (required, prompt if not provided)
- **Testing level** - 1-5 scale (required, prompt if not provided, default: 4)
- **Output path** - Where to write TASKS.md (default: same directory as PRD)

## Modes

### Mode 1: Explain Fidelity
If user asks about fidelity settings/levels/dial:
1. Read `references/fidelity-dial.md`
2. Read `references/baseline.md`
3. Explain both clearly
4. Stop there — don't generate tasks

### Mode 1a: Explain Testing
If user asks about testing settings/levels:
1. Read `references/testing-levels.md`
2. Explain levels and detection logic
3. Stop there — don't generate tasks

### Mode 2: Generate Tasks
If user provides a PRD or asks to generate tasks:

**If fidelity level is not provided, ask for it.** Do not infer from PRD content.

Prompt: "What fidelity level (1-10)? 1-2=skeleton, 5-6=functional, 9-10=polished. See references/fidelity-dial.md for details."

**If testing level is not provided, detect infrastructure first, then ask.**

See Algorithm Step 0 for detection. Then prompt with recommendation:
"What testing level (1-5)? 1=none (spike), 2=unit only, 3=e2e only, 4=unit+e2e (recommended), 5=full suite. See references/testing-levels.md for details."

## Algorithm

### 0. Detect Codebase Testing Infrastructure

Before prompting for testing level, inspect the current codebase:

1. **Glob for config files:**
   - `vitest.config.*` → note "Vitest"
   - `playwright.config.*` → note "Playwright"
   - `jest.config.*` → note "Jest"
   - `cypress.config.*` → note "Cypress"

2. **Count existing test files (exclude node_modules):**
   - `**/*.test.{ts,tsx}` → count unit tests
   - `**/*.spec.{ts,tsx}` → count spec tests
   - `e2e/**/*` → count e2e tests

3. **Check for test infrastructure:**
   - `e2e/` → note "e2e directory"
   - `__tests__/` → note "jest-style tests"
   - `**/test-utils/**` → note "test utilities"
   - `**/fixtures/**` → note "fixtures"

4. **Read documentation:** `.claude/docs/testing.md` if exists

5. **Report findings and suggest:**
   ```
   Detected: Vitest (unit), Playwright (e2e), 12 unit tests, 5 e2e tests
   Suggested level: 4 (unit + e2e)
   ```

**Suggestion logic:**
- No test infrastructure → suggest 3 (e2e only)
- Unit tests only → suggest 2 or 4
- Mature infrastructure → suggest 4
- User says "spike" → suggest 1

### 1. Load References

Read before generating:
- `references/baseline.md` - Non-negotiables for all tasks
- `references/fidelity-dial.md` - What to include/exclude at this level
- `references/testing-levels.md` - What testing to include at this level

### 2. Parse PRD

Extract from PRD:
- User stories → become user journeys
- Acceptance criteria → become verification points
- Technical notes → inform implementation tasks
- Data flow → informs integration tasks

### 3. Generate Tasks

**CRITICAL: Vertical Slices Over Horizontal Layers**

Generate tasks that deliver complete user journeys vertically, not infrastructure horizontally.

For each user journey in the PRD, create ONE task slice that includes everything needed for that journey:
1. E2E test (if testing level 3, 4, or 5)
2. Implementation (all layers: DB → domain → API → UI as needed)
3. Unit tests (if testing level 2, 4, or 5)

**Task ordering between slices:**
1. **Setup** - Infrastructure task ONLY if project doesn't exist (Task 0)
2. **Deletions** - Remove dead code that blocks new work
3. **Bugs** - Fix broken things that prevent new features
4. **Refactoring** - Clean code that must change before adding features
5. **Features** - New user journeys, each as a complete vertical slice

**Within each journey slice:**
1. Write e2e test (if testing level 3, 4, or 5)
2. Run test — verify it fails because feature doesn't exist
3. Mark test as `skip` with reason: "Verified failing - awaiting implementation"
4. Implement feature through all necessary layers (DB, domain, API, UI)
5. Write unit tests for business logic (if testing level 2, 4, or 5)
6. Unskip e2e test and verify it passes
7. Verify all baseline requirements

**Example (correct - vertical slicing):**
```
001.001: Setup project infrastructure (only if new project)
001.002: User login journey
  - E2E test for login flow
  - DB: users table, auth schema
  - API: POST /auth/login endpoint
  - UI: login form component
  - Unit tests: auth validation logic
001.003: User registration journey
  - E2E test for registration flow
  - DB: extend users table
  - API: POST /auth/register endpoint
  - UI: registration form
  - Unit tests: registration validation
```

**Anti-pattern (incorrect - horizontal layering):**
```
001.001: Setup
001.002: Write all e2e tests
001.003: Build database schema
001.004: Build all API endpoints
001.005: Build all UI components
```

**When to split a journey into sub-tasks:**

Only split if a journey is genuinely too large (8+ hour estimate). Split by user action within journey, NOT by technical layer:

✅ Split by user action:
```
001.002a: Login with email/password
001.002b: Login with OAuth provider
```

❌ Don't split by layer:
```
001.002a: Login API
001.002b: Login UI
```

**Setup task (Task 0, only if needed):**

Include a setup task as Task 0 when project infrastructure doesn't exist yet:
- Generate app scaffolding
- Configure test frameworks (Vitest, Playwright)
- Set up dev server, env files, database config
- Tests run and pass (no actual tests yet)
- Hello World at root route to verify working
- All baseline infrastructure in place before any feature work

**Unit test requirements (if testing level 2, 4, or 5):**

For each journey slice that involves business logic:
- Include in task description: "Write unit tests for [business logic]"
- Add to acceptance criteria: "Unit tests cover new/changed logic"
- Note: Follow existing test patterns in codebase (co-located vs separate, naming conventions)

**Acceptance test requirements (if testing level 5):**

Prompt user: "What additional acceptance tests are needed?"
- Performance (response time targets)
- Security (OWASP checks)
- Load (concurrent user targets)
- Accessibility (WCAG level)
- Other (specify)

Add corresponding tasks/criteria based on selection.

### 4. Apply Fidelity Filter

For each potential task, check fidelity-dial.md:
- Include if within level scope
- Exclude if above level scope
- Always include baseline.md requirements

### 5. Task Structure

Each task must have:

```markdown
## Task: {descriptive name of user journey}

**Type:** setup | deletion | bug | refactoring | feature
**Slice:** {which complete user journey this delivers}
**Testing:** {testing requirements for this task}

### Description
{What needs to be done - describe the complete vertical slice}

Include all layers needed:
- E2E test (if applicable)
- Database changes (if applicable)
- Domain/business logic
- API endpoints
- UI components
- Unit tests (if applicable)

### Acceptance Criteria
- [ ] {Specific, verifiable criterion for the complete journey}
- [ ] {Cover all layers of the slice}

### Testing Requirements
{Include based on testing level:}

Level 1: (omit this section)

Level 2 (unit only):
- [ ] Unit tests cover business logic
- [ ] Tests follow existing patterns

Level 3 (e2e only):
- [ ] E2E test fails before implementation
- [ ] E2E test marked as skip with reason
- [ ] E2E test passes after implementation

Level 4 (unit + e2e):
- [ ] E2E test fails before implementation
- [ ] E2E test marked as skip with reason
- [ ] Unit tests cover business logic
- [ ] E2E test passes after implementation

Level 5 (full suite):
- [ ] E2E test lifecycle complete
- [ ] Unit tests cover business logic
- [ ] {Specific acceptance tests as selected}

### Baseline Requirements
- [ ] Logging in place for key operations
- [ ] Lint + typecheck passing
- [ ] Tests passing (if testing level >= 2)
- [ ] Deployable (no hardcoded secrets, env vars used)
- [ ] Auth checks on protected routes
- [ ] User input sanitized
```

## Output Format

**Task numbering:** `{feature}.{task}` where both are zero-padded to 3 digits.
- Feature number extracted from directory name (e.g., `001-walking-skeleton` → `001`)
- Tasks numbered starting at 001

Write to TASKS.md:

```markdown
# Tasks: {Feature Name}

**Source:** {PRD path}
**Fidelity:** {level}/10
**Testing:** {level}/5 ({name})
**Generated:** {date}

## Summary
{Brief overview of task breakdown}

## Testing Infrastructure
{Summary of detected infrastructure from Step 0}
- Frameworks: {list or "none detected"}
- Patterns: {e.g., "co-located *.test.ts" or "separate __tests__/"}
- Utilities: {list or "none"}

---

## 001.001: {Setup task (only if needed)}
...

## 001.002: {First user journey - complete vertical slice}
...

## 001.003: {Next user journey - complete vertical slice}
...
```

## Rules

1. **Vertical not horizontal** - Deliver complete user journeys, not technical layers
2. **One journey = one task** - E2E test + all implementation layers + unit tests together
3. **Order within slice** - e2e test → verify fail → skip → implement (all layers) → unskip test
4. **Order between slices** - setup → deletions → bugs → refactoring → features
5. **Fidelity is a ceiling** - Don't add tasks above the level
6. **Baseline is a floor** - Always include non-negotiables
7. **No inference** - Don't guess fidelity from PRD tone or scope
8. **Prompt don't assume** - If fidelity not given, ask explicitly
9. **E2E tests skip after verification** - Tests proven to fail correctly get skipped until implementation
10. **Setup task when needed** - Include Task 0 if project infrastructure doesn't exist
11. **Testing level is separate from fidelity** - Low fidelity can still have full testing
12. **Detect before asking** - Inspect codebase before prompting for testing level
13. **Default to level 4** - Unless user specifies otherwise or codebase suggests different
14. **Skip e2e phase at level 1-2** - No e2e tests for spikes or unit-only
15. **Follow existing patterns** - Match test file naming, locations, and utilities in codebase
16. **Complete slices over partial layers** - A working login is better than half of all features

## Anti-Patterns to Avoid

### ❌ Pattern 1: Horizontal Layering

**Bad example:**
```markdown
## 001.002: Create command layer abstraction
- Extract selectImage command
- Add error type definitions
- Update error mapping

## 001.003: Create domain layer functions
- Implement selectImageGeneration
- Implement selectProseGeneration

## 001.004: Refactor all routes
- Apply command pattern to /images
- Apply command pattern to /prose
```

**Why wrong:** Builds infrastructure horizontally across all features. No user value until all tasks complete.

**Good example:**
```markdown
## 001.002: Select image for blog post
- Write e2e test: user selects image from generation history
- Verify test fails (feature doesn't exist)
- Skip test with reason
- Implement POST /api/images/:id/select (route → command → domain → DB)
- Unit tests for selectImage command
- Unskip e2e test, verify passes

## 001.003: Select prose for blog post
- Write e2e test: user selects prose from generation history
- Implement POST /api/prose/:id/select (route → command → domain → DB)
- Unit tests for selectProse command
```

**Why right:** Each task delivers a complete, testable user capability. Extract common patterns later if they emerge naturally.

### ❌ Pattern 2: Test Phase Separation

**Bad example:**
```markdown
## 001.002: Write all e2e tests
- Test user login
- Test user registration
- Test password reset

## 001.003: Implement auth features
- Login endpoint
- Registration endpoint
- Password reset
```

**Why wrong:** Tests separated from implementation. Easy to skip unskipping tests.

**Good example:**
```markdown
## 001.002: User login journey
- E2E test for login flow
- Verify fails, mark skip
- Implement login (all layers)
- Unskip test, verify passes

## 001.003: User registration journey
- E2E test for registration
- Verify fails, mark skip
- Implement registration (all layers)
- Unskip test, verify passes
```

**Why right:** Test lifecycle tightly coupled with implementation. Can't forget to unskip.

### ❌ Pattern 3: Infrastructure First

**Bad example:**
```markdown
## 001.002: Set up auth middleware
## 001.003: Create database schema
## 001.004: Build API client wrapper
## 001.005: Implement first feature
```

**Why wrong:** Speculative infrastructure before knowing what's needed.

**Good example:**
```markdown
## 001.002: User login journey
- Implement login (creates auth middleware as needed)
- Creates users table as needed
- Makes API calls directly

## 001.003: User registration journey
- Extends auth middleware if needed
- Extends users table if needed
- Reuses or extends API patterns from login
```

**Why right:** Infrastructure emerges from actual feature needs. No gold-plating.
