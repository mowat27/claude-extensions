# Fidelity Dial

Single 1-10 scale controlling depth of finish for generated tasks.

## Levels

| Level | Name | Include | Exclude |
|-------|------|---------|---------|
| 1-2 | **Skeleton** | Happy path only, minimal UI, data flows work | Error states, loading states, validation feedback, any polish |
| 3-4 | **Rough** | Basic error handling, simple loading indicators | Edge cases, animations, detailed validation, accessibility |
| 5-6 | **Functional** | Common error cases, form validation, responsive basics | Micro-interactions, complex animations, rare edge cases |
| 7-8 | **Solid** | Edge cases, accessibility basics, thoughtful UX | Animation polish, performance optimization, comprehensive a11y |
| 9-10 | **Polished** | Full accessibility, animations, micro-interactions, all edge cases | Nothing - full production quality |

## How It Affects Task Generation

At each level, tasks should:

### Level 1-2 (Skeleton)
- Focus on data flow and integration
- UI can be unstyled or minimal
- Skip loading/error states entirely
- "Does it work?" is the only question

### Level 3-4 (Rough)
- Add basic user feedback (something happened)
- Simple error messages (not styled, not contextual)
- Loading states can be a simple spinner or text

### Level 5-6 (Functional)
- Error messages are helpful and positioned correctly
- Form validation with inline feedback
- Responsive layout works on mobile
- Loading states feel intentional

### Level 7-8 (Solid)
- Handle edge cases users might actually hit
- Keyboard navigation works
- Screen reader basics in place
- Empty states, error recovery options

### Level 9-10 (Polished)
- Animations and transitions feel smooth
- Micro-interactions provide delight
- Performance optimized
- Comprehensive accessibility
- Every edge case handled gracefully
