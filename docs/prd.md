# Tote Tracker — Product Requirements Document (PRD)

## 1. Project Overview
**Project Name:** Tote Tracker  
**Owner:** Emmanuel  
**Users:** Emmanuel (Admin), Brenda (Member)  
**Platforms:** iPhone (Safari / PWA), Web Browser  
**Deployment:** Self-hosted via Docker / Portainer on NAS

**Summary:**  
Tote Tracker is a self-hosted inventory application that allows a household to organize and locate storage totes using QR codes and numeric IDs. Users can add items with optional metadata and photos, search using fuzzy matching, track movements, and optionally check items in and out.

---

## 2. Problem Statement
Physical storage totes become disorganized over time. Users forget contents and locations, causing wasted time and effort. There is no shared system or audit history.

---

## 3. Goals & Objectives
### Primary Goal
- Instantly find any stored item and its physical location.

### Secondary Goals
- Reduce search time.
- Maintain movement history.
- Enable shared family usage.

### Success Metrics
- Search results < 1 second.
- All totes labeled with QR + number.
- Accurate audit trail.

---

## 4. Users & Roles
| Role   | Permissions |
|--------|------------|
| Admin  | Full control, manage users, locations, backups |
| Member | Add/edit items, move totes/items, checkout items |

### Permissions Matrix
| Action | Admin | Member |
|--------|:-----:|:------:|
| Create/Edit/Archive Totes | ✅ | ✅ |
| Create/Edit/Archive Items | ✅ | ✅ |
| Move Totes/Items | ✅ | ✅ |
| Checkout/Check-in Items | ✅ | ✅ |
| Manage Locations | ✅ | ✅ |
| Manage Users | ✅ | ❌ |
| View Audit Logs | ✅ | ✅ |
| Manage Backups/Settings | ✅ | ❌ |

---

## 5. Scope

### In Scope
- Tote creation with QR + number
- Item management
- Location hierarchy
- Fuzzy search
- Checkout system
- Multi-photo support
- Full audit logs
- Self-hosted deployment
- Simple password authentication (no JWT/session)

### Out of Scope (V1)
- Public sharing
- Notifications
- AI tagging
- Third-party integrations

---

## 6. Core Features

### Tote Management
- Auto-generated unique numeric ID
- Optional tote name
- Auto QR generation
- Location assignment
- 2x2 printable QR label
- Edit / Archive (soft delete with archived_at)

### Item Management
Fields:
- **Name (Required)**
- Quantity (Optional)
- Category (Optional)
- Notes (Optional)
- Multiple Photos (Optional)
- Checkoutable Toggle (Optional)
- Archived At (system field)

Capabilities:
- Add / Edit / Archive (soft delete with archived_at)
- Move between totes

### Search
- Fuzzy / partial matching
- Displays:
  - Item Name
  - Tote Number/Name
  - Location
  - Status
- Click tote → show contents

### Location System
Hierarchy:
Area → Zone → Spot

Implementation:
- Denormalized full path for fast search

Example:
Garage → Left Wall → Shelf A3

### Movement Tracking
- Tote location changes
- Item tote transfers
- Checkout / Check-in

### Checkout System
Fields:
- Checkoutable?
- Status
- Checked Out To
- Due Date (Optional)
- Notes

History:
- Multiple checkout rows per item
- Current checkout is the most recent row with no return date

### Full Audit Trail
Logs:
- Timestamp
- User
- Action Type
- Before/After Data
- Optional Notes

Visibility:
- Admin and Member can view audit logs (read-only)

---

## 7. Non-Functional Requirements
- Fast performance
- Mobile-friendly UI
- Secure password storage
- Database backups
- Docker deployment
- iPhone QR scanning compatibility

### Performance Targets
- Search results return in under 1 second on a typical home NAS.
- QR scan to tote detail in under 2 seconds on iPhone Safari.

### Data & Storage Limits
- Max photo size: 5 MB each.
- Max photos per item: 10.
- Soft-deleted records remain queryable by Admin only.

### Search Behavior
- Matches against item name, tote number/name, location path.
- Typo tolerance up to 2 edits.
- Results ranked by (1) item name, (2) tote number, (3) location path.

### Key User Flows
1. Create Tote: Admin/Member creates tote → system generates unique number + QR → assign location → print label.
2. Add Item: Add item → select tote → optional photos → save → item visible in tote.
3. Move Item: Select item → choose new tote/location → save → audit entry created.
4. Scan QR: Scan → open tote → view items → quick add item.
5. Checkout: Mark item checkoutable → checkout → item shows status + due date → check-in closes checkout.

---

## 8. Acceptance Criteria
- QR labels print correctly
- Scan opens correct tote
- Search returns correct location
- Checkout functions correctly
- Audit logs complete
- Remote access functional
