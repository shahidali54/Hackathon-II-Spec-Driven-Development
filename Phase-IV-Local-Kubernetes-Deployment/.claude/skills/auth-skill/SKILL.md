---
name: auth-skill
description: Implement secure authentication systems including signup, signin, password hashing, JWT tokens, and Better Auth integration.
---

# Authentication Skill

## Instructions

1. **User Signup**
   - Accept email/username and password
   - Validate input (email format, password strength)
   - Hash password before storing
   - Prevent duplicate accounts

2. **User Signin**
   - Verify credentials securely
   - Compare hashed passwords
   - Return authentication response
   - Handle invalid login attempts safely

3. **Password Security**
   - Use strong hashing algorithms (bcrypt, argon2)
   - Apply salting automatically
   - Never store plain-text passwords
   - Support password reset flows

4. **JWT Authentication**
   - Generate access tokens on signin
   - Include user identifier in payload
   - Set expiration times
   - Verify tokens on protected routes

5. **Better Auth Integration**
   - Configure Better Auth provider
   - Use Better Auth APIs for sessions
   - Enable token-based authentication
   - Support social or email auth if required

## Best Practices
- Always hash passwords before storage
- Use HTTPS for all auth requests
- Short-lived access tokens
- Secure refresh token handling
- Centralized auth middleware
- Clear error messages without leaking security details

## Example Flow
```ts
// Signup
POST /auth/signup
→ validate input
→ hash password
→ save user
→ return success

// Signin
POST /auth/signin
→ verify password
→ generate JWT
→ return token

// Protected Route
GET /profile
→ verify JWT
→ return user data
