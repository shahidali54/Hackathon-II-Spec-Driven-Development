---
name: backend-core
description: Design backend systems with clean routes, request/response handling, and database integration. Use for APIs and server-side applications.
---

# Backend Core Development

## Instructions

1. **Project structure**
   - Separate routes, controllers, and services
   - Use a clear entry point (e.g., `main.js` / `app.py`)
   - Keep configuration and environment variables isolated

2. **Routing**
   - Define RESTful routes (GET, POST, PUT, DELETE)
   - Group routes by resource
   - Use versioning for APIs (`/api/v1`)

3. **Request & Response Handling**
   - Validate incoming request data
   - Use consistent response formats (JSON)
   - Handle errors with proper HTTP status codes

4. **Database Connection**
   - Initialize DB connection at app startup
   - Use connection pooling
   - Abstract DB logic into repositories/services

5. **Error Handling & Middleware**
   - Global error handler
   - Logging middleware
   - Authentication & authorization middleware

## Best Practices
- Keep controllers thin, move logic to services
- Never expose sensitive data in responses
- Use async/await for non-blocking operations
- Validate inputs on every request
- Follow REST conventions consistently

## Example Structure

```text
src/
 ├─ main.js
 ├─ routes/
 │   └─ user.routes.js
 ├─ controllers/
 │   └─ user.controller.js
 ├─ services/
 │   └─ user.service.js
 └─ db/
     └─ connection.js
