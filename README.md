# Ticketing App - Authentication System

A microservices-based authentication system with a Flask backend and Next.js frontend.

## Tech Stack

- **Backend**: Python 3.9+, Flask 3.x, Prisma ORM
- **Frontend**: Next.js 14 (App Router), TypeScript, Tailwind CSS
- **Database**: PostgreSQL
- **Authentication**: JWT tokens (HttpOnly cookies), Argon2 password hashing

## Prerequisites

- Python 3.9+
- Node.js 18+
- PostgreSQL (running on localhost:5432)

## Project Structure

```
ticketing/
├── auth/                 # Flask backend service
│   ├── src/
│   │   ├── app.py        # Flask entry point
│   │   ├── schema.prisma # Database schema
│   │   ├── routes/       # API endpoints
│   │   ├── services/     # Business logic
│   │   ├── middleware/   # Auth & error handling
│   │   └── utils/        # JWT, security, Prisma
│   └── tests/            # Unit & integration tests
├── client/               # Next.js frontend
│   └── src/
│       ├── app/          # Pages (register, login, landing)
│       ├── components/   # UI components
│       ├── context/      # Auth context
│       └── lib/          # API client
└── specs/                # Feature specifications
```

## Setup

### 1. Database Setup

Ensure PostgreSQL is running and create a database:

```bash
psql -U postgres
CREATE DATABASE ticketing_auth;
CREATE USER julyan WITH PASSWORD 'admin123';
GRANT ALL PRIVILEGES ON DATABASE ticketing_auth TO julyan;
\q
```

### 2. Backend Setup

```bash
# Navigate to auth directory
cd auth

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Generate Prisma client
cd src
prisma generate

# Push schema to database (first time only)
prisma db push
```

### 3. Frontend Setup

```bash
# Navigate to client directory
cd client

# Install dependencies
npm install
```

### 4. Environment Variables

**Backend** (`auth/src/.env`):
```env
DATABASE_URL="postgresql://julyan:admin123@localhost:5432/ticketing_auth"
JWT_SECRET="your-secret-key-change-in-production"
```

**Frontend** (`client/.env.local`):
```env
NEXT_PUBLIC_API_URL=http://localhost:5000
```

## Running the Application

### Start Backend Server

```bash
cd auth
source venv/bin/activate
cd src
python app.py
```

The backend will run on http://localhost:5000

### Start Frontend Server

```bash
cd client
npm run dev
```

The frontend will run on http://localhost:3000

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/users/health` | Health check |
| POST | `/api/users/register` | Register new user |
| POST | `/api/users/login` | Login user |
| POST | `/api/users/logout` | Logout user |
| GET | `/api/users/me` | Get current user (protected) |

### Register User

```bash
curl -X POST http://localhost:5000/api/users/register \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'
```

### Login User

```bash
curl -X POST http://localhost:5000/api/users/login \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{"email": "user@example.com", "password": "password123"}'
```

## Running Tests

### Backend Tests

```bash
cd auth
source venv/bin/activate
cd src
python -m pytest ../tests/ -v
```

## User Flow

1. **Register**: Visit http://localhost:3000/register to create an account
2. **Login**: Visit http://localhost:3000/login to authenticate
3. **Landing**: After login, you'll be redirected to http://localhost:3000/landing
4. **Logout**: Click the logout button in the header

## Development

### Backend Development

The Flask server runs in debug mode by default, with auto-reload enabled.

### Frontend Development

Next.js runs with hot module replacement (HMR) for instant updates.

## License

MIT
