---
name: ralph-context-builder
description: Build context documentation for a task before implementation. Use when user asks to build/assemble/gather context, prepare docs for a task, get context for implementation, or set up context for an agent/builder. Reads task definition and gathers relevant docs (WHAT to build, not HOW).
---

# Context Builder

Assemble context from project docs for a Ralph task.

## Input

- **Task object** - From task-chooser (slug, type, description, acceptance_criteria)
- **feature_folder** - Relative path to feature docs (e.g., `docs/features/skills-test`)
- **Project root** - Path to locate context docs

## Algorithm

### 1. Load Global Context

Read these from `<project_root>/`:
- `PRODUCT_STRATEGY.md` - Product vision
- `USER_JOURNEYS.md` - User workflows
- `DESIGN_SYSTEM.md` - Visual patterns
- `TECHNICAL_ARCHITECTURE.md` - Tech stack

### 2. Load Feature Context

If `feature_folder` provided, read from `<project_root>/<feature_folder>/`:
- `PRD.md` - Requirements
- `TASKS.md` - Implementation steps
- `UX.md` - UI requirements

### 3. Context Selection by Task Type

| Type | Prioritize | Minimize |
|------|-----------|----------|
| `bug` | TECHNICAL_ARCHITECTURE, UX error handling | DESIGN_SYSTEM (unless UI bug) |
| `refactoring` | TECHNICAL_ARCHITECTURE | USER_JOURNEYS, DESIGN_SYSTEM |
| `enhancement` | All global + feature docs | None |

### 4. Build Reference Table

For each doc: check existence, extract first heading, note path.

## Output Format

```markdown
## Context

### Product Strategy
{Relevant excerpts from PRODUCT_STRATEGY.md}

### User Journey
{Relevant workflow from USER_JOURNEYS.md}

### Design System
{Applicable patterns from DESIGN_SYSTEM.md}

### Technical Architecture
{Relevant tech from TECHNICAL_ARCHITECTURE.md}

### Feature: {feature_folder}
{Feature-specific docs if available}

## Reference Table

| File | Description |
|------|-------------|
| PRODUCT_STRATEGY.md | Product vision |
| {feature_folder}/PRD.md | Feature requirements |
```

## Edge Cases

| Scenario | Action |
|----------|--------|
| Global doc missing | Note "Not found" in Reference Table |
| feature_folder not provided | Skip feature section |
| Feature folder path invalid | Note "Not found" in Reference Table |
| Large docs | Extract sections matching task keywords |
