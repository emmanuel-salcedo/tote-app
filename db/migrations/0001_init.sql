-- Tote Tracker minimal Postgres schema (draft)

CREATE TABLE users (
  id BIGSERIAL PRIMARY KEY,
  email TEXT NOT NULL,
  name TEXT NOT NULL,
  role TEXT NOT NULL,
  password_hash TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  archived_at TIMESTAMPTZ
);

CREATE UNIQUE INDEX users_email_uq ON users(email);

CREATE TABLE sessions (
  id TEXT PRIMARY KEY,
  user_id BIGINT NOT NULL REFERENCES users(id),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  expires_at TIMESTAMPTZ NOT NULL
);

CREATE INDEX sessions_user_id_idx ON sessions(user_id);

CREATE TABLE locations (
  id BIGSERIAL PRIMARY KEY,
  parent_id BIGINT REFERENCES locations(id),
  name TEXT NOT NULL,
  path_string TEXT NOT NULL,
  archived_at TIMESTAMPTZ
);

CREATE UNIQUE INDEX locations_path_string_uq ON locations(path_string);
CREATE INDEX locations_path_string_idx ON locations(path_string);

CREATE TABLE totes (
  id BIGSERIAL PRIMARY KEY,
  tote_number INTEGER NOT NULL,
  tote_name TEXT,
  location_id BIGINT REFERENCES locations(id),
  qr_value TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  archived_at TIMESTAMPTZ
);

CREATE UNIQUE INDEX totes_tote_number_uq ON totes(tote_number);
CREATE UNIQUE INDEX totes_qr_value_uq ON totes(qr_value);
CREATE INDEX totes_location_id_idx ON totes(location_id);

CREATE TABLE items (
  id BIGSERIAL PRIMARY KEY,
  tote_id BIGINT REFERENCES totes(id),
  name TEXT NOT NULL,
  quantity INTEGER,
  category TEXT,
  notes TEXT,
  is_checkoutable BOOLEAN NOT NULL DEFAULT false,
  status TEXT,
  checked_out_to TEXT,
  due_back_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  archived_at TIMESTAMPTZ
);

CREATE INDEX items_name_idx ON items(name);
CREATE INDEX items_tote_id_idx ON items(tote_id);

CREATE TABLE item_photos (
  id BIGSERIAL PRIMARY KEY,
  item_id BIGINT NOT NULL REFERENCES items(id),
  file_path TEXT NOT NULL
);

CREATE INDEX item_photos_item_id_idx ON item_photos(item_id);

CREATE TABLE item_checkouts (
  id BIGSERIAL PRIMARY KEY,
  item_id BIGINT NOT NULL REFERENCES items(id),
  checked_out_by BIGINT REFERENCES users(id),
  checked_out_to TEXT,
  checked_out_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  due_back_at TIMESTAMPTZ,
  returned_at TIMESTAMPTZ,
  notes TEXT
);

CREATE INDEX item_checkouts_item_id_idx ON item_checkouts(item_id);
CREATE INDEX item_checkouts_checked_out_at_idx ON item_checkouts(checked_out_at);

CREATE TABLE audit_log (
  id BIGSERIAL PRIMARY KEY,
  actor_user_id BIGINT REFERENCES users(id),
  entity_type TEXT NOT NULL,
  entity_id BIGINT NOT NULL,
  action TEXT NOT NULL,
  before_json JSONB,
  after_json JSONB,
  timestamp TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX audit_log_entity_idx ON audit_log(entity_type, entity_id);
CREATE INDEX audit_log_timestamp_idx ON audit_log(timestamp);
