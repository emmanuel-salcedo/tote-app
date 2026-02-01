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
- Simple password authentication

### Out of Scope (V1)
- Public sharing
- Notifications
- AI tagging
- Third-party integrations

---

## 6. Core Features

### Tote Management
- Unique numeric ID
- Optional tote name
- Auto QR generation
- Location assignment
- 2x2 printable QR label
- Edit / Archive

### Item Management
Fields:
- **Name (Required)**
- Quantity (Optional)
- Category (Optional)
- Notes (Optional)
- Multiple Photos (Optional)
- Checkoutable Toggle (Optional)

Capabilities:
- Add / Edit / Archive
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

### Full Audit Trail
Logs:
- Timestamp
- User
- Action Type
- Before/After Data
- Optional Notes

---

## 7. Non-Functional Requirements
- Fast performance
- Mobile-friendly UI
- Secure password storage
- Database backups
- Docker deployment
- iPhone QR scanning compatibility

---

## 8. Acceptance Criteria
- QR labels print correctly
- Scan opens correct tote
- Search returns correct location
- Checkout functions correctly
- Audit logs complete
- Remote access functional
