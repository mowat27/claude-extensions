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

For each user journey in the PRD:

#### Phase 1: E2E Test (if testing level 3, 4, or 5)

**Skip this phase entirely if testing level is 1 or 2.**

Create a task to write a failing e2e test that documents the user journey. This task comes before any implementation.

**E2E test lifecycle:**
1. Write test for user journey
2. Run test — verify it fails because feature doesn't exist (not because test is broken or environment misconfigured)
3. Mark test as `skip` with reason: "Verified failing - awaiting implementation"
4. Implementation tasks reference which skipped test they will enable
5. After implementation, unskip test and verify it passes

#### Phase 2: Implementation
Break into tasks following this order:
1. **Setup** - Project scaffolding, first task only (see below)
2. **Deletions** - Remove dead code first
3. **Bugs** - Fix broken things
4. **Refactoring** - Clean before adding
5. **Features** - New functionality last

**Setup task (if needed):**
Include a setup task as Task 0 when project infrastructure doesn't exist yet:
- Generate app scaffolding
- Configure test frameworks (Vitest, Playwright)
- Set up dev server, env files, database config
- Tests run and pass (no actual tests yet)
- Hello World at root route to verify working
- All baseline infrastructure in place before any feature work

**Unit test requirements (if testing level 2, 4, or 5):**
For each implementation task that involves logic:
- Add to description: "Write unit tests for [component/function]"
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

#### Phase 3: Apply Fidelity Filter
For each potential task, check fidelity-dial.md:
- Include if within level scope
- Exclude if above level scope
- Always include baseline.md requirements

### 4. Task Structure

Each task must have:

```markdown
## Task: {descriptive name}

**Type:** setup | deletion | bug | refactoring | feature
**Journey:** {which user journey this supports}
**Enables:** {which skipped e2e test this will enable, if applicable}
**Testing:** {testing requirements for this task}

### Description
{What needs to be done}

### Acceptance Criteria
- [ ] {Specific, verifiable criterion}

### Testing Requirements
{Include based on testing level:}

Level 1: (omit this section)

Level 2 (unit only):
- [ ] Unit tests cover new/changed logic
- [ ] Tests follow existing patterns

Level 3 (e2e only):
- [ ] E2E test passes (or skipped pending implementation)

Level 4 (unit + e2e):
- [ ] Unit tests cover new/changed logic
- [ ] E2E test passes (or skipped pending implementation)

Level 5 (full suite):
- [ ] Unit tests cover new/changed logic
- [ ] E2E test passes
- [ ] {Specific acceptance tests as selected}

### Baseline Requirements
- [ ] Logging in place
- [ ] Lint + typecheck passing
- [ ] Tests passing (if testing level >= 2)
- [ ] Deployable
```

For e2e test tasks (level 3, 4, 5), acceptance criteria must include:
- [ ] Test fails because feature doesn't exist
- [ ] Test marked as skip with reason

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

## 001.001: {Setup task}
...

## 001.002: Write failing e2e test for {journey}
...

## 001.003: {next task}
...
```

## Rules

1. **One journey = one e2e test task first** - If testing level 3, 4, or 5
2. **Order matters** - setup → deletions → bugs → refactoring → features
3. **Fidelity is a ceiling** - Don't add tasks above the level
4. **Baseline is a floor** - Always include non-negotiables
5. **No inference** - Don't guess fidelity from PRD tone or scope
6. **Prompt don't assume** - If fidelity not given, ask explicitly
7. **E2E tests skip after verification** - Tests proven to fail correctly get skipped until implementation
8. **Setup task when needed** - Include Task 0 if project infrastructure doesn't exist
9. **Testing level is separate from fidelity** - Low fidelity can still have full testing
10. **Detect before asking** - Inspect codebase before prompting for testing level
11. **Default to level 4** - Unless user specifies otherwise or codebase suggests different
12. **Skip e2e phase at level 1-2** - No e2e tests for spikes or unit-only
13. **Follow existing patterns** - Match test file naming, locations, and utilities in codebase
