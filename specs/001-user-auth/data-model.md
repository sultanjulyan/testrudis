# Data Model: User Authentication

## Entities

### User

Represents a registered account in the system.

| Field | Type | Required | Unique | Description |
|-------|------|----------|--------|-------------|
| `id` | Integer (Auto-inc) | Yes | Yes | Primary Key |
| `email` | String | Yes | Yes | User's email address |
| `password` | String | Yes | No | Hashed password (Argon2) |
| `createdAt` | DateTime | Yes | No | Timestamp of creation |
| `updatedAt` | DateTime | Yes | No | Timestamp of last update |

> **Note**: PascalCase for Prisma models, camelCase for fields.

## Prisma Schema (Draft)

```prisma
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

generator client {
  provider = "prisma-client-py"
  interface = "asyncio"
}

model User {
  id        Int      @id @default(autoincrement())
  email     String   @unique
  password  String
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}
```

## Validation Rules

### Registration (Input)
- **Email**: Must be valid email format. Max 255 chars.
- **Password**: Min 8 chars, Max 100 chars.

### Database Constraints
- `email`: UNIQUE index.
