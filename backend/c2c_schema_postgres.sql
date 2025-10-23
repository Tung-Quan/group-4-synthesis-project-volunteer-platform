-- ===========================================================
-- C2C Volunteer/Event Platform - Clean Schema (UUID-based)
-- ===========================================================

CREATE EXTENSION IF NOT EXISTS pgcrypto; -- gen_random_uuid()

-- --------------------------
-- USERS (auth + common info)
-- --------------------------
CREATE TABLE IF NOT EXISTS users (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email         TEXT NOT NULL UNIQUE,
  password_hash TEXT NOT NULL,
  full_name     TEXT,
  phone         TEXT,
  is_active     BOOLEAN NOT NULL DEFAULT TRUE,
  created_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- --------------------------
-- CONSENTS (per user)
-- --------------------------
CREATE TABLE IF NOT EXISTS consents (
  user_id        UUID PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
  email_marketing BOOLEAN NOT NULL DEFAULT FALSE,
  data_sharing    BOOLEAN NOT NULL DEFAULT FALSE,
  updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- --------------------------
-- AUDIT LOG (polymorphic)
-- --------------------------
CREATE TABLE IF NOT EXISTS audit_logs (
  id              BIGSERIAL PRIMARY KEY,
  actor_user_id   UUID REFERENCES users(id) ON DELETE SET NULL,
  action          TEXT NOT NULL,                    -- e.g. CREATE_EVENT
  entity_type     TEXT NOT NULL,                    -- e.g. 'event','slot','application'
  entity_id       TEXT,                             -- store pk as text (UUID/COMPOSITE)
  meta            JSONB,                            -- arbitrary details
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_audit_entity ON audit_logs(entity_type, entity_id);
CREATE INDEX IF NOT EXISTS idx_audit_actor  ON audit_logs(actor_user_id);

-- --------------------------
-- ROLE TABLES
-- --------------------------
CREATE TABLE IF NOT EXISTS students (
  user_id           UUID PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
  student_no        TEXT NOT NULL UNIQUE,
  social_work_days  NUMERIC(5,2) NOT NULL DEFAULT 0 CHECK (social_work_days >= 0)
);

CREATE TABLE IF NOT EXISTS organizers (
  user_id      UUID PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
  organizer_no TEXT NOT NULL UNIQUE,
  org_name     TEXT
);

-- --------------------------
-- EVENT / SLOT
-- --------------------------
DO $$ BEGIN
  CREATE TYPE event_status AS ENUM ('draft','published','cancelled','completed');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

CREATE TABLE IF NOT EXISTS events (
  id                 UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  organizer_user_id  UUID NOT NULL REFERENCES organizers(user_id) ON DELETE RESTRICT,
  title              TEXT NOT NULL,
  description        TEXT,
  location           TEXT,
  status             event_status NOT NULL DEFAULT 'draft',
  created_at         TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at         TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_events_org ON events(organizer_user_id);

-- Mỗi event có thể có nhiều time slots
CREATE TABLE IF NOT EXISTS event_slots (
  id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  event_id   UUID NOT NULL REFERENCES events(id) ON DELETE CASCADE,
  starts_at  TIMESTAMPTZ NOT NULL,
  ends_at    TIMESTAMPTZ NOT NULL,
  capacity   INT CHECK (capacity IS NULL OR capacity > 0),
  day_reward NUMERIC(4,2) NOT NULL DEFAULT 1 CHECK (day_reward >= 0),
  UNIQUE (event_id, starts_at, ends_at),
  CHECK (ends_at > starts_at)
);
CREATE INDEX IF NOT EXISTS idx_slots_event_time ON event_slots(event_id, starts_at);

-- --------------------------
-- APPLICATION (applies + decision + attendance lifecycle)
-- gộp APPLICATION & APPLICATION_DECISION
-- --------------------------
DO $$ BEGIN
  CREATE TYPE application_status AS ENUM
    ('applied','approved','rejected','withdrawn','attended','absent');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

CREATE TABLE IF NOT EXISTS applications (
  event_id         UUID NOT NULL REFERENCES events(id) ON DELETE CASCADE,
  student_user_id  UUID NOT NULL REFERENCES students(user_id) ON DELETE CASCADE,
  slot_id          UUID REFERENCES event_slots(id) ON DELETE SET NULL, -- nếu apply theo slot
  note             TEXT,
  status           application_status NOT NULL DEFAULT 'applied',
  created_at       TIMESTAMPTZ NOT NULL DEFAULT now(),                 -- applied_at
  decided_by       UUID REFERENCES organizers(user_id) ON DELETE SET NULL,
  decided_at       TIMESTAMPTZ,
  reason           TEXT,
  updated_at       TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (event_id, student_user_id)
);
CREATE INDEX IF NOT EXISTS idx_applications_student ON applications(student_user_id);
CREATE INDEX IF NOT EXISTS idx_applications_event   ON applications(event_id);

-- --------------------------
-- SAVED (bookmark)
-- --------------------------
CREATE TABLE IF NOT EXISTS student_saved_events (
  student_user_id  UUID NOT NULL REFERENCES students(user_id) ON DELETE CASCADE,
  event_id         UUID NOT NULL REFERENCES events(id)        ON DELETE CASCADE,
  saved_at         TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (student_user_id, event_id)
);

-- --------------------------
-- RATING (một SV đánh giá 1 lần / event)
-- --------------------------
CREATE TABLE IF NOT EXISTS ratings (
  event_id        UUID NOT NULL REFERENCES events(id)   ON DELETE CASCADE,
  student_user_id UUID NOT NULL REFERENCES students(user_id) ON DELETE CASCADE,
  stars           SMALLINT NOT NULL CHECK (stars BETWEEN 1 AND 5),
  comment         TEXT,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (event_id, student_user_id)
);

-- --------------------------
-- NOTIFICATIONS
-- --------------------------
CREATE TABLE IF NOT EXISTS notifications (
  id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  type           TEXT NOT NULL,           -- e.g. 'APPLICATION_APPROVED'
  payload        JSONB,                    -- arbitrary data
  is_read        BOOLEAN NOT NULL DEFAULT FALSE,
  created_at     TIMESTAMPTZ NOT NULL DEFAULT now(),
  sender_user_id   UUID REFERENCES users(id) ON DELETE SET NULL,
  receiver_user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  event_id       UUID REFERENCES events(id) ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS idx_notifications_to ON notifications(receiver_user_id, is_read);

-- --------------------------
-- (TÙY CHỌN) LEDGER cộng ngày công
-- Nếu muốn chi tiết mỗi lần cộng trừ, bật bảng dưới đây + trigger.
-- --------------------------
CREATE TABLE IF NOT EXISTS student_service_ledger (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  student_user_id UUID NOT NULL REFERENCES students(user_id) ON DELETE CASCADE,
  event_id        UUID REFERENCES events(id) ON DELETE SET NULL,
  slot_id         UUID REFERENCES event_slots(id) ON DELETE SET NULL,
  delta_days      NUMERIC(4,2) NOT NULL, -- +1, +0.5, v.v.
  note            TEXT,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_ledger_student ON student_service_ledger(student_user_id);

-- Trigger: khi applications.status chuyển sang 'attended' => cộng day_reward
CREATE OR REPLACE FUNCTION fn_app_attended_add_days()
RETURNS TRIGGER AS $$
DECLARE
  reward NUMERIC(4,2);
BEGIN
  IF TG_OP = 'UPDATE' AND NEW.status = 'attended' AND OLD.status IS DISTINCT FROM 'attended' THEN
    SELECT COALESCE(s.day_reward, 1) INTO reward
    FROM event_slots s
    WHERE s.id = NEW.slot_id;

    IF reward IS NULL THEN
      reward := 1; -- fallback nếu không apply theo slot
    END IF;

    -- ledger (chi tiết)
    INSERT INTO student_service_ledger(student_user_id, event_id, slot_id, delta_days, note)
    VALUES (NEW.student_user_id, NEW.event_id, NEW.slot_id, reward, 'auto: attended');

    -- tổng hợp nhanh trên students
    UPDATE students
       SET social_work_days = social_work_days + reward
     WHERE user_id = NEW.student_user_id;
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_app_attended_add_days ON applications;
CREATE TRIGGER trg_app_attended_add_days
AFTER UPDATE OF status ON applications
FOR EACH ROW
EXECUTE FUNCTION fn_app_attended_add_days();

-- --------------------------
-- VIEWS tiện ích
-- --------------------------
CREATE OR REPLACE VIEW v_organizer_events AS
SELECT e.*, o.organizer_no, o.org_name
FROM events e
JOIN organizers o ON o.user_id = e.organizer_user_id;

CREATE OR REPLACE VIEW v_student_bookmarks AS
SELECT s.student_no, e.id AS event_id, e.title, se.saved_at
FROM student_saved_events se
JOIN students s ON s.user_id = se.student_user_id
JOIN events   e ON e.id = se.event_id;

-- DONE
