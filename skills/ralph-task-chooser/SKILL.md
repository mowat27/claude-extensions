---
name: ralph-task-chooser
description: Select which task to work on next from features.json. Use when user asks to choose/pick/select a task or feature, decide what to work on, find the next task, or prioritize work. Sorts by priority (bug > refactoring > enhancement).
---

# Task Chooser

Select the highest-priority eligible task from a features JSON file.

## Usage

Invoke with paths:
- `FEATURES_JSON` - Path to features.json (required)
- `PROGRESS_MD` - Path to progress markdown (optional, for history context)

## Algorithm

1. **Read** features.json and optionally progress.md
2. **Filter** eligible tasks: `passes: false`
3. **Sort** by priority:
   - `bug` (highest - fix broken things first)
   - `refactoring` (middle - clean before adding)
   - `enhancement` (lowest - new features last)
4. **Within same priority**: use judgment to select the highest-impact task (not necessarily first in list)
5. **Choose only one** task - never return multiple
6. **Return** result JSON

## Output Format

**Task found:**
```json
{
  "task": { /* full task object */ },
  "feature_folder": "docs/features/<feature-slug>",
  "rationale": "Bug: highest priority incomplete task"
}
```

`feature_folder` is the parent directory of FEATURES_JSON.

**Nothing to do:**
```json
{
  "task": null,
  "feature_folder": "docs/features/<feature-slug>",
  "reason": "All tasks complete"
}
```

## Expected features.json Structure

```json
[
  {
    "slug": "task-1",
    "type": "bug" | "refactoring" | "enhancement",
    "description": "string",
    "acceptance_criteria": ["string"],
    "passes": boolean
  }
]
```
