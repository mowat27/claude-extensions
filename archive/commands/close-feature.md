---
description: Close feature branch with doc updates, archive, and PR
allowed-tools: Read, Edit, Write, Glob, Grep, Bash(git:*), Bash(gh:*), Bash(mkdir:*), Bash(mv:*)
---

## Context

- Current branch: !`git branch --show-current`
- Main branch: main
- Recent commits on this branch: !`git log --oneline main..HEAD`

## Task: Close Feature Branch

You are closing out a feature branch. Follow these steps IN ORDER, stopping where indicated.

### Phase 1: Update Documentation (STOP AFTER)

1. **Analyze the feature branch** - Review commits, changed files, and understand what was built/discovered

2. **Update project memory and docs** with discoveries and new features:
   - Update `CLAUDE.md` if there are new patterns, commands, or project knowledge
   - Update `README.md` if there are user-facing features or setup changes
   - Update any other relevant documentation files

   **CRITICAL: Updates must be TERSE and TO THE POINT to prevent context bloat. Prefer bullet points and short phrases over prose. Sacrifice grammar for the sake of concision**

3. **STOP HERE** - Present the changes to the user for review. Say something like:
   > "I've updated the documentation. Please review the changes above and let me know if you want any adjustments before I commit."

Wait for user confirmation before proceeding.

### Phase 2: Commit Documentation (after user approval)

4. Commit the documentation changes with a conventional commit message (e.g., `docs: update CLAUDE.md with feature X learnings`)

### Phase 3: Archive PRD and Tasks

5. Find PRD and task files in `tasks/` that relate to this feature branch
6. Move them to `tasks/archive/` (create folder if needed)
7. Commit the archive with message like `chore: archive PRD and tasks for feature X`

### Phase 4: Create PR

8. Push branch and create PR using `gh pr create`:
   - Title should be descriptive of the feature
   - Body should summarize key changes with bullet points
   - Include link to any relevant issues

Return the PR URL when done.
