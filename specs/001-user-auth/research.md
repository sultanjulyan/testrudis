# Research & Decisions: User Authentication

**Status**: Completed
**Date**: 2026-01-14

## Unknowns & Clarifications

### 1. Flask + Prisma Integration
**Context**: Flask is synchronous by default (WSGI), Prisma Python client is Async (ASGI) focused but supports sync.
**Resolution**: Use `prisma-client-py`.
**Pattern**:
- Register Prisma client as a global extension or singleton.
- Ensure `await prisma.connect()` runs on startup.
- Use `async` route handlers if using Quart or `async` extra in Flask 2.0+, OR use the synchronous method of Prisma client if strictly WSGI.
- **Decision**: Use `async` Flask routes (available in Flask 2.0+) to leverage Prisma's native async nature for performance.

### 2. Authentication Strategy for Microservices
**Context**: Need to authenticate users across potential future services (`tickets`, `orders`).
**Options**:
- **Session-based (Cookies)**: Harder to share across domains/services without shared Redis/DB.
- **JWT (Stateless)**: Standard for microservices.
**Decision**: **JWT (JSON Web Tokens)**.
- Auth Service issues JWT upon login.
- Client stores JWT (HttpOnly cookie preferred for security).
- Other services verify JWT signature.

### 3. Password Hashing
**Context**: Security requirement.
**Decision**: **Argon2** (via `passlib` or `argon2-cffi`). Current industry standard, memory-hard.

## Technology Stack Confirmation

| Component | Choice | Rationale |
|-----------|--------|-----------|
| **Backend Framework** | Flask (Python) | User request. Lightweight, flexible. |
| **Frontend Framework** | Next.js 14 | User request. React Server Components, Routing. |
| **ORM** | Prisma | User request. Type-safe, auto-generated client. |
| **DB** | PostgreSQL | User request. Robust relational DB. |
| **Auth** | JWT | Scalable for microservices. |

## Implementation Patterns

### Validation
- **Backend**: Pydantic (integrates well with Python type hints).
- **Frontend**: Zod (matches TypeScript/Prisma types well).

### API Contract
- RESTful JSON API.
- Endpoints:
    - `POST /api/users/register`
    - `POST /api/users/login`
    - `GET /api/users/me` (Current user)
    - `POST /api/users/logout`
