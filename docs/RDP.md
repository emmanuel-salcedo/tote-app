# Tote Tracker — Requirements & Design Plan (RDP)

## 1. Technical Architecture

### Frontend
- React or Vue
- Mobile-first design
- PWA installable

### Backend
- Node.js (Express) or Python (FastAPI)
- REST API
- JWT / Session auth

### Database
- PostgreSQL

### File Storage
- NAS mounted volume for photos

### QR Generation
- SVG/PNG generation on tote creation

---

## 2. Data Model

### Users
- id
- name
- role
- password_hash
- created_at

### Locations
- id
- parent_id
- name
- path_string

### Totes
- id
- tote_number
- tote_name
- location_id
- qr_value
- created_at

### Items
- id
- tote_id
- name
- quantity
- category
- notes
- is_checkoutable
- status
- checked_out_to
- due_back_at
- timestamps

### Item_Photos
- id
- item_id
- file_path

### Audit_Log
- id
- actor_user_id
- entity_type
- entity_id
- action
- before_json
- after_json
- timestamp

---

## 3. Key Screens
1. Home (Search + Scan + Quick Add)
2. QR Scan Screen
3. Tote Detail
4. Item Detail
5. Locations Manager
6. Admin Panel

---

## 4. Deployment Plan

### Docker Stack
Services:
- app
- db (Postgres)
- uploads volume

### Remote Access
- Cloudflare Tunnel or Tailscale

---

## 5. Git Integration

### Repository Structure
tote-tracker/
frontend/
backend/
docker/
db/
docs/
README.md

### Branches
- main
- dev
- feature/*

### Commit Style
- feat:
- fix:
- docs:
- chore:
- ui:

### Tags
- v0.1-alpha
- v0.5-beta
- v1.0

---

## 6. Testing Plan
- API unit tests
- QR scan tests
- Search performance tests
- Checkout flow tests

---

## 7. Maintenance & Backup
- Weekly DB export
- Photo folder backup
- Git repository as code backup

---

## 8. Final Acceptance Criteria
- QR scanning works
- Items searchable
- Locations hierarchical
- Checkout system functional
- Audit logs complete
- Docker deployment stable
