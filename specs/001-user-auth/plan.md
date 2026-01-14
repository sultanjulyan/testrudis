# Implementation Plan: User Authentication

**Branch**: `001-user-auth` | **Date**: 2026-01-14 | **Spec**: [specs/001-user-auth/spec.md](../spec.md)
**Input**: Feature specification from `specs/001-user-auth/spec.md`

## Summary

Implement a microservices-ready User Authentication system. 
Frontend: Next.js application for registration, login, and landing page.
Backend: Flask service ("Auth Service") handling API requests.
Database: PostgreSQL managed via Prisma ORM.

## Technical Context

**Language/Version**: Python 3.11+ (Backend), TypeScript 5.x+ (Frontend)
**Primary Dependencies**: 
- Backend: Flask, prisma-client-py
- Frontend: Next.js 14 (App Router), Prisma Client (if direct DB needed, but likely via API), Axios/Fetch
**Storage**: PostgreSQL (localhost:5432, user: julyan, pass: admin123)
**Testing**: 
- Backend: Pytest
- Frontend: Jest / React Testing Library
**Target Platform**: Web browsers, Microservices infrastructure
**Project Type**: Microservices Web Application
**Performance Goals**: <500ms Login/Register P95, <100ms UI interaction
**Constraints**: Zero-trust architecture logic (validate everything), Secure password hashing (Argon2/Bcrypt)
**Scale/Scope**: Foundation for future ticketing services.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **I. Code Quality**: Standard linters (Black/Pylint for Python, ESLint/Prettier for TS) will be configured.
- [x] **II. Testing**: Plan includes mandatory unit and integration tests. TDD approach for API.
- [x] **III. UX**: Uses Next.js for consistent routing and React for component usage.
- [x] **IV. UI**: "Don't make me think" applied to Login/Register flows.
- [x] **V. Performance**: Async Python and compiled JS for efficiency.
- [x] **Tech Standards**: Flask and Next.js are industry standards. Prisma is a modern standard ORM.

## Project Structure

### Documentation (this feature)

```text
specs/001-user-auth/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
└── tasks.md             # Phase 2 output
```

### Source Code (repository root)

```text
auth/                   # Microservice: Auth
├── src/
│   ├── app.py          # Entry point
│   ├── schema.prisma   # Prisma Schema
│   ├── models/         # Pydantic models / Domain entities
│   ├── routes/         # API Controllers
│   └── services/       # Business Logic
└── tests/

client/                 # Frontend Application
├── app/               # Next.js App Router
│   ├── (auth)/        # Route groups for auth
│   │   ├── login/
│   │   └── register/
│   └── landing/
├── components/
└── lib/               # API clients, utils
```

**Structure Decision**: Microservices split. `auth/` directory contains the Flask service. `client/` contains the Next.js frontend. This prepares the repo for adding `tickets/`, `orders/` services later.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Microservices Arch | User Request | Monolith rejected by explicit user requirement for microservices |
| Prisma with Flask | User Request | SQLAlchmey is standard for Flask, but user requested Prisma |
