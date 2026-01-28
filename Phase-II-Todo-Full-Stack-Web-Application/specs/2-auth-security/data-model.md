# Data Model: Authentication & Security

## Overview
This document defines the data models for the JWT-based authentication and security system. It extends the existing user model to support authentication and security features while maintaining the existing functionality.

## Entity Extensions

### User Entity (Extended)
**Description**: Represents an authenticated user in the system with additional authentication fields

**Additional Fields** (beyond the basic User model):
- `hashed_password`: String - BCrypt hashed password
- `is_active`: Boolean (Default: True) - Whether the user account is active
- `created_at`: DateTime - Timestamp when the user account was created
- `updated_at`: DateTime - Timestamp when the user account was last updated

**Authentication-specific Methods**:
- `verify_password(plain_password: str) -> bool` - Verify plaintext password against hash
- `get_auth_data() -> dict` - Get authentication data for JWT creation

**Validation Rules**:
- Email must be a valid email format
- Email must be unique across all users
- Password must meet minimum security requirements

**Relationships**:
- One-to-Many: User has many Tasks
- One-to-Many: User has many AuthSessions (if implementing session tracking)

## JWT Token Structure

### JWT Payload
**Description**: The structure of the JWT token payload that will be used for authentication

**Fields**:
- `sub`: String (Subject) - User ID as a string
- `email`: String - User's email address
- `exp`: Integer - Expiration timestamp (Unix timestamp)
- `iat`: Integer - Issued at timestamp (Unix timestamp)
- `jti`: String (Optional) - JWT ID for token tracking (if implementing revocation)

**Token Characteristics**:
- Algorithm: HS256 (HMAC with SHA-256)
- Expiration: 30 minutes from issue time (configurable)
- Claims: Minimal necessary information to avoid token bloat

## Authentication Session (Optional - for advanced tracking)
**Description**: Tracks active authentication sessions (not required for basic JWT implementation)

**Fields**:
- `id`: UUID (Primary Key) - Unique identifier for the session
- `user_id`: UUID (Foreign Key) - Reference to the user
- `token_hash`: String - Hash of the JWT token (for revocation)
- `expires_at`: DateTime - When the session expires
- `created_at`: DateTime - When the session was created
- `last_accessed_at`: DateTime - When the session was last used

**Note**: This is optional for the basic implementation since JWTs are stateless. Session tracking would be needed for features like "logout all devices".

## Security-Related Constants

### Token Configuration
- **Secret Key**: Stored in environment variable `BETTER_AUTH_SECRET`
- **Algorithm**: HS256 (can be upgraded to RS256 for production)
- **Expiration Time**: 30 minutes (configurable)
- **Refresh Threshold**: 5 minutes before expiration (if refresh is implemented)

### Error Responses
**Unauthorized (401) Scenarios**:
- Missing Authorization header
- Invalid Bearer token format
- Malformed JWT
- Invalid signature
- Expired token
- Revoked token (if using blacklisting)

**Forbidden (403) Scenarios**:
- Valid token but attempting to access another user's data
- Insufficient permissions for requested action

## API Representation

### Authentication Response
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

### User Profile Response (for authenticated users)
```json
{
  "id": "uuid-string",
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "is_active": true,
  "created_at": "2023-01-01T00:00:00Z"
}
```

## Security Considerations

### Data Integrity Rules
- All authentication requests must validate email format
- Passwords must be properly hashed before storage
- JWT tokens must be verified using the shared secret
- All user data access must be filtered by the authenticated user

### Access Control
- Unauthenticated requests should return 401 Unauthorized
- Requests for data not owned by the authenticated user should return 403 Forbidden
- Invalid JWT tokens should result in 401 Unauthorized responses
- Token refresh should be limited to prevent abuse

### Token Management
- Tokens should have appropriate expiration times
- Consider implementing token blacklisting for logout functionality
- Use HTTPS in production to protect token transmission
- Avoid storing sensitive information in JWT payloads

This data model extends the existing user model to support the authentication and security requirements while maintaining all previous functionality. The JWT-based approach ensures stateless authentication that scales well with the application.