# PRD Template

This is the bare template structure for capability-focused PRDs. Match this structure exactly.

```markdown
# Feature: {FEATURE_NAME}

## Summary

## User Stories

## Acceptance Criteria

## Technical Notes

## Data Flow

## Dependencies
```

## Content Guidance

- **Summary**: 2-3 sentences describing what the feature does and why. Include route if applicable (e.g., `**Route:** /path`)
- **User Stories**: Format as "As a [role], I can [action] and [outcome]". Aim for 3-5 concrete stories.
- **Acceptance Criteria**: Testable checkboxes covering user actions, API endpoints, data persistence, edge cases, auth
- **Technical Notes**: Stack decisions, entities/tables with fields, API endpoints with purpose
- **Data Flow**: Simple ASCII diagram showing the main request/response flow
- **Dependencies**: External services, APIs, infrastructure needed
