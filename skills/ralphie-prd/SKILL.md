---
name: ralphie-prd
description: Generate PRDs for features. Supports walking skeletons (greenfield projects), capability features (backend-focused), and more. Use when user mentions "write a PRD", "create a PRD", "document this feature", "bootstrap a project", "walking skeleton", or starts describing a feature.
---

# Ralphie PRD

Unified PRD generation for different feature types. Routes to the appropriate workflow based on what you're building.

## Draft Mode Detection

Before asking about feature type, check if the user's request indicates this is a draft/temporary PRD. Look for phrases like:
- "draft", "temporary", "temp", "working draft"
- "hidden", "not for this branch"
- "idea", "future feature", "planning ahead"
- "don't want to pollute", "separate from current work"

If detected, confirm: "This sounds like a draft PRD - I'll write it to `tmp/{slug}/PRD.md` to keep it separate from your active feature work. Correct?"

When in draft mode, pass this context to the workflow. The workflow will:
- Write to `tmp/{slug}/PRD.md` instead of `docs/features/{number}-{slug}/PRD.md`
- Skip feature numbering entirely
- For walking skeletons, still create `.claude/docs/` files normally (those aren't feature-specific)

## Entry Point

When invoked, ask the user what type of feature they're building:

**Ask:** "What type of feature are you building?" (use the AskUserQuestion tool)

Present these options:
1. **Walking skeleton** - Bootstrap a new project with a minimal end-to-end feature that proves the architecture works. Creates project documentation (.claude/docs/) and a PRD.
2. **Capability feature** - Add a backend-focused feature (APIs, data models, business logic) to an existing project. Creates a PRD only.

If the user's request already makes the type obvious (e.g., "bootstrap a new project" → walking skeleton, "add a user profile API" → capability), skip the question, confirm your assumption with the user and proceed to the appropriate workflow.

## Workflow Dispatch

Based on the user's selection:

### Walking Skeleton
Read and follow `workflows/walking-skeleton.md`

This workflow:
- Guides through architecture decisions conversationally
- Creates project documentation structure
- Generates PRD at `docs/features/001-walking-skeleton/PRD.md`
- Generates all `.claude/docs/` files

### Capability Feature
Read and follow `workflows/capability.md`

This workflow:
- Gathers context about the feature
- Works through technical design (data models, APIs, business logic)
- Generates PRD at `docs/features/{number}-{slug}/PRD.md`

## Adding New Feature Types

To add a new feature type:
1. Create `workflows/{type}.md` with the full workflow
2. Add the option to the entry point question above
3. Add dispatch logic to route to the new workflow

Future feature types might include:
- **UI feature** - Frontend-focused features emphasizing UX
- **Integration** - Third-party API integrations, webhooks
- **Migration** - Data migrations, system upgrades

## Shared Resources

- `references/prd-template.md` - Standard PRD structure used by all workflows
- `references/checklist.md` - Architecture checklist for walking skeletons
- `assets/templates/` - Documentation templates for walking skeletons
