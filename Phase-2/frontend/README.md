# Full-Stack Todo App - Frontend

This is the frontend for a full-stack Todo application built with Next.js 16+ using the App Router. The application provides a modern, responsive interface for managing personal tasks with secure user authentication.

## Features

- **Authentication System**: Secure user registration and login using JWT tokens
- **Dashboard Interface**: Personalized task management dashboard
- **Task Management**: Create, read, update, and delete tasks
- **Task Completion**: Toggle task completion status
- **Protected Routes**: Middleware to protect authenticated routes
- **Responsive Design**: Mobile-first responsive interface
- **Modern UI**: Built with Tailwind CSS and React components

## Tech Stack

- **Framework**: Next.js 16+ (App Router)
- **Runtime**: Node.js
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **Authentication**: Better Auth with JWT tokens
- **State Management**: React Hook Form
- **Database**: Connected to Neon PostgreSQL via backend API

## Project Structure

```
frontend/
├── app/
│   ├── auth/           # Authentication pages (signin, signup)
│   ├── dashboard/      # Protected dashboard with task management
│   ├── layout.tsx      # Root layout
│   ├── page.tsx        # Landing page
│   └── ...             # Other route handlers
├── components/         # Reusable UI components
├── hooks/              # Custom React hooks
├── lib/                # Utility functions
├── middleware.ts       # Route protection middleware
└── ...
```

## Getting Started

First, ensure you have the backend server running (port 8000). Then run the frontend development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the application.

## Authentication Flow

1. Users can register or login via the auth pages
2. Upon successful authentication, JWT tokens are stored securely
3. Protected routes (like /dashboard) require valid authentication
4. Middleware automatically redirects unauthenticated users to login

## Environment Variables

Create a `.env.local` file with the following variables:
- `NEXT_PUBLIC_API_URL` - Base URL for the backend API
- `NEXTAUTH_SECRET` - Secret for JWT token signing

## Learn More

This application is part of a hackathon project created using spec-driven-development methodology as part of Hackathon-II-Phase-II.
