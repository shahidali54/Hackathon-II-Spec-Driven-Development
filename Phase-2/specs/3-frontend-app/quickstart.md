# Quickstart Guide: Frontend Web Application

## Overview
This guide provides essential information to get the Next.js frontend application up and running with Better Auth integration and secure API communication to the FastAPI backend.

## Prerequisites
- Node.js 18+ installed
- Access to the FastAPI backend server
- Understanding of the existing project structure
- Basic knowledge of Next.js App Router

## Setup Instructions

### 1. Initialize the Project
```bash
# Navigate to the frontend directory
cd frontend

# Install dependencies
npm install

# Install additional dependencies for this feature
npm install @types/react @types/node axios react-hook-form
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

### 2. Configure Environment Variables
```bash
# Create .env.local file in the frontend directory
touch .env.local
```

Add the following environment variables to `.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=your-super-secret-jwt-key-here
```

### 3. Configure Tailwind CSS
Update `tailwind.config.js`:
```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};
```

Update `src/styles/globals.css`:
```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

### 4. Project Structure Setup
Ensure the following directory structure exists:
```
frontend/
├── src/
│   ├── app/
│   │   ├── auth/
│   │   │   ├── signup/
│   │   │   │   └── page.tsx
│   │   │   ├── signin/
│   │   │   │   └── page.tsx
│   │   │   └── profile/
│   │   │       └── page.tsx
│   │   ├── dashboard/
│   │   │   └── page.tsx
│   │   ├── tasks/
│   │   │   ├── page.tsx
│   │   │   ├── create/
│   │   │   │   └── page.tsx
│   │   │   ├── [id]/
│   │   │   │   ├── page.tsx
│   │   │   │   └── edit/
│   │   │   │       └── page.tsx
│   │   │   └── complete/
│   │   │       └── page.tsx
│   │   └── protected/
│   ├── components/
│   │   ├── AuthGuard.tsx
│   │   ├── ProtectedRoute.tsx
│   │   ├── TaskCard.tsx
│   │   ├── TaskForm.tsx
│   │   ├── TaskList.tsx
│   │   ├── Navbar.tsx
│   │   └── Footer.tsx
│   ├── lib/
│   │   ├── auth.ts
│   │   ├── api.ts
│   │   └── types/
│   │       └── index.ts
│   ├── styles/
│   │   └── globals.css
│   └── hooks/
│       └── useAuth.ts
├── package.json
├── next.config.js
├── tailwind.config.js
└── tsconfig.json
```

## Key Implementation Steps

### 1. Authentication Setup
1. Create authentication utilities in `src/lib/auth.ts`
2. Implement API client with JWT handling in `src/lib/api.ts`
3. Create AuthGuard and ProtectedRoute components
4. Build signup and signin pages

### 2. API Client Implementation
1. Create centralized API client with Axios or Fetch
2. Implement request interceptors to attach JWT tokens
3. Handle 401 responses by redirecting to login
4. Implement proper error handling and loading states

### 3. Task Management UI
1. Create dashboard page to display user's tasks
2. Build task creation form
3. Implement task listing with filtering and sorting
4. Create task detail and edit pages
5. Add task completion toggle functionality

### 4. Responsive Design
1. Apply Tailwind CSS classes for responsive layouts
2. Test UI on mobile and desktop screen sizes
3. Implement loading and empty states
4. Add proper error messaging

## Running the Application

### Development
```bash
# Start the development server
npm run dev

# Application will be available at http://localhost:3000
```

### Production Build
```bash
# Build the application
npm run build

# Start the production server
npm start
```

## Testing the Application

### Manual Testing Steps
1. Visit the home page
2. Navigate to signup page and create a new account
3. Verify you're redirected to the dashboard after signup
4. Try creating a new task
5. Verify the task appears in the task list
6. Try editing and deleting tasks
7. Test the toggle completion functionality
8. Log out and verify you're redirected to login when accessing protected pages

### Common Issues and Solutions
1. **Authentication Issues**: Verify NEXTAUTH_SECRET matches between frontend and backend
2. **API Connection Issues**: Check that NEXT_PUBLIC_API_URL points to the correct backend server
3. **JWT Token Issues**: Ensure tokens are properly attached to requests
4. **CORS Issues**: Verify backend allows requests from frontend origin

## Environment Variables

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000  # URL of the FastAPI backend
NEXTAUTH_URL=http://localhost:3000        # URL of the Next.js frontend
NEXTAUTH_SECRET=your-super-secret-jwt-key-here  # Secret for JWT signing
```

## API Endpoints Used

### Authentication Endpoints
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user and return JWT
- `POST /api/auth/logout` - Logout user

### Task Management Endpoints
- `GET /api/tasks` - Get all tasks for authenticated user
- `POST /api/tasks` - Create a new task
- `GET /api/tasks/{id}` - Get specific task details
- `PUT /api/tasks/{id}` - Update task details
- `DELETE /api/tasks/{id}` - Delete a task
- `PATCH /api/tasks/{id}/complete` - Toggle task completion status

## Next Steps

1. Implement the authentication pages (signup, signin)
2. Create the API client with JWT handling
3. Build the dashboard and task management pages
4. Add responsive design and improve UX
5. Test the complete user flow
6. Optimize performance and accessibility
7. Add comprehensive error handling

This quickstart guide provides the essential setup instructions for developing the frontend web application. The application follows modern Next.js practices with proper authentication and secure API communication.