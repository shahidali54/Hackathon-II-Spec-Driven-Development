# Research: Todo Full-Stack Web Application

## Overview
This research document addresses the technical decisions and best practices for implementing the secure, multi-user todo web application with Next.js, FastAPI, SQLModel, and Better Auth.

## Phase 0: Technical Decisions

### 1. Authentication Approach
**Decision**: JWT-based authentication using Better Auth with FastAPI integration
**Rationale**: Better Auth provides a robust, well-maintained authentication solution that supports JWT tokens out of the box. It integrates seamlessly with Next.js and can be easily connected to FastAPI backend.
**Alternatives considered**:
- Custom JWT implementation: Would require significant development time and security expertise
- Other auth providers (Auth0, Firebase): Would add external dependencies and potential costs

### 2. Database Connection Pooling
**Decision**: Use SQLModel with connection pooling for Neon PostgreSQL
**Rationale**: SQLModel provides a clean integration with both SQLAlchemy and Pydantic, making it ideal for FastAPI applications. Neon's serverless nature works well with connection pooling strategies.
**Alternatives considered**:
- Raw asyncpg: Lower-level but less convenient for model management
- Peewee ORM: Less suitable for async FastAPI applications

### 3. API Endpoint Design
**Decision**: RESTful API with user-id parameter in URL path
**Rationale**: While the final implementation will extract user ID from JWT token, using user_id in the URL path maintains RESTful conventions and makes the API easier to understand during development.
**Implementation note**: The user_id in URL will be verified against the JWT token, not trusted as the source of truth.

### 4. Frontend Architecture
**Decision**: Next.js 16+ with App Router for server-client component organization
**Rationale**: Next.js App Router provides excellent performance, SEO benefits, and a clean architecture for full-stack applications. Better Auth integrates seamlessly with Next.js.
**Alternatives considered**:
- React + Vite: Would require additional setup for server-side rendering
- Traditional SPA frameworks: Would lack the SSR benefits of Next.js

### 5. Task Status Management
**Decision**: Boolean field for completion status with PATCH endpoint for toggling
**Rationale**: A simple boolean field is efficient and straightforward for tracking completion. The PATCH method is semantically correct for partial updates.
**Alternatives considered**:
- Separate status enum: Would be overengineering for a simple todo app
- Separate endpoints for complete/incomplete: Would create unnecessary API endpoints

## Best Practices Researched

### 1. JWT Security Best Practices
- Use strong secret keys (BETTER_AUTH_SECRET)
- Set appropriate token expiration times
- Implement proper token refresh mechanisms
- Validate tokens on every protected endpoint
- Never trust client-provided user IDs

### 2. SQL Injection Prevention
- Use parameterized queries through SQLModel
- Validate all input parameters
- Implement proper database transaction handling
- Use connection pooling safely

### 3. CORS Configuration
- Restrict origins appropriately
- Configure credentials handling for JWT cookies
- Set appropriate timeout and retry policies

### 4. Error Handling
- Use appropriate HTTP status codes (200, 201, 400, 401, 403, 404, 500)
- Provide meaningful error messages without exposing system details
- Log errors appropriately for debugging while protecting sensitive information

## Integration Patterns

### 1. Frontend-Backend Communication
- Use axios or fetch for API calls
- Include JWT tokens in Authorization header
- Implement proper error handling for network requests
- Handle token expiration gracefully

### 2. Database Transaction Management
- Use async context managers for database sessions
- Implement proper error handling and rollback mechanisms
- Ensure atomic operations for related data changes

### 3. User Session Management
- Store JWT tokens in httpOnly cookies when possible
- Implement token refresh mechanisms
- Handle session expiration gracefully

## Technology-Specific Findings

### Better Auth Integration
- Can be configured to work with Next.js App Router
- Supports custom JWT claims for user information
- Provides hooks for custom validation and middleware

### FastAPI + SQLModel
- Excellent type validation through Pydantic integration
- Automatic API documentation generation
- Async/await support for improved performance
- Built-in request validation and error handling

### Neon PostgreSQL
- Serverless scaling for cost efficiency
- PostgreSQL compatibility for familiar SQL syntax
- Connection pooling considerations for serverless environment
- Environment-specific configuration requirements

## Next Steps
With these technical decisions resolved, the implementation can proceed with confidence in the architectural choices. The next phase will focus on creating the data models, API contracts, and initial implementation tasks.