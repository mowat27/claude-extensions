---
name: ralph-discovery
description: Orchestrate task selection and context gathering for development. Use when user asks to discover the next task, find what to work on, or prepare context from a features.json file. Combines ralph-task-chooser (task selection) and ralph-context-builder (context assembly) into a single workflow.
---

# Ralph Discovery

Orchestrate task discovery by invoking two skills in sequence and assembling their outputs.

## Workflow

### Step 1: Task Selection

Invoke the `ralph-task-chooser` skill:

```
/ralph-task-chooser <path-to-features.json>
```

Capture the JSON response verbatim.

### Step 2: Context Building

Invoke the `ralph-context-builder` skill with the path and selected task slug:

```
/ralph-context-builder <path-to-features.json> <task-slug>
```

Capture the markdown response verbatim.

### Step 3: Assemble Output

Return a markdown document in exactly this structure:

```markdown
# Context

<verbatim output from ralph-context-builder>

# Task

<verbatim JSON from ralph-task-chooser>
```

## Critical Rules

- Execute skills in order: task-chooser THEN context-builder
- Do NOT read features.json directly - let the skills do it
- Do NOT perform task selection yourself - use the skill
- Include skill outputs verbatim - do not summarize or interpret
- If a skill fails, report the error and stop
