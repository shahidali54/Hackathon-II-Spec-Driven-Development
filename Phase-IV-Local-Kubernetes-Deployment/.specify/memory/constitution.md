<!-- SYNC IMPACT REPORT:
Version change: 1.0.0 → 2.0.0
Added sections: Agent-first design, MCP tools integration, Stateless architecture, AI-powered interactions, Conversation persistence
Removed sections: None
Modified principles: Spec-driven (expanded), Security-first (updated for AI context), Data Integrity (enhanced for agent context)
Templates requiring updates: ✅ .specify/templates/plan-template.md, ✅ .specify/templates/spec-template.md, ✅ .specify/templates/tasks-template.md, ⚠ .specify/templates/commands/sp.constitution.md
Follow-up TODOs: None
-->
# AI-Powered Todo Chatbot Constitution

## Core Principles

### Correctness
All features must match the defined requirements exactly. Implementation must fulfill specifications without deviation or assumption. Ensures reliable, predictable behavior that meets user expectations.

### Security-first
Authentication, authorization, and data isolation are mandatory. Every access point must enforce proper security controls. Protects user data and system integrity from unauthorized access, especially in AI-driven interactions where user context must be preserved.

### Spec-driven
All development must follow Spec-Kit Plus and Claude Code workflows. Every feature begins with a specification before implementation. Ensures consistent, well-planned development that aligns with project goals. All AI agent behaviors and MCP tool definitions must be specified before implementation.

### Simplicity
Prefer clear, maintainable solutions over clever but complex ones. Code should be readable and understandable by team members. Reduces maintenance burden and improves long-term sustainability.

### Reliability
System must behave consistently across frontend, backend, and AI agent. All components should work together seamlessly without unexpected failures. Provides stable user experience and reduces operational issues.

### API Design Standard
Fully RESTful, predictable endpoints, proper HTTP status codes. All API endpoints must follow REST conventions and return appropriate status codes. Enables predictable client-server interactions and standard error handling.

### Data Integrity
All task operations must enforce user ownership. Every task operation must verify the user has rights to perform the action. With AI agents executing operations, all database actions must be properly attributed to the authenticated user and maintain data consistency.

### Agent-first Design
AI agents must orchestrate all task operations through MCP tools. Direct database access by agents is prohibited. All task actions must be executed only via MCP tools following the clear separation: UI → Agent → MCP Tools → Database. Ensures centralized control and auditability of all operations.

## Key Standards

### Auth Standard
JWT-based authentication using Better Auth + FastAPI. Authentication tokens must be validated using shared secrets. Ensures secure, stateless authentication across the application stack, including AI agent requests.

### AI Agent Standard
OpenAI Agents SDK must be used for all AI functionality. Conversations must be stateless with context rebuilt from database each request. All AI actions must be traceable and persisted for auditability.

### MCP Tools Standard
All MCP tools must be stateless and schema-defined. Each tool must have a clear, documented interface that follows consistent patterns. Tools must be reusable and composable for various AI agent workflows.

### Code Quality
Lint-free, type-safe where applicable, readable structure. All code must pass linting checks and use appropriate typing. Maintains high code quality and reduces runtime errors.

### Error Handling
Meaningful errors, no silent failures. All errors must be properly logged and communicated to clients. Ensures proper debugging capability and user feedback, especially important for AI agent interactions.

## Constraints

### Technology Stack
- Frontend: Next.js 16+ (App Router)
- Backend: Python FastAPI
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth with JWT
- AI Agent: OpenAI Agents SDK
- MCP Tools: Official MCP SDK
All implementations must use these specified technologies. Ensures consistent tech stack and interoperability.

### Authentication Requirement
All endpoints require valid JWT token after auth integration. Any request without a valid token must be rejected. Maintains security posture across the entire API surface, including AI agent requests.

### Agent Constraints
- Agents must not access the database directly
- MCP tools must be stateless and schema-defined
- Conversation context must be rebuilt from database each request
- All AI actions must be traceable and persisted
- Phase-II auth and user isolation rules remain enforced

## Security Rules

### JWT Token Requirement
No request without JWT token is allowed (401 Unauthorized). Every API request must include a valid JWT token in the Authorization header. Applies to both direct client requests and AI agent requests. Prevents unauthorized access to protected resources.

### JWT Verification
JWT must be verified using shared secret (BETTER_AUTH_SECRET). Tokens must be cryptographically validated before processing requests. Ensures token authenticity and prevents tampering in AI agent interactions.

### User Identification
Backend must extract user from token, never trust client user_id. User identity must come from verified JWT claims, not client-provided data. Applies to AI agent requests where the user context must be preserved. Prevents privilege escalation and identity spoofing.

### Query Filtering
Every DB query must be filtered by authenticated user. All database operations must include user-specific filters. Even when executed by AI agents via MCP tools, all queries must respect user boundaries. Maintains data isolation between users.

### Token Expiration
Tokens must support expiration and proper refresh mechanisms. JWTs must include expiration times and be validated accordingly. Prevents long-lived access tokens from becoming security risks.

### Agent Authorization
AI agents must validate user permissions before executing MCP tools. Every tool invocation must verify the authenticated user has rights to perform the action. Prevents unauthorized operations through AI agents.

## Constraints on Behavior

### User Task Access
Users can only see their own tasks. Task retrieval queries must be filtered by the authenticated user. Applies to both direct requests and AI agent-mediated requests. Maintains privacy and data separation between users.

### User Task Modification
Users can only modify/delete their own tasks. Any modification request must verify user ownership of the target task. Even when executed by AI agents, all modifications must respect user ownership. Prevents unauthorized data manipulation.

### Access Control
Invalid access attempts must return 403 Forbidden. Requests for resources the user doesn't own must return appropriate error codes. Provides clear feedback for unauthorized access attempts, including those made through AI agents.

### Token Validation
Missing/invalid tokens must return 401 Unauthorized. Requests without valid tokens must be rejected with appropriate status codes. Ensures proper authentication enforcement for all interaction types.

### MCP Tool Execution
All task operations must be executed only via MCP tools. Direct database modifications are prohibited. All actions taken by AI agents must route through properly defined MCP tools to ensure consistency and auditability.

## Success Criteria

### End-to-End Functionality
All basic-level task features work end-to-end. All required functionality must be implemented and tested across the full stack. Validates that the system meets functional requirements.

### Multi-User Isolation
Multi-user isolation is enforced everywhere. Each user can only access their own data regardless of request method. Includes AI agent-mediated requests. Ensures proper security and privacy implementation.

### JWT Authentication
JWT auth works between Next.js, FastAPI, and AI agents. Authentication tokens must be properly issued, transmitted, and validated across all application layers. Enables secure communication between frontend, backend, and AI components.

### Data Protection
No user can access another user's data. Comprehensive checks prevent cross-user data access through any endpoint or AI agent interaction. Validates security implementation effectiveness.

### Database Integration
System runs using Neon DB with persistent storage. All data operations must work reliably with the Neon PostgreSQL database. Ensures proper data persistence and retrieval for all components including AI agents.

### Security Testing
Passes manual security testing for auth and ownership checks. System must withstand testing for authentication bypasses and data access violations, including AI agent bypass attempts. Validates security implementation completeness.

### AI Agent Functionality
Users manage todos via natural language. Agent correctly invokes MCP tools based on user requests. Conversations resume after restart. System remains secure and stateless while providing intelligent task management.

### Conversation Persistence
Conversations and messages are persisted in Neon PostgreSQL. AI agents can reconstruct conversation context from stored data. System maintains conversation continuity across restarts.

## Governance

All development must comply with these constitutional principles. Any deviation requires explicit amendment to this document with justification. All pull requests and code reviews must verify adherence to these principles. The constitution supersedes all other practices and guidelines in case of conflict.

**Version**: 2.0.0 | **Ratified**: 2026-01-19 | **Last Amended**: 2026-01-29