# Walking Skeleton Checklist

## The skeleton itself

- **Minimal feature:** What is the simplest end-to-end feature that exercises the full stack?
- **Happy path:** What's the flow? (e.g., user hits endpoint → DB read → LLM call → response)
- **Minimum entities:** What tables/models are needed for this feature?

## Core architectural decisions (cut across all stages)

- **Config & secrets management:** How do we handle environment variables, secrets, and config across dev/test/prod?
- **Environment definitions:** What environments exist? (dev/staging/prod?) How do we know which env we're in?
- **Docker strategy:** Are we containerizing? What's containerized? Same images across environments or different approaches?
- **Auth mechanism:** API key, JWT, session cookies, OAuth? Where does auth state live? User accounts or service-to-service?
- **Logging approach:** Where do logs go? What format? How to access in each environment?
- **Database provider:** What's our database?
- **External services:** Beyond DB/LLM - file storage? Email? Third-party APIs?
- **Stack & frameworks:** What frameworks? CSS approach? Component frameworks? Third-party libraries? Core libraries for logic?
- **Architecture pattern:** Monolithic MVC vs skinny frontend + APIs vs something in between?
- **Project structure:** Folder conventions? Monorepo or separate repos?
- **LLM provider setup:** Which provider(s)? How configured?

## Development stage decisions

- How do we run databases locally?
- How do we run application servers for development?
- Docker: docker-compose for local dev orchestration?

## Testing stage decisions

- How do we make isolated tests?
- What framework are we using for tests?
- How do we set up test databases?
- How do we set up test servers?
- Test-specific secrets/config handling?

## Code quality decisions

- Linting: What linter? (ESLint, Ruff, etc.) What ruleset?
- Type checking: How do we verify types? (tsc --noEmit, pyright, etc.)
- Combined check command: Single command to run all static analysis?
- Build integration: Do lint/typecheck run before build?

## CI/CD decisions

- What CI tool? (GitHub Actions, CircleCI, etc.)
- What checks run before deploy? (tests, linting, type checks)
- Manual or automatic deployment trigger?

## Deployment stage decisions

- Where are we deploying to?
- How do we deploy?
- What do we need to add to do a deployment?
- Docker: Container strategy for production? Image registry? Build in CI or locally?

## Verification

- Health check endpoints?
- How do we confirm it works post-deploy?
- Smoke tests in production?
