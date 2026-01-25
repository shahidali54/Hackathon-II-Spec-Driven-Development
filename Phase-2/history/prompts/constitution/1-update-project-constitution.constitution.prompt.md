---
id: 1
title: update-project-constitution
stage: constitution
date: 2026-01-19
surface: agent
model: Claude Sonnet 4.5
feature: none
branch: main
user: shahi
command: sp.constitution
labels: ["constitution", "setup", "security", "auth"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
  - .specify/templates/plan-template.md
  - .specify/templates/spec-template.md
  - .specify/templates/tasks-template.md
tests: []
---

## Prompt

Project: Todo Full-Stack Web Application (Hackathon Phase-2)

Core principles:
- Correctness: All features must match the defined requirements exactly
- Security-first: Authentication, authorization, and data isolation are mandatory
- Spec-driven: All development must follow Spec-Kit Plus and Claude Code workflows
- Simplicity: Prefer clear, maintainable solutions over clever but complex ones
- Reliability: System must behave consistently across frontend and backend

Key standards:
- API design: Fully RESTful, predictable endpoints, proper HTTP status codes
- Data integrity: All task operations must enforce user ownership
- Auth standard: JWT-based authentication using Better Auth + FastAPI
- Code quality: Lint-free, type-safe where applicable, readable structure
- Error handling: Meaningful errors, no silent failures

Constraints:
- Frontend: Next.js 16+ (App Router)
- Backend: Python FastAPI
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth with JWT
- Spec-driven workflow: Must use Claude Code + Spec-Kit Plus
- All endpoints require valid JWT token after auth integration

Security rules:
- No request without JWT token is allowed (401 Unauthorized)
- JWT must be verified using shared secret (BETTER_AUTH_SECRET)
- Backend must extract user from token, never trust client user_id
- Every DB query must be filtered by authenticated user
- Tokens must support expiration

Constraints on behavior:
- Users can only see their own tasks
- Users can only modify/delete their own tasks
- Invalid access attempts must return 403 Forbidden
- Missing/invalid tokens must return 401 Unauthorized

Success criteria:
- All basic-level task features work end-to-end
- Multi-user isolation is enforced everywhere
- JWT auth works between Next.js and FastAPI
- No user can access another user's data
- System runs using Neon DB with persistent storage
- Passes manual security testing for auth and ownership checks

## Response snapshot

Created and updated the project constitution file (.specify/memory/constitution.md) with all the specified principles, standards, constraints, security rules, and success criteria. Also updated the template files to incorporate constitutional compliance checks:

1. Updated plan-template.md to include constitutional compliance verification checklist
2. Updated spec-template.md to include functional requirements aligned with the constitution
3. Updated tasks-template.md to include foundational tasks that implement constitutional requirements

The constitution now serves as the governing document for the Todo Full-Stack Web Application project, establishing clear principles for correctness, security-first approach, spec-driven development, simplicity, and reliability.

## Outcome

- ✅ Impact: Created foundational constitution document and updated templates to reflect project principles
- 🧪 Tests: No tests created
- 📁 Files: Updated constitution.md and three template files
- 🔁 Next prompts: Continue with spec-driven development following the established constitution
- 🧠 Reflection: The constitution establishes clear boundaries and principles for the project, ensuring security and proper architecture from the start.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Not applicable
- Prompt variant (if applicable): Initial constitution setup
- Next experiment (smallest change to try): Begin creating feature specifications following the constitution