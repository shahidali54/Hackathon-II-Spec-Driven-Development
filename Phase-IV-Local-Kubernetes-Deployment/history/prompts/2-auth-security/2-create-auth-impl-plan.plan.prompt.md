---
id: 2
title: create-auth-impl-plan
stage: plan
date: 2026-01-19
surface: agent
model: Claude Sonnet 4.5
feature: 2-auth-security
branch: 2-auth-security
user: shahi
command: sp.plan
labels: ["plan", "auth", "security", "jwt", "better-auth"]
links:
  spec: ../specs/2-auth-security/spec.md
  plan: ../specs/2-auth-security/plan.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/2-auth-security/plan.md
  - specs/2-auth-security/research.md
  - specs/2-auth-security/data-model.md
  - specs/2-auth-security/quickstart.md
tests: []
---

## Prompt

Spec 2: Authentication & Security

Step 1 – Better Auth Setup (Frontend)
- Install and configure Better Auth in Next.js
- Enable JWT plugin
- Configure:
  - Signup flow
  - Signin flow
  - Session handling
- Set JWT secret from environment variable BETTER_AUTH_SECRET
- Verify JWT is generated on successful login

Deliverable:
- User can sign up and log in
- JWT token is created after login

---

Step 2 – Frontend API Client
- Build API client utility
- Read JWT from Better Auth session
- Attach token to every request:
  - Authorization: Bearer <token>
- Handle missing/expired token:
  - Redirect to login
  - Show auth error

Deliverable:
- All frontend API calls include JWT

---

Step 3 – FastAPI JWT Verification
- Add middleware or dependency:
  - Read Authorization header
  - Extract Bearer token
  - Verify signature using BETTER_AUTH_SECRET
  - Decode payload
- Handle errors:
  - Missing token → 401
  - Invalid token → 401
  - Expired token → 401

Deliverable:
- Backend can verify JWT and extract user info

---

Step 4 – Enforce User Ownership
- Remove trust in URL user_id parameter
- Use user ID from decoded JWT
- Update all queries:
  - Filter by authenticated user only
- On mismatch:
  - Return 403 Forbidden

Deliverable:
- Users can only access their own tasks

---

Step 5 – Security Testing
- Test:
  - No token → 401
  - Invalid token → 401
  - Expired token → 401
  - Access other user's task → 403
- Test normal flow:
  - Login → token issued → API works

Deliverable:
- Auth system passes manual security tests

Final Outcome:
- Stateless JWT-based authentication
- Secure integration between Next.js and FastAPI
- Strong user isolation enforced at API level
- Ready to plug into full-stack app

## Response snapshot

Successfully created a comprehensive implementation plan for the Authentication & Security feature. The plan includes:

1. Implementation Plan (plan.md): Outlined the technical context, project structure, and constitutional compliance verification for the JWT-based authentication system using Better Auth, Next.js, and FastAPI.

2. Research Document (research.md): Resolved technical decisions including Better Auth integration, JWT token strategy, token storage and transmission, backend JWT verification, and user identity extraction.

3. Data Model (data-model.md): Extended the existing User entity with authentication fields, defined JWT token structure, and outlined security-related constants and error responses.

4. Quickstart Guide (quickstart.md): Provided comprehensive setup instructions, implementation steps, security measures, API endpoint updates, and testing procedures for the authentication system.

All constitutional compliance checks passed, ensuring the implementation follows security-first principles, proper authentication, and user data isolation requirements. The plan is ready for the next phase of development with clear implementation steps for JWT-based authentication.

## Outcome

- ✅ Impact: Created comprehensive authentication implementation plan with all required artifacts
- 🧪 Tests: No tests created in planning phase
- 📁 Files: Created plan.md, research.md, data-model.md, and quickstart.md
- 🔁 Next prompts: Ready for task breakdown with /sp.tasks
- 🧠 Reflection: Plan addresses all aspects of authentication and security with proper security and architecture considerations.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Not applicable
- Prompt variant (if applicable): Implementation planning
- Next experiment (smallest change to try): Proceed to task breakdown phase