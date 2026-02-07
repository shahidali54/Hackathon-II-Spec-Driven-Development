---
name: database-schema-design
description: Design relational database schemas, create tables, and manage migrations. Use for backend and data-driven applications.
---

# Database Schema & Migrations

## Instructions

1. **Schema design**
   - Identify entities and relationships
   - Normalize data (avoid duplication)
   - Define primary and foreign keys

2. **Table creation**
   - Use clear, consistent naming
   - Choose appropriate data types
   - Add constraints (NOT NULL, UNIQUE, CHECK)

3. **Migrations**
   - Create versioned migration files
   - Support up and down (rollback) operations
   - Apply migrations incrementally

4. **Indexes & performance**
   - Add indexes for frequently queried columns
   - Avoid over-indexing
   - Optimize for read/write balance

## Best Practices
- Use snake_case for table and column names
- Keep tables focused on a single responsibility
- Always use migrations instead of manual DB changes
- Document schema decisions
- Test migrations on staging before production

## Example Structure
```sql
-- users table
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- posts table
CREATE TABLE posts (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
  title VARCHAR(200) NOT NULL,
  body TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
