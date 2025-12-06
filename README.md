# Volunteer & Charity Platform (Design-first, Tech-agnostic)

> Anonymous group per course rule: members referenced only by aliases **XA, XB, XC, XD, XE**.

## Overview
A platform to create campaigns/shifts, recruit/approve volunteers, **QR-based attendance**, and summarize volunteer hours. This repository focuses on **requirements & system design** first; technology choices will be recorded via ADRs.

## Scope (MVP)
- Auth & Roles (Organizer, Volunteer)
- Campaign/Shift management
- Apply/Approve flow + notifications
- QR check-in/out + hour computation
- Dashboard & CSV export

See `/docs/proposal` and `/docs/requirements`.

## Repository Rules (5 members)
- **Aliases only** (no real names): XA (PM/BA), XB (Backend lead), XC (Frontend lead), XD (QA/DevOps), **XE (UX/UI)**.
- **Weekly commits:** each member ≥1 update/week. Tag weekly releases: `v0.<week>`.
- **Branching:** `main` (protected) + short-lived feature branches `feat/...`, `fix/...`, `docs/...`.
- **Conventional Commits:** `feat:`, `fix:`, `docs:`, `chore:`, `refactor:`, `test:`.
- **PR Reviews:** at least 1 reviewer; CODEOWNERS auto-assigns.

## How to Use this Repo
1. Fill `/docs/proposal/*` following anonymity rules.
2. Capture requirements in `/docs/requirements`.
3. Draft design diagrams in `/docs/design` (keep both REST & GraphQL stubs until ADR 0002).
4. Record decisions in `/docs/adr`.
5. Plan tests in `/docs/qa`, deployment in `/docs/ops`.

## Roadmap
See [`/ROADMAP.md`](./ROADMAP.md) for week-by-week deliverables.

## Security & Privacy
See [`/docs/security`](./docs/security) and [`/SECURITY.md`](./SECURITY.md).

## Running the backend (development)

This repository includes a minimal FastAPI-based backend under the `backend/` folder. To run it locally:

1. Create and activate a Python virtual environment (recommended):

	- On Windows (PowerShell):
	  ```powershell
	  python -m venv .venv
	  .\.venv\Scripts\Activate.ps1
	  ```

2. Install dependencies (from `backend/requirements.txt`):

	```powershell
	pip install -r backend/requirements.txt
	```

3. Ensure you have a `.env` file at the repository root (or set environment variables) with the database credentials used by `backend/main.py`:

	Example `.env`:

	```text
	DATABASE_USER=your_user
	DATABASE_PASSWORD=your_password
	DATABASE_HOST=localhost
	DATABASE_NAME=your_db
	```

4. Run the backend with uvicorn on port 8000:

	```powershell
	# from repository root
	uvicorn backend.main:app --host 0.0.0.0 --reload
	```

5. Open http://localhost:8000/docs to see the interactive OpenAPI UI.

Notes:
- In development you can use `psycopg2-binary` (included) or `psycopg` / connection pool for production.
- If you don't want to connect to a real DB while developing endpoints, edit `backend/backend.py` to mock the DB connection or provide a fallback mode.
