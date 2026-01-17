# Walking Skeleton Workflow

Create a deployable minimal feature that proves the architecture works end-to-end. This workflow guides through architectural decisions and generates project documentation.

## Phase 1: Discovery (Conversational)

Start with open-ended questions to understand the vision. This is a conversation, not a checklist.

**Step 1 - The App:**
Ask: "What does this app do? What problem does it solve?"

Let the user explain in their own words. Follow up on anything unclear.

**Step 2 - The Skeleton:**
Ask: "Describe what a user would experience in the walking skeleton - the simplest end-to-end flow that proves the architecture works."

This should be concrete: what does the user see/do, what happens behind the scenes, what's the output?

**Step 3 - Architecture Conversation:**
Based on Steps 1-2, discuss architecture. This is exploratory:
- Propose architecture patterns that fit what they described
- If multiple valid approaches exist, explain trade-offs
- If you need to research frameworks or patterns, do so (use web search, explore docs)
- Ask clarifying questions about constraints, team experience, existing systems

**Solution selection principle:** Prefer idiomatic, mainstream, well-supported solutions over bespoke approaches found on GitHub. A clunkier built-in solution is better than a clever third-party library with limited adoption. Check if the framework/platform provides native functionality before reaching for external tools.

The goal is to collaboratively arrive at architecture decisions, not to extract answers from a form.

## Phase 2: Technical Details (Informed by Phase 1)

Walk through each category below **one at a time**. For each:
1. Propose sensible defaults based on Phase 1 context
2. Explain briefly why (one sentence)
3. Ask "Does this work, or would you prefer something different?"
4. Only move to the next category after confirmation

Reference `../references/checklist.md` to ensure nothing is missed.

**Categories (in order):**

1. **Environments** - What environments exist? Propose based on deployment target.

2. **Config/Secrets** - How are env vars and secrets handled? Propose based on stack.

3. **Database** - Schema for skeleton entities, local setup approach, migrations.

4. **Auth** - Implementation details: where state lives, session handling.

5. **Development** - Local DB setup, dev server, logging, Docker compose if needed.

6. **Testing** - Framework, test DB setup, isolation approach.

7. **Code Quality** - Linting, type checking, combined check command.

8. **Deployment** - CI/CD pipeline, checks before deploy, verification approach.

9. **LLM Integration** - Config approach for each provider, error handling. (Skip if N/A)

**Guidance:**
- Propose defaults confidently - don't ask if you can reasonably infer
- If the stack choice makes the answer obvious, just state it
- Only ask when there's genuine ambiguity or user preference matters
- Keep each category brief - this isn't a lecture, it's confirmation

## Phase 3: Create Directory Structure

Create if not exists:
```
.claude/docs/
docs/features/
```

## Phase 4: Generate PRD

**If draft mode:**
1. Generate a slug from the project/skeleton name (lowercase, hyphens, 2-3 words max)
2. Propose: "I'll create this in `tmp/{slug}/PRD.md`. Does this slug work?"
3. Create `tmp/{slug}/PRD.md` using `../assets/templates/prd.md`

**If normal mode:**
Create `docs/features/001-walking-skeleton/PRD.md` using `../assets/templates/prd.md`.

Content should include the skeleton definition from Phase 1:
- **Summary**: The minimal feature being built, the happy path flow
- **User Stories**: The happy path as a user story
- **Acceptance Criteria**: What "done" looks like for the skeleton
- **Technical Notes**: Key architectural decisions, entities/tables needed
- **Data Flow**: ASCII diagram showing the request/response flow for this feature
- **Dependencies**: External services, frameworks chosen

Also create `setup.md` in the same directory as the PRD (either `tmp/{slug}/` or `docs/features/001-walking-skeleton/`) documenting any manual setup required:
- External service account creation (Supabase, Vercel, cloud providers)
- API key generation steps
- OAuth configuration steps
- Database seeding or manual data entry
- Any one-time configuration not captured in code

## Phase 5: Generate Documentation

Generate each file using templates from `../assets/templates/`:

| Template | Output | Content From |
|----------|--------|--------------|
| `CLAUDE.md` | `.claude/CLAUDE.md` | Stack summary, key commands, structure overview |
| `architecture.md` | `.claude/docs/architecture.md` | Architecture decisions from Phase 1 |
| `database.md` | `.claude/docs/database.md` | Database decisions from Phase 2 |
| `deployment.md` | `.claude/docs/deployment.md` | Deployment decisions from Phase 2 |
| `testing.md` | `.claude/docs/testing.md` | Testing decisions from Phase 2 |
| `auth.md` | `.claude/docs/auth.md` | Auth decisions (skip if N/A) |
| `llm-integration.md` | `.claude/docs/llm-integration.md` | LLM decisions (skip if N/A) |
| `development.md` | `.claude/docs/development.md` | Development setup from Phase 2 |

## Phase 6: Summary

After generating all files, provide a summary:
- List all files created
- Highlight any decisions that need follow-up
- Suggest next steps (e.g., "implement the skeleton feature")

## Template Guidance

### CLAUDE.md
Keep minimal. Include:
- One-line stack description
- Essential commands (dev, test, build, deploy)
- Brief project structure
- Pointers to `.claude/docs/` for details

### architecture.md
Document patterns and structure:
- Architecture pattern chosen and why
- Framework choices
- Project folder structure
- External service integrations

**Note:** Do not include data flow diagrams here - they belong in feature PRDs. Architecture.md should contain stable, general information that won't go stale as features evolve.

### database.md
Document database setup:
- Provider and why
- Schema for skeleton entities
- Local setup commands
- Migration approach

### deployment.md
Document deployment:
- Environment list with URLs/identifiers
- Target platform details
- Step-by-step deploy process
- CI/CD pipeline configuration
- Docker strategy if applicable
- Health check endpoints
- Smoke test approach

### testing.md
Document testing:
- Framework and why
- Test database setup commands
- Test server setup
- How to run tests
- Isolation strategy
- Test secrets handling
- Linting setup and commands
- Type checking setup and commands
- Combined check command (lint + typecheck)

### auth.md
Document authentication:
- Mechanism chosen and why
- Where state lives
- Implementation notes

### llm-integration.md
Document LLM setup:
- Provider(s) and why
- Configuration approach
- Common usage patterns

### development.md
Document local development:
- Prerequisites
- Database setup steps
- Running the app
- Docker compose if applicable
- Config/secrets access
- Log viewing
