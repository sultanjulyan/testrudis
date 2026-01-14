# Quickstart: User Authentication

## Prerequisites
- Node.js 18+
- Python 3.11+
- PostgreSQL Running (localhost:5432)
- Database created: `ticketing_auth` (or similar)

## Services

### 1. auth-service (Backend)

```bash
cd auth
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Database Setup
# Ensure .env has DATABASE_URL="postgresql://julyan:admin123@localhost:5432/ticketing_auth"
prisma generate
prisma db push

# Run App
python src/app.py
# Runs on http://localhost:5000
```

### 2. client (Frontend)

```bash
cd client
npm install
npm run dev
# Runs on http://localhost:3000
```

## Testing

### Backend Tests
```bash
cd auth
pytest
```

### Frontend Tests
```bash
cd client
npm test
```

## Environment Variables

### Backend (.env)
```
DATABASE_URL="postgresql://julyan:admin123@localhost:5432/ticketing_auth"
JWT_SECRET="your_jwt_secret_key"
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL="http://localhost:5000"
```
