# Tote Tracker — Development Phases

## Phase 0 — Project Setup
- Create Git repo ✅
- Add PRD/RDP docs ✅
- Select stack ✅ (FastAPI)
- Docker skeleton ✅
- Initial commit ✅

---

## Phase 1 — Database + API Foundation
- Create schema + migrations ✅
- Seed admin/member ✅ (admin bootstrap)
- Health endpoint ✅
- Commit ✅

---

## Phase 2 — Authentication
- Login endpoint ✅
- Session cookie auth + guards ✅
- Role permissions ⏳ (policy defined; enforcement TBD)
- Login UI ⏳
- Commit ✅

---

## Phase 3 — Locations System
- CRUD hierarchy ✅
- Path generation ✅
- Location picker UI ⏳
- Commit ✅

---

## Phase 4 — Tote Management + QR
- Tote CRUD ✅
- QR generation ✅
- 2x2 print view ✅
- Commit ✅

---

## Phase 5 — Item Management
- Item CRUD ✅
- Optional fields ✅
- Tote detail UI ⏳
- Commit ✅

---

## Phase 6 — Photos
- Upload endpoint ✅
- Multi-photo support ✅
- Gallery UI ⏳
- Commit ✅

---

## Phase 7 — QR Scanning
- Camera scanner page ✅ (basic page scaffolded)
- Tote lookup ⏳
- Commit ✅

---

## Phase 8 — Fuzzy Search
- Backend fuzzy query ✅ (basic ILIKE search)
- Search UI ⏳
- Commit ✅

---

## Phase 9 — Moves + Audit Logs
- Audit middleware ✅
- Item/tote move logging ✅
- Audit viewer UI ⏳
- Commit ✅

---

## Phase 10 — Checkout System
- Checkout fields ✅
- Checkout/check-in endpoints ✅
- UI workflow ✅ (basic UI stub)
- Commit ✅

---

## Phase 11 — Polish & Deployment
- Docker hardening ✅ (non-root container)
- Backup scripts ✅ (stub)
- PWA polish ✅ (manifest route)
- Error handling ✅ (global handler)
- Final commit ⏳

---

## Suggested Version Tags
- v0.1 DB/API
- v0.4 Totes + QR
- v0.7 Scanning
- v0.9 Audit
- v1.0 Checkout Complete
