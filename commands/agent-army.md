---
description: Run Craig, Eduard, Kevin in parallel for comprehensive analysis
allowed-tools: Task, Bash(git:*)
---

## Context

- Current branch: !`git branch --show-current`
- Changes on branch: !`git diff --stat main...HEAD 2>/dev/null || echo "No changes from main"`
- Recent commits: !`git log --oneline main..HEAD 2>/dev/null | head -10 || echo "No commits ahead of main"`

## Task: Launch Analysis Army

Spawn three analysis agents in parallel using the Task tool. Each agent analyzes the material provided by the user, or defaults to the current branch changes.

**CRITICAL**: If an agent has nothing relevant to analyze, it should return immediately with a brief note rather than forcing analysis on irrelevant material.

### Agent 1: Craig (Complexity/Overengineering)

Prompt:
```
Analyze for complexity and overengineering. Material: [user-provided OR current branch changes].

If there are no code changes or relevant material to analyze, respond with "No material to analyze" and stop.

Otherwise, run your full complexity analysis.
```

### Agent 2: Eduard (Logic, Consistency and Compliance)

Prompt:
```
Comprehensive review for logical flaws, standards compliance, pattern consistency. Material: [user-provided OR current branch changes].

If there are no changes or material to review, respond with "No material to review" and stop.

Otherwise, run your full review process with sub-agents.
```

### Agent 3: Kevin (Coupling Analysis)

Prompt:
```
Coupling assessment using connascence taxonomy. Material: [user-provided OR current branch code changes].

IMPORTANT: You only analyze CODE changes. If there are no code file changes (only docs, config, markdown, etc.), respond with "No code changes to analyze for coupling" and stop immediately.

Otherwise, run your full coupling analysis on the changed code.
```

## Execution

1. Determine what material to analyze:
   - If user provided specific material → use that
   - Otherwise → use current branch changes vs main

2. Launch all three agents in parallel using Task tool

3. Collect and present results as they complete

## Output

Present each agent's findings under clear headers:

```
## Craig (Complexity)
[findings]

## Eduard (Logic, Consistency)
[findings]

## Kevin (Coupling)
[findings]
```
