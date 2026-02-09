# Hackathon II: The Evolution of Todo – Mastering Spec-Driven Development & Cloud Native AI

## Project Title and Overview

This is a Spec-Driven Todo application evolving from a console app to a cloud-native AI-powered system. The project demonstrates the progression of software development practices, moving from simple command-line interfaces to sophisticated AI-integrated systems. Development is conducted using Claude Code and Spec-Kit Plus, showcasing modern AI-assisted development workflows.

## Hackathon Context

Hackathon II focuses on AI-native and spec-driven development methodologies. This project serves as a practical demonstration of how traditional applications can evolve into intelligent, cloud-native systems using AI tools and modern development practices. The project is implemented phase-by-phase, with each phase building upon the previous one to create increasingly sophisticated functionality.

## Project Progress

- ✅ **Phase I, Phase II, and Phase III** - Completed
- 🔄 **Phase IV and Phase V** - In progress / Pending

## Phase-by-Phase Description

### Phase I – In-Memory Python Console Todo App
Command-line todo app with add, update, delete, view, and mark complete features using spec-driven development.

### Phase II – Full-Stack Web Todo Application
Multi-user web app with Next.js frontend, FastAPI backend, PostgreSQL database, and authentication.

### Phase III – AI Todo Chatbot
AI chatbot interface using OpenAI Agents SDK and MCP server to manage todos conversationally.

### Phase IV – Kubernetes Deployment
Containerization and deployment on Minikube using Docker, Helm charts, and AI-assisted Kubernetes tools.

### Phase V – Advanced Cloud Deployment (Pending)
Advanced features, event-driven architecture with Kafka, Dapr integration, and deployment to DigitalOcean Kubernetes with CI/CD.

## Tech Stack Summary

Technologies used across phases include:
- **Frontend**: Next.js, React
- **Backend**: FastAPI, Python
- **Database**: PostgreSQL, SQLModel
- **AI Integration**: OpenAI Agents SDK, MCP Server
- **Authentication**: JWT, OAuth
- **Containerization**: Docker
- **Orchestration**: Kubernetes, Helm
- **Deployment**: Minikube, DigitalOcean
- **Development Tools**: Claude Code, Spec-Kit Plus

## Setup Instructions

### Backend Setup
1. Navigate to the backend directory
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables
4. Run the FastAPI server: `uvicorn main:app --reload`

### Frontend Setup
1. Navigate to the frontend directory
2. Install dependencies: `npm install`
3. Start the development server: `npm run dev`
4. Access the application at `http://localhost:3000`

## Repository Structure Overview

The repository is organized into several key directories:
- **`src/`** - Main source code files
- **`specs/`** - Specification documents and requirements
- **`frontend/`** - Next.js frontend application
- **`backend/`** - FastAPI backend services
- **`agents/`** - AI agent implementations and configurations
- **`docker/`** - Docker configurations and container definitions
- **`k8s/`** - Kubernetes manifests and Helm charts
- **`tests/`** - Unit and integration tests

---

*Part of Hackathon II: The Evolution of Todo – Mastering Spec-Driven Development & Cloud Native AI*
