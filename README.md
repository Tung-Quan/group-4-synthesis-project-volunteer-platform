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
