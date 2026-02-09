<!-- SYNC IMPACT REPORT:
Version change: 2.0.0 → 3.0.0
Added sections: Event-driven architecture, Kafka integration, Dapr distributed runtime, Advanced task features, Cloud deployment, Modularity and scalability, Comprehensive testing, Dapr secrets management
Removed sections: None
Modified principles: Spec-driven (expanded for advanced features), Security-first (updated for Dapr/Kafka context), Data Integrity (enhanced for distributed systems), Code Quality (updated standards), Error Handling (enhanced for distributed systems), Technology Stack (updated with Kafka/Dapr), Success Criteria (updated for advanced features)
Templates requiring updates: ✅ .specify/templates/plan-template.md, ✅ .specify/templates/spec-template.md, ✅ .specify/templates/tasks-template.md, ⚠ .specify/templates/commands/sp.constitution.md
Follow-up TODOs: None
-->
# Advanced AI-Powered Todo Chatbot Constitution - Phase V

## Core Principles

### Correctness
All features must match the defined requirements exactly. Implementation must fulfill specifications without deviation or assumption. Ensures reliable, predictable behavior that meets user expectations for advanced features like Recurring Tasks, Due Dates & Reminders, Priorities, Tags, Search, Filter, Sort.

### Security-first
Authentication, authorization, and data isolation are mandatory. Every access point must enforce proper security controls. Protects user data and system integrity from unauthorized access, especially in AI-driven interactions where user context must be preserved. Must handle secrets via Dapr, validate inputs, and use secure connections in distributed environments.

### Spec-driven
All development must follow Spec-Kit Plus and Claude Code workflows. Every feature begins with a specification before implementation. Ensures consistent, well-planned development that aligns with project goals. All AI agent behaviors and MCP tool definitions must be specified before implementation. All features must directly map to specified requirements.

### Simplicity
Prefer clear, maintainable solutions over clever but complex ones. Code should be readable and understandable by team members. Reduces maintenance burden and improves long-term sustainability while maintaining modularity and scalability through event-driven architecture.

### Reliability
System must behave consistently across frontend, backend, AI agent, Kafka, and Dapr components. All components should work together seamlessly without unexpected failures. Provides stable user experience and reduces operational issues with comprehensive testing and error handling in distributed systems.

### API Design Standard
Fully RESTful, predictable endpoints, proper HTTP status codes. All API endpoints must follow REST conventions and return appropriate status codes. Enables predictable client-server interactions and standard error handling across the distributed runtime.

### Data Integrity
All task operations must enforce user ownership. Every task operation must verify the user has rights to perform the action. With AI agents executing operations, all database actions must be properly attributed to the authenticated user and maintain data consistency across distributed systems with Dapr state management.

### Agent-first Design
AI agents must orchestrate all task operations through MCP tools. Direct database access by agents is prohibited. All task actions must be executed only via MCP tools following the clear separation: UI → Agent → MCP Tools → Database. Ensures centralized control and auditability of all operations in the distributed system.

### Event-driven Architecture
All asynchronous operations must be handled through Kafka event streams. Real-time communications, reminders, recurring task triggers, and audit logs must use Kafka for decoupled, scalable processing. Enables reliable event processing and supports advanced features like real-time sync and automated reminders.

### Modularity and Scalability
Components must be designed with clear separation of concerns and minimal coupling. Services should scale independently based on demand. Dapr components (Pub/Sub, State, Bindings, Secrets, Service Invocation) must be leveraged to create resilient, scalable microservices that maintain separation of business logic from infrastructure concerns.

## Key Standards

### Auth Standard
JWT-based authentication using Better Auth + FastAPI. Authentication tokens must be validated using shared secrets. Ensures secure, stateless authentication across the application stack, including AI agent requests and Dapr service invocations.

### AI Agent Standard
OpenAI Agents SDK must be used for all AI functionality. Conversations must be stateless with context rebuilt from database each request. All AI actions must be traceable and persisted for auditability in distributed environments.

### MCP Tools Standard
All MCP tools must be stateless and schema-defined. Each tool must have a clear, documented interface that follows consistent patterns. Tools must be reusable and composable for various AI agent workflows and distributed operations.

### Code Quality
Lint-free, type-safe where applicable, readable structure. All code must follow PEP 8 for Python, ESLint for JavaScript; include type hints and comments. Maintains high code quality and reduces runtime errors in complex distributed systems.

### Error Handling
Meaningful errors, no silent failures. All errors must be properly logged and communicated to clients. Distributed tracing and centralized logging must be implemented across Kafka, Dapr, and all services. Ensures proper debugging capability and user feedback, especially important for AI agent interactions and distributed system operations.

### Testing Standards
Minimum 80% unit test coverage; include integration tests for Kafka/Dapr flows. Testing must cover distributed system scenarios including service invocation, pub/sub messaging, state management, and bindings. All advanced features must have comprehensive test coverage to ensure reliability.

### Documentation Standard
Inline comments, README updates, and architecture diagrams. Documentation must include distributed system architecture, Kafka topic flows, Dapr component configurations, and API specifications for all services.

## Constraints

### Technology Stack
- Frontend: Next.js 16+ (App Router)
- Backend: Python FastAPI
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth with JWT
- AI Agent: OpenAI Agents SDK
- MCP Tools: Official MCP SDK
- Message Queue: Kafka (via Redpanda Cloud)
- Distributed Runtime: Dapr (Pub/Sub, State, Bindings, Secrets, Service Invocation)
All implementations must use these specified technologies. Ensures consistent tech stack and interoperability in distributed environment.

### Authentication Requirement
All endpoints require valid JWT token after auth integration. Any request without a valid token must be rejected. Maintains security posture across the entire API surface, including AI agent requests and Dapr service invocations.

### Advanced Features Constraint
All features must directly map to specified requirements: Recurring Tasks, Due Dates & Reminders, Priorities, Tags, Search, Filter, Sort. No additional features beyond those specified may be implemented without explicit approval.

### Distributed Systems Constraint
- Kafka must be used for all event-driven patterns and asynchronous operations
- Dapr components must be used for all distributed runtime capabilities
- Direct service-to-service communication should be avoided in favor of Dapr service invocation
- State management must use Dapr state stores
- Secret management must use Dapr secret stores

### Compatibility Constraint
Ensure backward compatibility with Phases I-IV. All new features and architectural changes must not break existing functionality for users of the previous phases.

## Security Rules

### JWT Token Requirement
No request without JWT token is allowed (401 Unauthorized). Every API request must include a valid JWT token in the Authorization header. Applies to both direct client requests, AI agent requests, and Dapr service invocations. Prevents unauthorized access to protected resources.

### JWT Verification
JWT must be verified using shared secret (BETTER_AUTH_SECRET). Tokens must be cryptographically validated before processing requests. Ensures token authenticity and prevents tampering in AI agent interactions and distributed system operations.

### User Identification
Backend must extract user from token, never trust client user_id. User identity must come from verified JWT claims, not client-provided data. Applies to AI agent requests where the user context must be preserved. Prevents privilege escalation and identity spoofing in distributed systems.

### Query Filtering
Every DB query must be filtered by authenticated user. All database operations must include user-specific filters. Even when executed by AI agents via MCP tools or through Dapr bindings, all queries must respect user boundaries. Maintains data isolation between users in distributed environments.

### Token Expiration
Tokens must support expiration and proper refresh mechanisms. JWTs must include expiration times and be validated accordingly. Prevents long-lived access tokens from becoming security risks.

### Agent Authorization
AI agents must validate user permissions before executing MCP tools. Every tool invocation must verify the authenticated user has rights to perform the action. Prevents unauthorized operations through AI agents.

### Dapr Secrets Management
All sensitive information must be stored and accessed through Dapr secret stores. Applications must never hardcode secrets or store them in configuration files. Dapr components must handle secret retrieval and distribution securely.

### Secure Communication
All communication between services must use secure connections. Dapr service invocation must enforce mTLS. Communication with Kafka must use SSL/TLS encryption.

## Constraints on Behavior

### User Task Access
Users can only see their own tasks. Task retrieval queries must be filtered by the authenticated user. Applies to both direct requests and AI agent-mediated requests through Dapr service invocations. Maintains privacy and data separation between users.

### User Task Modification
Users can only modify/delete their own tasks. Any modification request must verify user ownership of the target task. Even when executed by AI agents, through Kafka events, or via Dapr bindings, all modifications must respect user ownership. Prevents unauthorized data manipulation.

### Access Control
Invalid access attempts must return 403 Forbidden. Requests for resources the user doesn't own must return appropriate error codes. Provides clear feedback for unauthorized access attempts, including those made through AI agents, Kafka consumers, or Dapr service invocations.

### Token Validation
Missing/invalid tokens must return 401 Unauthorized. Requests without valid tokens must be rejected with appropriate status codes. Ensures proper authentication enforcement for all interaction types including distributed system communications.

### MCP Tool Execution
All task operations must be executed only via MCP tools. Direct database modifications are prohibited. All actions taken by AI agents must route through properly defined MCP tools to ensure consistency and auditability in distributed environments.

## Success Criteria

### End-to-End Functionality
All advanced-level task features work end-to-end. All required functionality must be implemented and tested across the full distributed stack. Validates that the system meets functional requirements for Recurring Tasks, Due Dates & Reminders, Priorities, Tags, Search, Filter, Sort.

### Multi-User Isolation
Multi-user isolation is enforced everywhere. Each user can only access their own data regardless of request method. Includes AI agent-mediated requests and distributed system operations. Ensures proper security and privacy implementation across all services.

### JWT Authentication
JWT auth works between Next.js, FastAPI, AI agents, Kafka, and Dapr components. Authentication tokens must be properly issued, transmitted, and validated across all application layers. Enables secure communication between frontend, backend, AI components, and distributed services.

### Data Protection
No user can access another user's data. Comprehensive checks prevent cross-user data access through any endpoint, AI agent interaction, Kafka event, or Dapr service invocation. Validates security implementation effectiveness in distributed environment.

### Database Integration
System runs using Neon DB with persistent storage. All data operations must work reliably with the Neon PostgreSQL database across distributed services. Ensures proper data persistence and retrieval for all components including AI agents and Kafka consumers.

### Security Testing
Passes manual security testing for auth and ownership checks. System must withstand testing for authentication bypasses and data access violations, including AI agent bypass attempts, Kafka consumer attacks, and Dapr service invocation bypasses. Validates security implementation completeness in distributed system.

### AI Agent Functionality
Users manage todos via natural language. Agent correctly invokes MCP tools based on user requests. Conversations resume after restart. System remains secure and stateless while providing intelligent task management for advanced features.

### Conversation Persistence
Conversations and messages are persisted in Neon PostgreSQL. AI agents can reconstruct conversation context from stored data. System maintains conversation continuity across restarts in distributed environment.

### Event-driven Operations
Kafka handles all asynchronous operations reliably. Reminders, recurring tasks, and audit logs are processed through Kafka topics without loss. Validates that event-driven patterns work correctly in production scenarios.

### Dapr Integration
Dapr components work correctly for Pub/Sub, State management, Bindings, Secrets, and Service Invocation. All distributed runtime capabilities function as expected both locally and in cloud deployments. Validates that Dapr integration meets requirements.

### Cloud Deployment
Services deploy successfully to cloud environments with Dapr and Kafka integration. Applications maintain functionality and performance characteristics in cloud deployments. Validates that cloud deployment meets requirements.

### Advanced Features Complete
All advanced features (Recurring Tasks, Due Dates & Reminders, Priorities, Tags, Search, Filter, Sort) are fully implemented and functional. Features work end-to-end with distributed system architecture and AI agent integration.

### Event-driven Flows Verified
Distributed flows (reminders, recurring tasks, audit logs, real-time sync) verified via tests. All event-driven patterns function correctly with Kafka and Dapr components. Validates reliability of advanced feature flows.

### Zero Critical Bugs
Zero critical bugs in feature implementations. System passes comprehensive testing with no blocking issues. Ensures production readiness of all advanced features.

### Local and Cloud Deployability
Dapr-integrated services deployable locally and to cloud without errors. Both development and production deployments work without configuration issues. Validates deployment pipeline robustness.

### End-to-End Demo Success
Complete end-to-end demo scenario works: Create task with due date, trigger reminder, complete recurring task, observe real-time sync. All advanced features function together in demonstration scenario.

## Governance

All development must comply with these constitutional principles. Any deviation requires explicit amendment to this document with justification. All pull requests and code reviews must verify adherence to these principles. The constitution supersedes all other practices and guidelines in case of conflict.

**Version**: 3.0.0 | **Ratified**: 2026-01-19 | **Last Amended**: 2026-02-09