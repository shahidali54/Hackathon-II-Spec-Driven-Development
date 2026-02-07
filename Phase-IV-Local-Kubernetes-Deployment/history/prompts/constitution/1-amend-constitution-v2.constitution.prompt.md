---
id: 1
title: Amend Constitution V2
stage: constitution
date: 2026-01-29
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: shahi
command: /sp.constitution
labels: [constitution,update,ai-chatbot]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
---

## Prompt

(Phase-III Update)

Project Extension: AI-Powered Todo Chatbot

Core additions:
- Agent-first design using OpenAI Agents SDK
- Stateless chat and tool execution
- All task actions executed only via MCP tools
- Clear separation: UI → Agent → MCP Tools → Database

Key standards:
- Agents must not access the database directly
- MCP tools must be stateless and schema-defined
- Conversation context rebuilt from database each request
- All AI actions traceable and persisted
- Phase-II auth and user isolation rules remain enforced

Constraints:
- Use OpenAI Agents SDK and Official MCP SDK
- Stateless FastAPI chat endpoint
- Persist conversations and messages in Neon PostgreSQL
- No manual coding; Claude code only

Success criteria:
- Users manage todos via natural language
- Agent correctly invokes MCP tools
- Conversation resumes after restart
- System remains secure and stateless

## Response snapshot

Updated the project constitution to version 2.0.0 to incorporate the Phase-III requirements for the AI-Powered Todo Chatbot. The key changes include:

1. Added new principles:
   - Agent-first Design: AI agents must orchestrate all task operations through MCP tools

2. Enhanced existing principles to account for AI context:
   - Security-first: Updated to address AI-driven interactions
   - Data Integrity: Enhanced for agent context
   - Spec-driven: Expanded to include AI agent behaviors and MCP tool definitions

3. Added new standards:
   - AI Agent Standard: Using OpenAI Agents SDK with stateless conversations
   - MCP Tools Standard: Requiring stateless, schema-defined tools

4. Added new constraints specific to the AI agent functionality:
   - Prohibiting direct database access by agents
   - Requiring stateless MCP tools with schema definitions
   - Enforcing conversation context rebuilding from database

5. Updated security rules to cover AI agent interactions:
   - Agent Authorization: Requiring user permission validation before tool execution

6. Added success criteria for AI functionality:
   - AI Agent Functionality: Natural language task management
   - Conversation Persistence: Maintaining conversations across restarts

The constitution version was incremented from 1.0.0 to 2.0.0 to reflect the significant architectural changes introduced by the AI agent and MCP tools integration.

## Outcome

- ✅ Impact: Major update to constitution reflecting Phase-III AI agent integration
- 🧪 Tests: N/A (Documentation update)
- 📁 Files: Updated .specify/memory/constitution.md with new AI-focused principles
- 🔁 Next prompts: Implementation of AI agent and MCP tools according to new constitution
- 🧠 Reflection: Constitution now properly governs AI agent behavior and MCP tool usage

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin implementing AI agent according to new constitutional requirements