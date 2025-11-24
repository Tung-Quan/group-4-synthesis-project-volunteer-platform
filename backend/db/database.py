# import threading
# import psycopg2
# import logging
# from ..config.env import ENV, env_settings
# from ..config.logger import logger

# logger=logging.getLogger(__name__)
# logger.info("Initializing database connection...")

# class DataBase:
#     """Thread-safe singleton that holds a persistent psycopg2 connection.

#     Notes:
#     - __new__ ensures only one instance is created.
#     - __init__ is guarded by _initialized so initialization happens once.
#     - Do not use a `with psycopg2.connect(...) as conn:` here because that
#       closes the connection at the end of the with-block; we want a
#       persistent connection stored on the instance.
#     """

#     _instance = None
#     _instance_lock = threading.Lock()

#     def __new__(cls, *args, **kwargs):
#         if cls._instance is None:
#             with cls._instance_lock:
#                 if cls._instance is None:
#                     cls._instance = super(DataBase, cls).__new__(cls)
#         return cls._instance

#     def __init__(self):
#         # run initialization only once
#         if getattr(self, "_initialized", False):
#             return
#         self.env = ENV()
#         try:
#             # keep connection open on the instance (don't use `with`)
#             self.connection = psycopg2.connect(self.env.get_db_url())
#             self.cursor = self.connection.cursor()
#             logger.info("Database connected successfully")
            
            
#             #CREATE DATABASE ENUMS
#             self.cursor.execute(
#         """
#         DO $$ BEGIN 
#             IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'user_type') THEN
#                 CREATE TYPE user_type AS ENUM ('STUDENT', 'ORGANIZER', 'BOTH');
#             END IF;
#             IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'event_status') THEN
#                 CREATE TYPE event_status AS ENUM ('OPEN', 'CLOSED', 'ARCHIVED');
#             END IF;
#             IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'app_status') THEN
#                 CREATE TYPE app_status AS ENUM ('PENDING', 'APPROVED', 'REJECTED', 'CANCELLED');
#             END IF;
#         END $$;
#         """
#             )
#             logger.info("Enums ensured")
            
#             #CREATE TABLES users IF NOT EXISTS
#             self.cursor.execute(
#         """
#         CREATE TABLE IF NOT EXISTS users (
#             id            uuid PRIMARY KEY DEFAULT gen_random_uuid(),
#             email         text NOT NULL UNIQUE,
#             password_hash text NOT NULL,
#             display_name  text NOT NULL,
#             type          user_type NOT NULL DEFAULT 'BOTH',
#             is_active     boolean NOT NULL DEFAULT true,
#             created_at    timestamptz NOT NULL DEFAULT now(),
#             updated_at    timestamptz NOT NULL DEFAULT now()
#         );
#         """
#             )
            
            
#             #CREATE TABLES events IF NOT EXISTS
#             self.cursor.execute(
#         """
#         CREATE TABLE IF NOT EXISTS events (
#             id          uuid PRIMARY KEY DEFAULT gen_random_uuid(),
#             created_by  uuid NOT NULL REFERENCES users(id) ON DELETE CASCADE,
#             title       text NOT NULL,
#             description text,
#             location    text,
#             starts_at   timestamptz,
#             ends_at     timestamptz,
#             capacity    integer NOT NULL DEFAULT 1 CHECK (capacity >= 1),
#             status      event_status NOT NULL DEFAULT 'OPEN',
#             created_at  timestamptz NOT NULL DEFAULT now(),
#             updated_at  timestamptz NOT NULL DEFAULT now(),
#             CHECK (ends_at IS NULL OR starts_at IS NULL OR ends_at >= starts_at)
#         );
#         CREATE INDEX IF NOT EXISTS idx_events_creator ON events(created_by);
#         CREATE INDEX IF NOT EXISTS idx_events_time    ON events(starts_at, ends_at);
#         CREATE INDEX IF NOT EXISTS idx_events_status  ON events(status);
#         """
#             )
            
#             #CREATE TABLES applications IF NOT EXISTS
#             self.cursor.execute(
#         """CREATE TABLE IF NOT EXISTS applications (
#             id           uuid PRIMARY KEY DEFAULT gen_random_uuid(),
#             event_id     uuid NOT NULL REFERENCES events(id) ON DELETE CASCADE,
#             applicant_id uuid NOT NULL REFERENCES users(id)  ON DELETE CASCADE,
#             status       app_status NOT NULL DEFAULT 'PENDING',
#             note         text,
#             reason       text,
#             decided_at   timestamptz,
#             decided_by   uuid REFERENCES users(id),
#             created_at   timestamptz NOT NULL DEFAULT now(),
#             CONSTRAINT uq_application UNIQUE (event_id, applicant_id)
#         );
#         CREATE INDEX IF NOT EXISTS idx_app_event      ON applications(event_id);
#         CREATE INDEX IF NOT EXISTS idx_app_applicant  ON applications(applicant_id);
#         CREATE INDEX IF NOT EXISTS idx_app_status     ON applications(status);
#         """
#             )
            
#             #CREATE TABLES tags IF NOT EXISTS
#             self.cursor.execute(
#         """CREATE TABLE IF NOT EXISTS tags (
#             id   uuid PRIMARY KEY DEFAULT gen_random_uuid(),
#             name text NOT NULL UNIQUE
#         );
#         """
#             )
            
#             #CREATE TABLES event_tags IF NOT EXISTS
#             self.cursor.execute(
#         """CREATE TABLE IF NOT EXISTS event_tags (
#             event_id uuid NOT NULL REFERENCES events(id) ON DELETE CASCADE,
#             tag_id   uuid NOT NULL REFERENCES tags(id)   ON DELETE CASCADE,
#             CONSTRAINT pk_event_tags PRIMARY KEY (event_id, tag_id)
#         );
#         CREATE INDEX IF NOT EXISTS idx_event_tags_event ON event_tags(event_id);
#         CREATE INDEX IF NOT EXISTS idx_event_tags_tag   ON event_tags(tag_id);
#         """ 
#             )
            
            
#             #CREATE TABLES event_slots IF NOT EXISTS
#             self.cursor.execute(
#         """CREATE TABLE IF NOT EXISTS event_slots (
#             id        uuid PRIMARY KEY DEFAULT gen_random_uuid(),
#             event_id  uuid NOT NULL REFERENCES events(id) ON DELETE CASCADE,
#             starts_at timestamptz NOT NULL,
#             ends_at   timestamptz NOT NULL,
#             capacity  integer,
#             CONSTRAINT chk_slot_time CHECK (ends_at >= starts_at),
#             CONSTRAINT chk_slot_capacity CHECK (capacity IS NULL OR capacity >= 1)
#         );
#         CREATE INDEX IF NOT EXISTS idx_event_slots_event ON event_slots(event_id);
#         CREATE INDEX IF NOT EXISTS idx_event_slots_time  ON event_slots(starts_at, ends_at);
#         """
#             )
            
#             #CREATE TABLES saved_events IF NOT EXISTS
#             self.cursor.execute(
#         """CREATE TABLE IF NOT EXISTS saved_events (
#             user_id  uuid NOT NULL REFERENCES users(id) ON DELETE CASCADE,
#             event_id uuid NOT NULL REFERENCES events(id) ON DELETE CASCADE,
#             saved_at timestamptz NOT NULL DEFAULT now(),
#             CONSTRAINT pk_saved_events PRIMARY KEY (user_id, event_id)
#         );
#         """
#             )
            
#             #CREATE TABLE notifications IF NOT EXISTS
#             self.cursor.execute(
#         """CREATE TABLE IF NOT EXISTS notifications (
#             id         uuid PRIMARY KEY DEFAULT gen_random_uuid(),
#             user_id    uuid NOT NULL REFERENCES users(id) ON DELETE CASCADE,
#             type       text NOT NULL,    -- 'APP_APPROVED' | 'APP_REJECTED' | 'SYSTEM' ...
#             payload    jsonb,
#             is_read    boolean NOT NULL DEFAULT false,
#             created_at timestamptz NOT NULL DEFAULT now()
#         );
#         CREATE INDEX IF NOT EXISTS idx_notifications_user    ON notifications(user_id);
#         CREATE INDEX IF NOT EXISTS idx_notifications_is_read ON notifications(is_read);
#         """
#             )
            
#             #CREATE TABLE audit_logs IF NOT EXISTS
#             self.cursor.execute(
#         """CREATE TABLE IF NOT EXISTS audit_log (
#             id          uuid PRIMARY KEY DEFAULT gen_random_uuid(),
#             actor_id    uuid REFERENCES users(id) ON DELETE SET NULL,
#             action      text NOT NULL,           -- 'CREATE_EVENT', 'UPDATE_EVENT', 'APPROVE', 'REJECT', ...
#             entity_type text NOT NULL,           -- 'EVENT' | 'APPLICATION' | 'USER'
#             entity_id   uuid NOT NULL,
#             meta        jsonb,
#             at          timestamptz NOT NULL DEFAULT now()
#         );
#         CREATE INDEX IF NOT EXISTS idx_audit_actor  ON audit_log(actor_id);
#         CREATE INDEX IF NOT EXISTS idx_audit_entity ON audit_log(entity_type, entity_id);

#         """
#             )
            
#             #CREATE TABLE reports IF NOT EXISTS
#             self.cursor.execute(
#         """CREATE TABLE IF NOT EXISTS reports (
#             id           uuid PRIMARY KEY DEFAULT gen_random_uuid(),
#             reporter_id  uuid NOT NULL REFERENCES users(id) ON DELETE CASCADE,
#             target_type  text NOT NULL,          -- 'USER' | 'EVENT' | 'APPLICATION'
#             target_id    uuid NOT NULL,
#             reason       text NOT NULL,
#             created_at   timestamptz NOT NULL DEFAULT now(),
#             resolved_by  uuid REFERENCES users(id),
#             resolved_at  timestamptz
#         );
#         CREATE INDEX IF NOT EXISTS idx_reports_reporter ON reports(reporter_id);
#         CREATE INDEX IF NOT EXISTS idx_reports_target   ON reports(target_type, target_id);
#         """
#             )
            
#             #CREATE TABLE consents IF NOT EXISTS
#             self.cursor.execute(
#         """CREATE TABLE IF NOT EXISTS consents (
#             user_id         uuid PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
#             email_marketing boolean NOT NULL DEFAULT false,
#             data_sharing    boolean NOT NULL DEFAULT false,
#             updated_at      timestamptz NOT NULL DEFAULT now()
#         );
#         """
#             )
            
#             logger.info("All tables ensured")
            
#             #CREATE helpful Views
#             self.cursor.execute(
#         """
#             CREATE OR REPLACE VIEW event_application_counts AS
#             SELECT
#             e.id AS event_id,
#             COUNT(*) FILTER (WHERE a.status = 'PENDING')  AS pending_count,
#             COUNT(*) FILTER (WHERE a.status = 'APPROVED') AS approved_count,
#             COUNT(*) FILTER (WHERE a.status = 'REJECTED') AS rejected_count
#             FROM events e
#             LEFT JOIN applications a ON a.event_id = e.id
#             GROUP BY e.id;

#             CREATE OR REPLACE VIEW applicant_status_summary AS
#             SELECT
#             u.id AS user_id,
#             COUNT(*) FILTER (WHERE a.status = 'PENDING')   AS pending_count,
#             COUNT(*) FILTER (WHERE a.status = 'APPROVED')  AS approved_count,
#             COUNT(*) FILTER (WHERE a.status = 'REJECTED')  AS rejected_count,
#             COUNT(*) FILTER (WHERE a.status = 'CANCELLED') AS cancelled_count
#             FROM users u
#             LEFT JOIN applications a ON a.applicant_id = u.id
#             GROUP BY u.id;
#         """
#             )
#             self.connection.commit()
#             logger.info("Views created or replaced")
#             data_temp = self.cursor.execute(
#                 """
#                 SELECT * FROM users
#                 """
#             )
#             logger.info(f"Sample data fetched: {data_temp}")
            
            
#         except Exception as e:
#             # re-raise to make failures visible during startup
#             raise
#         self._initialized = True
    

#     async def execute_query(self, query: str):
#         try:
#             data = await self.cursor.execute(query)
#             await self.connection.commit()
#             return data
#         except Exception as e:
#             logger.error(f"Error executing query: {e}")
#             await self.connection.rollback()
#             return None
        
#     async def fetch_one(self, query: str, params: tuple = ()):
#         try:
#             await self.cursor.execute(query, params)
#             return await self.cursor.fetchone()
#         except Exception as e:
#             logger.error(f"Error fetching one: {e}")
#             return None

#     # Synchronous helpers for blocking psycopg2 usage from sync endpoints
#     def execute_query_sync(self, query: str, params: tuple = ()): 
#         try:
#             self.cursor.execute(query, params)
#             # try to fetch rows if any
#             if self.cursor.description:
#                 cols = [d.name if hasattr(d, 'name') else d[0] for d in self.cursor.description]
#                 rows = self.cursor.fetchall()
#                 self.connection.commit()
#                 return [dict(zip(cols, r)) for r in rows]
#             else:
#                 self.connection.commit()
#                 return []
#         except Exception as e:
#             logger.error(f"Error executing query sync: {e}")
#             try:
#                 self.connection.rollback()
#             except Exception:
#                 pass
#             return None

#     def fetch_one_sync(self, query: str, params: tuple = ()): 
#         try:
#             self.cursor.execute(query, params)
#             row = self.cursor.fetchone()
#             if row and self.cursor.description:
#                 cols = [d.name if hasattr(d, 'name') else d[0] for d in self.cursor.description]
#                 return dict(zip(cols, row))
#             return None
#         except Exception as e:
#             logger.error(f"Error fetching one sync: {e}")
#             try:
#                 self.connection.rollback()
#             except Exception:
#                 pass
#             return None
# db = DataBase()
# logger.info("Database instance created")

import threading
import psycopg2
import logging
from ..config.env import ENV, env_settings
from ..config.logger import logger

logger=logging.getLogger('_name_')
logger.info("Initializing database connection...")

class DataBase:
    """Thread-safe singleton that holds a persistent psycopg2 connection.

    Notes:
    - _new_ ensures only one instance is created.
    - _init_ is guarded by _initialized so initialization happens once.
    - Do not use a with psycopg2.connect(...) as conn: here because that
      closes the connection at the end of the with-block; we want a
      persistent connection stored on the instance.
    """

    _instance = None
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._instance_lock:
                if cls._instance is None:
                    cls._instance = super(DataBase, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        # run initialization only once
        if getattr(self, "_initialized", False):
            return
        self.env = ENV()
        try:
            # keep connection open on the instance (don't use with)
            self.connection = psycopg2.connect(self.env.get_db_url())
            self.cursor = self.connection.cursor()
            logger.info("Database connected successfully")
            
            
            # --- C2C SCHEMA START ---
            
            # 0. ENUMS (Tạo trước bảng users để dùng cho cột type)
            # Lưu ý: Nếu enum đã tồn tại với giá trị 'BOTH', bạn cần drop và tạo lại trong DB thực tế
            # hoặc dùng ALTER TYPE. Ở đây là code khởi tạo cho môi trường mới.
            self.cursor.execute(
        """
        DO $$ BEGIN 
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'user_type') THEN
                CREATE TYPE user_type AS ENUM ('STUDENT', 'ORGANIZER');
            END IF;
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'event_status') THEN
                CREATE TYPE event_status AS ENUM ('draft','published','cancelled','completed');
            END IF;
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'application_status') THEN
                CREATE TYPE application_status AS ENUM ('applied','approved','rejected','withdrawn','attended','absent');
            END IF;
        END $$;
        """
            )
            # USERS table
            self.cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id            uuid PRIMARY KEY DEFAULT gen_random_uuid(),
            email         text NOT NULL UNIQUE,
            password_hash text NOT NULL,
            full_name     text,
            phone         text,
            type          user_type NOT NULL, -- type collumn using ENUM user_type
            is_active     boolean NOT NULL DEFAULT true,
            created_at    timestamptz NOT NULL DEFAULT now(),
            updated_at    timestamptz NOT NULL DEFAULT now()
        );\
        """
            )
            # STUDENTS table
            self.cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS students (
            user_id           uuid PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
            student_no        text NOT NULL UNIQUE,
            social_work_days  numeric(5,2) NOT NULL DEFAULT 0 CHECK (social_work_days >= 0)
        );
        """
            )
            # ORGANIZERS table
            self.cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS organizers (
            user_id      uuid PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
            organizer_no text NOT NULL UNIQUE,
            org_name     text
        );
        """
            )
            
            # EVENTS table
            self.cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS events (
            id                 uuid PRIMARY KEY DEFAULT gen_random_uuid(),
            organizer_user_id  uuid NOT NULL REFERENCES organizers(user_id) ON DELETE RESTRICT,
            title              text NOT NULL,
            description        text,
            location           text,
            status             event_status NOT NULL DEFAULT 'draft',
            created_at         timestamptz NOT NULL DEFAULT now(),
            updated_at         timestamptz NOT NULL DEFAULT now()
        );
        CREATE INDEX IF NOT EXISTS idx_events_org ON events(organizer_user_id);
        """
            )
            # EVENT_SLOTS table
            self.cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS event_slots (
            id         uuid PRIMARY KEY DEFAULT gen_random_uuid(),
            event_id   uuid NOT NULL REFERENCES events(id) ON DELETE CASCADE,
            work_date  DATE NOT NULL,
            starts_at  TIME NOT NULL,
            ends_at    TIME NOT NULL,
            capacity   int CHECK (capacity IS NULL OR capacity > 0),
            day_reward numeric(4,2) NOT NULL DEFAULT 1 CHECK (day_reward >= 0),

            UNIQUE (event_id, work_date, starts_at, ends_at),
            CHECK (ends_at > starts_at)
        );
        """
            )
            # APPLICATIONS table
            self.cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS applications (
            event_id         uuid NOT NULL REFERENCES events(id) ON DELETE CASCADE,
            student_user_id  uuid NOT NULL REFERENCES students(user_id) ON DELETE CASCADE,
            slot_id          uuid REFERENCES event_slots(id) ON DELETE SET NULL,
            note             text,
            status           application_status NOT NULL DEFAULT 'applied',
            created_at       timestamptz NOT NULL DEFAULT now(),
            decided_by       uuid REFERENCES organizers(user_id) ON DELETE SET NULL,
            decided_at       timestamptz,
            reason           text,
            updated_at       timestamptz NOT NULL DEFAULT now(),
            PRIMARY KEY (event_id, student_user_id)
        );
        CREATE INDEX IF NOT EXISTS idx_applications_student ON applications(student_user_id);
        CREATE INDEX IF NOT EXISTS idx_applications_event   ON applications(event_id);
        """
            )
            # STUDENT_SAVED_EVENTS (bookmark)
            self.cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS student_saved_events (
            student_user_id  uuid NOT NULL REFERENCES students(user_id) ON DELETE CASCADE,
            event_id         uuid NOT NULL REFERENCES events(id)        ON DELETE CASCADE,
            saved_at         timestamptz NOT NULL DEFAULT now(),
            PRIMARY KEY (student_user_id, event_id)
        );
        """
            )
            # NOTIFICATIONS
            self.cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS notifications (
            id             uuid PRIMARY KEY DEFAULT gen_random_uuid(),
            type           text NOT NULL,
            payload        jsonb,
            is_read        boolean NOT NULL DEFAULT false,
            created_at     timestamptz NOT NULL DEFAULT now(),
            sender_user_id   uuid REFERENCES users(id) ON DELETE SET NULL,
            receiver_user_id uuid REFERENCES users(id) ON DELETE CASCADE,
            event_id       uuid REFERENCES events(id) ON DELETE SET NULL
        );
        CREATE INDEX IF NOT EXISTS idx_notifications_to ON notifications(receiver_user_id, is_read);
        """
            )
            # AUDIT_LOGS
            self.cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS audit_logs (
            id              bigserial PRIMARY KEY,
            actor_user_id   uuid REFERENCES users(id) ON DELETE SET NULL,
            action          text NOT NULL,
            entity_type     text NOT NULL,
            entity_id       text,
            meta            jsonb,
            created_at      timestamptz NOT NULL DEFAULT now()
        );
        CREATE INDEX IF NOT EXISTS idx_audit_entity ON audit_logs(entity_type, entity_id);
        CREATE INDEX IF NOT EXISTS idx_audit_actor  ON audit_logs(actor_user_id);
        """
            )
            # CONSENTS
            self.cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS consents (
            user_id         uuid PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
            email_marketing boolean NOT NULL DEFAULT false,
            data_sharing    boolean NOT NULL DEFAULT false,
            updated_at      timestamptz NOT NULL DEFAULT now()
        );
        """
            )
            logger.info("All tables ensured (c2c schema)")
            self.connection.commit()
            
            
        except Exception as e:
            # re-raise to make failures visible during startup
            raise
        self._initialized = True
    

    async def execute_query(self, query: str):
        try:
            data = await self.cursor.execute(query)
            await self.connection.commit()
            return data
        except Exception as e:
            logger.error(f"Error executing query: {e}")
            await self.connection.rollback()
            return None
        
    async def fetch_one(self, query: str, params: tuple = ()):
        try:
            await self.cursor.execute(query, params)
            return await self.cursor.fetchone()
        except Exception as e:
            logger.error(f"Error fetching one: {e}")
            return None

    # Synchronous helpers for blocking psycopg2 usage from sync endpoints
    def execute_query_sync(self, query: str, params: tuple = ()): 
        try:
            self.cursor.execute(query, params)
            # try to fetch rows if any
            if self.cursor.description:
                cols = [d.name if hasattr(d, 'name') else d[0] for d in self.cursor.description]
                rows = self.cursor.fetchall()
                self.connection.commit()
                return [dict(zip(cols, r)) for r in rows]
            else:
                self.connection.commit()
                return []
        except Exception as e:
            logger.error(f"Error executing query sync: {e}")
            try:
                self.connection.rollback()
            except Exception:
                pass
            return None

    def fetch_one_sync(self, query: str, params: tuple = ()): 
        try:
            self.cursor.execute(query, params)
            row = self.cursor.fetchone()
            if row and self.cursor.description:
                cols = [d.name if hasattr(d, 'name') else d[0] for d in self.cursor.description]
                return dict(zip(cols, row))
            return None
        except Exception as e:
            logger.error(f"Error fetching one sync: {e}")
            try:
                self.connection.rollback()
            except Exception:
                pass
            return None
db = DataBase()
logger.info("Database instance created")