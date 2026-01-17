# Capability Feature Workflow

Guide users through creating PRDs for capability-focused features. This workflow emphasizes system functionality (APIs, data models, business logic) over UI polish, using a conversational approach to gather context and build the PRD section by section.

## Initial Offer

Offer a structured workflow for creating the PRD through conversation. Explain the stages:

1. **Context Gathering**: Understand the feature, problem it solves, and user journey
2. **Technical Design**: Work through data models, APIs, business logic, and integrations
3. **Drafting & Refinement**: Build the PRD section by section with iteration

Ask if they want to use this workflow or prefer to work freeform.

If user declines, work freeform. If user accepts, proceed to Stage 1.

## Stage 1: Context Gathering

**Goal:** Understand what the feature does, why it's needed, and how users will interact with it.

### Initial Questions

Start with high-level context:

1. What is this feature called?
2. What problem does it solve?
3. What's the main user journey or workflow?
4. Is there a specific route/page for this feature?
5. What similar features exist in the codebase that you'd want this to follow?

### Understanding the User Journey

Once initial context is gathered, dig into the user journey:

- What triggers this feature?
- What steps does the user go through?
- What does the user see or receive at the end?
- What are the key actions the user takes?

Ask clarifying questions about edge cases:
- What happens if something fails?
- Are there different paths for different user types?
- What validations or constraints exist?

### Technical Context

Ask about technical components:

- What data needs to be stored?
- Are there external services involved?
- What APIs need to exist?
- How does this integrate with existing systems?

### Exit Condition

Move on when you understand:
- The user journey clearly
- What data flows through the system
- What technical components are needed

**Transition:**
Summarize your understanding and ask if anything is missing before moving to technical design.

## Stage 2: Technical Design

**Goal:** Define the technical implementation details - data models, APIs, business logic, and integrations.

### Data Model Design

Work through what needs to be stored:

1. Ask about entities: "What are the main things this feature needs to store?"
2. For each entity, ask about key fields
3. Ask about relationships between entities
4. Confirm database tables/types needed

Generate a draft data model and iterate based on feedback.

### API Contracts

Work through the API endpoints:

1. List the operations needed (create, read, update, delete, custom actions)
2. For each endpoint, define:
   - HTTP method and path
   - Request format
   - Success response format
   - Error responses
3. Ask about authentication and authorization requirements

### Business Logic

Ask about processing rules:

- What validations are needed?
- Are there calculations or algorithms involved?
- What state transitions exist?
- What side effects happen (notifications, webhooks, etc.)?

### Integration Points

Clarify how this feature connects to other systems:

- What database tables are read/written?
- What external APIs are called?
- What events are emitted or consumed?
- What authentication/authorization is needed?

### Error Handling

Ask about failure scenarios:

- What can go wrong?
- How should each error be handled?
- What gets logged?
- What metrics should be tracked?

### UI Components (Minimal)

Since this is capability-focused, keep UI discussion minimal:

- What components are needed?
- What does each component do (behavior, not appearance)?
- Simple layout notes (not detailed mockups)

**Exit Condition:**
When technical design is clear enough to implement.

**Transition:**
Confirm the technical design is complete and ready to draft the PRD.

## Stage 3: Drafting & Refinement

**Goal:** Create the PRD document using the standard structure.

### Create Initial Structure

Determine the feature directory name:

**If draft mode:**
1. Generate a slug from the feature name (lowercase, hyphens, no special chars, 2-3 words max)
2. Propose: "I'll create this in `tmp/{slug}/PRD.md`. Does this slug work?"
3. Create `tmp/{slug}/PRD.md`

**If normal mode:**
1. Scan `docs/features/` to find existing feature directories
2. Identify the highest feature number (e.g., `001-walking-skeleton` → 001)
3. Increment to get the next feature number (e.g., 002)
4. Generate a slug from the feature name:
   - Convert to lowercase
   - Replace spaces with hyphens
   - Remove special characters
   - Keep it concise (prefer 2-3 words max)
5. Propose the directory name: `{number}-{slug}` (e.g., `002-user-profile`)
6. Ask: "I'll create this in `docs/features/{number}-{slug}/`. Does this slug work, or would you prefer a different one?"
7. If user suggests a different slug, use that instead

Create the directory and the file `PRD.md` inside it with placeholder sections:

- Summary
- User Stories
- Acceptance Criteria
- Technical Notes
- Data Flow
- Dependencies

Confirm the file path created.

### Build Each Section

For each section:

#### Summary Section

Draft 2-3 sentences describing what the feature does and why. Include the route if applicable.

Ask for feedback and refine.

#### User Stories Section

Based on the user journey discussed, draft user stories in the format:
- As a [role], I can [action] and [outcome]

Aim for 3-5 concrete stories.

Ask for feedback and refine.

#### Acceptance Criteria Section

Generate testable acceptance criteria as checkboxes covering:
- Key user actions and outcomes
- API endpoints working correctly
- Data persistence
- Edge cases and error handling
- Authentication/authorization

Ask what's missing or should be removed.

Refine based on feedback.

#### Technical Notes Section

Document:
- Stack and key technical decisions
- Key entities/tables with their fields
- API endpoints with brief purpose

Use the technical design from Stage 2.

Ask for feedback and refine.

#### Data Flow Section

Create a simple ASCII diagram showing the main flow:
```
User action
    ↓
API endpoint
    ↓
Business logic
    ↓
Result
```

For more complex flows, show branching or parallel operations.

Ask for feedback and refine.

#### Dependencies Section

List external services, APIs, or infrastructure needed.

Ask for feedback and refine.

### Final Review

Once all sections are complete:

1. Re-read the entire PRD for consistency and completeness
2. Check that technical details match across sections
3. Verify acceptance criteria cover all user stories
4. Confirm the data flow matches the API contracts

Provide final suggestions for improvement.

Ask if the PRD is complete or if anything needs adjustment.

## Tips for Effective Guidance

**Tone:**
- Be direct and procedural
- Ask specific questions rather than open-ended ones
- Focus on technical details over UI polish

**Handling Deviations:**
- If user wants to skip a stage, accommodate them
- If user provides all information upfront, adapt the workflow
- Always give user agency to adjust the process

**Context Management:**
- Don't let gaps accumulate - address them immediately
- If something is unclear, ask right away
- Reference information from earlier in the conversation

**File Management:**
- Use Bash ls to scan docs/features/ for existing features
- Use Write to create the initial PRD file in the new feature directory
- Use Edit with str_replace for all refinements
- Never rewrite entire sections - make surgical edits

**Quality over Speed:**
- Ensure technical details are concrete and implementable
- Make sure acceptance criteria are actually testable
- Verify the data flow matches the described implementation

## PRD Structure Reference

See `../references/prd-template.md` for the exact structure and format to follow.
