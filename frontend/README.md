# Skill Lantern Frontend

Next.js frontend for the Skill Lantern career guidance platform.

## Features

- Landing pages for product information
- Multi-step signup and profile collection
- Credentials and Google OAuth sign-in through NextAuth
- Prisma-backed user profiles and recommendation history
- Dashboard with career predictions, roadmaps, college recommendations, progress tracking, feedback, and print/PDF support
- API proxy routes that call the FastAPI backend and persist recommendation results

## Tech Stack

- **Next.js 16** with App Router
- **React 19**
- **NextAuth v5**
- **Prisma** with PostgreSQL
- **Tailwind CSS**
- **Framer Motion**

## Setup

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Configure Environment

```bash
cp .env.example .env.local
```

Required values:

- `DATABASE_URL`
- `AUTH_URL`
- `AUTH_SECRET`
- `AUTH_GOOGLE_ID`
- `AUTH_GOOGLE_SECRET`
- `NEXT_PUBLIC_API_URL`

Optional values:

- `ADMIN_EMAILS` - comma-separated list for `/api/users`
- `AUTH_ALLOW_DANGEROUS_EMAIL_LINKING` - defaults to false; set true only if you intentionally want Google OAuth to link to an existing credentials account with the same email

### 3. Generate Prisma Client

```bash
npx prisma generate
```

### 4. Run Migrations

```bash
npx prisma migrate dev
```

### 5. Start Development Server

```bash
npm run dev
```

Open http://localhost:3000.

## Scripts

```bash
npm run dev      # Start local development server
npm run build    # Production build
npm run start    # Start production server
npm run lint     # ESLint
```

## Backend Dependency

Recommendation generation expects the FastAPI backend to be running at `NEXT_PUBLIC_API_URL`, usually:

```text
http://localhost:8000
```

If the backend is unavailable during signup, account creation still succeeds and the dashboard can retry recommendation generation later.
