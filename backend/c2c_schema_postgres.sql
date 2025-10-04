-- ====================================================================
-- C2C Database Schema (PostgreSQL) — NO attachments
-- Core: users, events, applications
-- Kept: tags, event_tags, event_slots, saved_events,
--       application_decisions, notifications, audit_log, reports, consents
-- ====================================================================

CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- =========================
-- ENUM Types
-- =========================
DO $$ BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'user_type') THEN
    CREATE TYPE user_type  AS ENUM ('STUDENT','ORGANIZER','BOTH');
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'event_status') THEN
    CREATE TYPE event_status AS ENUM ('OPEN','CLOSED','ARCHIVED');
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'app_status') THEN
    CREATE TYPE app_status AS ENUM ('PENDING','APPROVED','REJECTED','CANCELLED');
  END IF;
END $$;

-- =========================
-- CORE TABLES
-- =========================
CREATE TABLE IF NOT EXISTS users (
  id            uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  email         text NOT NULL UNIQUE,
  password_hash text NOT NULL,
  display_name  text NOT NULL,
  type          user_type NOT NULL DEFAULT 'BOTH',
  is_active     boolean NOT NULL DEFAULT true,
  created_at    timestamptz NOT NULL DEFAULT now(),
  updated_at    timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS events (
  id          uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  created_by  uuid NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  title       text NOT NULL,
  description text,
  location    text,
  starts_at   timestamptz,
  ends_at     timestamptz,
  capacity    integer NOT NULL DEFAULT 1 CHECK (capacity >= 1),
  status      event_status NOT NULL DEFAULT 'OPEN',
  created_at  timestamptz NOT NULL DEFAULT now(),
  updated_at  timestamptz NOT NULL DEFAULT now(),
  CHECK (ends_at IS NULL OR starts_at IS NULL OR ends_at >= starts_at)
);
CREATE INDEX IF NOT EXISTS idx_events_creator ON events(created_by);
CREATE INDEX IF NOT EXISTS idx_events_time    ON events(starts_at, ends_at);
CREATE INDEX IF NOT EXISTS idx_events_status  ON events(status);

CREATE TABLE IF NOT EXISTS applications (
  id           uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  event_id     uuid NOT NULL REFERENCES events(id) ON DELETE CASCADE,
  applicant_id uuid NOT NULL REFERENCES users(id)  ON DELETE CASCADE,
  status       app_status NOT NULL DEFAULT 'PENDING',
  note         text,
  reason       text,
  decided_at   timestamptz,
  decided_by   uuid REFERENCES users(id),
  created_at   timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT uq_application UNIQUE (event_id, applicant_id)
);
CREATE INDEX IF NOT EXISTS idx_app_event      ON applications(event_id);
CREATE INDEX IF NOT EXISTS idx_app_applicant  ON applications(applicant_id);
CREATE INDEX IF NOT EXISTS idx_app_status     ON applications(status);

-- =========================
-- EXTENSIONS
-- =========================

-- tags & event_tags (N:M)
CREATE TABLE IF NOT EXISTS tags (
  id   uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name text NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS event_tags (
  event_id uuid NOT NULL REFERENCES events(id) ON DELETE CASCADE,
  tag_id   uuid NOT NULL REFERENCES tags(id)   ON DELETE CASCADE,
  CONSTRAINT pk_event_tags PRIMARY KEY (event_id, tag_id)
);
CREATE INDEX IF NOT EXISTS idx_event_tags_event ON event_tags(event_id);
CREATE INDEX IF NOT EXISTS idx_event_tags_tag   ON event_tags(tag_id);

-- event_slots (1:N)
CREATE TABLE IF NOT EXISTS event_slots (
  id        uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  event_id  uuid NOT NULL REFERENCES events(id) ON DELETE CASCADE,
  starts_at timestamptz NOT NULL,
  ends_at   timestamptz NOT NULL,
  capacity  integer,
  CONSTRAINT chk_slot_time CHECK (ends_at >= starts_at),
  CONSTRAINT chk_slot_capacity CHECK (capacity IS NULL OR capacity >= 1)
);
CREATE INDEX IF NOT EXISTS idx_event_slots_event ON event_slots(event_id);
CREATE INDEX IF NOT EXISTS idx_event_slots_time  ON event_slots(starts_at, ends_at);

-- saved_events (bookmark)
CREATE TABLE IF NOT EXISTS saved_events (
  user_id  uuid NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  event_id uuid NOT NULL REFERENCES events(id) ON DELETE CASCADE,
  saved_at timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT pk_saved_events PRIMARY KEY (user_id, event_id)
);

-- application_decisions (history / append-only)
CREATE TABLE IF NOT EXISTS application_decisions (
  id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  application_id  uuid NOT NULL REFERENCES applications(id) ON DELETE CASCADE,
  decided_by      uuid NOT NULL REFERENCES users(id),
  status          app_status NOT NULL CHECK (status IN ('APPROVED','REJECTED')),
  reason          text,
  decided_at      timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_app_decision_app ON application_decisions(application_id);
CREATE INDEX IF NOT EXISTS idx_app_decision_by  ON application_decisions(decided_by);

-- notifications
CREATE TABLE IF NOT EXISTS notifications (
  id         uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id    uuid NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  type       text NOT NULL,    -- 'APP_APPROVED' | 'APP_REJECTED' | 'SYSTEM' ...
  payload    jsonb,
  is_read    boolean NOT NULL DEFAULT false,
  created_at timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_notifications_user    ON notifications(user_id);
CREATE INDEX IF NOT EXISTS idx_notifications_is_read ON notifications(is_read);

-- audit_log
CREATE TABLE IF NOT EXISTS audit_log (
  id          uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  actor_id    uuid REFERENCES users(id) ON DELETE SET NULL,
  action      text NOT NULL,           -- 'CREATE_EVENT', 'UPDATE_EVENT', 'APPROVE', 'REJECT', ...
  entity_type text NOT NULL,           -- 'EVENT' | 'APPLICATION' | 'USER'
  entity_id   uuid NOT NULL,
  meta        jsonb,
  at          timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_audit_actor  ON audit_log(actor_id);
CREATE INDEX IF NOT EXISTS idx_audit_entity ON audit_log(entity_type, entity_id);

-- reports (abuse reports)
CREATE TABLE IF NOT EXISTS reports (
  id           uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  reporter_id  uuid NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  target_type  text NOT NULL,          -- 'USER' | 'EVENT' | 'APPLICATION'
  target_id    uuid NOT NULL,
  reason       text NOT NULL,
  created_at   timestamptz NOT NULL DEFAULT now(),
  resolved_by  uuid REFERENCES users(id),
  resolved_at  timestamptz
);
CREATE INDEX IF NOT EXISTS idx_reports_reporter ON reports(reporter_id);
CREATE INDEX IF NOT EXISTS idx_reports_target   ON reports(target_type, target_id);

-- consents (1:1 with users)
CREATE TABLE IF NOT EXISTS consents (
  user_id         uuid PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
  email_marketing boolean NOT NULL DEFAULT false,
  data_sharing    boolean NOT NULL DEFAULT false,
  updated_at      timestamptz NOT NULL DEFAULT now()
);

-- =========================
-- Helpful Views (optional)
-- =========================
CREATE OR REPLACE VIEW event_application_counts AS
SELECT
  e.id AS event_id,
  COUNT(*) FILTER (WHERE a.status = 'PENDING')  AS pending_count,
  COUNT(*) FILTER (WHERE a.status = 'APPROVED') AS approved_count,
  COUNT(*) FILTER (WHERE a.status = 'REJECTED') AS rejected_count
FROM events e
LEFT JOIN applications a ON a.event_id = e.id
GROUP BY e.id;

CREATE OR REPLACE VIEW applicant_status_summary AS
SELECT
  u.id AS user_id,
  COUNT(*) FILTER (WHERE a.status = 'PENDING')   AS pending_count,
  COUNT(*) FILTER (WHERE a.status = 'APPROVED')  AS approved_count,
  COUNT(*) FILTER (WHERE a.status = 'REJECTED')  AS rejected_count,
  COUNT(*) FILTER (WHERE a.status = 'CANCELLED') AS cancelled_count
FROM users u
LEFT JOIN applications a ON a.applicant_id = u.id
GROUP BY u.id;
