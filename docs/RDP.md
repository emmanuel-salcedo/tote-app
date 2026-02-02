# Tote Tracker — Requirements & Design Plan (RDP)

## 1. Technical Architecture

### Frontend
- React or Vue
- Mobile-first design
- PWA installable

### Backend
- Node.js (Express) or Python (FastAPI)
- REST API
- Simple password auth with HTTP-only session cookie (no JWT)

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
- email
- name
- role
- password_hash
- created_at
- archived_at

Constraints:
- email unique

### Locations
- id
- parent_id
- name
- path_string
- archived_at

Constraints:
- path_string unique (denormalized full path)

Indexes:
- locations(path_string)

### Totes
- id
- tote_number
- tote_name
- location_id
- qr_value
- created_at
- archived_at

Constraints:
- tote_number unique (auto-generated)
- qr_value unique

Indexes:
- totes(tote_number)
- totes(qr_value)
- totes(location_id)

### Items
- id
- tote_id
- name
- quantity
- category
- notes
- is_checkoutable
- timestamps
- archived_at

Constraints:
- name required
- is_checkoutable default false

Indexes:
- items(name)
- items(tote_id)

### Item_Photos
- id
- item_id
- file_path

Constraints:
- file_path required

Indexes:
- item_photos(item_id)

### Item_Checkouts
- id
- item_id
- checked_out_by
- checked_out_to
- checked_out_at
- due_back_at
- returned_at
- notes

Constraints:
- checked_out_at required

Indexes:
- item_checkouts(item_id)
- item_checkouts(checked_out_at)

### Audit_Log
- id
- actor_user_id
- entity_type
- entity_id
- action
- before_json
- after_json
- timestamp

Indexes:
- audit_log(entity_type, entity_id)
- audit_log(timestamp)

---

## 3. Key Screens
1. Home (Search + Scan + Quick Add)
2. QR Scan Screen
3. Tote Detail
4. Item Detail
5. Locations Manager
6. Admin Panel

---

## 3.1 API Outline

### Auth
- POST /auth/login (sets session cookie)
- POST /auth/logout (clears session cookie)

### Users
- GET /users
- POST /users
- PATCH /users/:id
- DELETE /users/:id (soft delete)

### Locations
- GET /locations
- POST /locations
- PATCH /locations/:id
- DELETE /locations/:id (soft delete)

### Totes
- GET /totes
- POST /totes
- PATCH /totes/:id
- DELETE /totes/:id (soft delete)
- GET /totes/:id/items

### Items
- GET /items
- POST /items
- PATCH /items/:id
- DELETE /items/:id (soft delete)

### Photos
- POST /items/:id/photos
- DELETE /items/:id/photos/:photoId

### Checkouts
- POST /items/:id/checkouts
- POST /items/:id/checkins
- GET /items/:id/checkouts

### Audit
- GET /audit

---

## 3.2 Behavior Rules
- Current checkout = most recent Item_Checkouts row where returned_at is null.
- Item status is derived from current checkout (do not store redundant status fields on items).
- Soft-deleted rows are excluded from default queries; Admin can include them via a flag.
- Audit_Log records create/update/delete/checkout/check-in actions with before/after payloads.

Auth & Permissions:
- All non-auth endpoints require a valid session cookie.
- Role checks enforced in route guards or middleware.

Photo Limits:
- Enforce max file size and max count per item at upload time.

---

## 4. Deployment Plan

### Docker Stack
Services:
- app
- db (Postgres)
- uploads volume

### Ports & Volumes
- app: 8000
- db: 5432
- uploads mounted to NAS path (photos)

### Env Vars
- DATABASE_URL
- ADMIN_EMAIL
- ADMIN_PASSWORD
- UPLOADS_PATH

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

Retention:
- Keep 4 weekly DB exports
- Keep 30 days of photos backup snapshots

---

## 8. Final Acceptance Criteria
- QR scanning works
- Items searchable
- Locations hierarchical
- Checkout system functional
- Audit logs complete
- Docker deployment stable
