import threading
import psycopg2
import logging
from ..config.env import ENV, env_settings
from ..config.logger import logger

logger = logging.getLogger('__name__')
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
        
        self._initialized = True
        self.connection = None

        self.connect() # Tách hàm connect ra riêng

    def connect(self):
        # Check if database environment variables are configured
        if not all([self.env.DATABASE_HOST, self.env.DATABASE_USER, self.env.DATABASE_NAME]):
            logger.warning(
                "Database environment variables not fully configured. Skipping database connection.")
            logger.warning(
                "Please set DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD, and DATABASE_NAME in your .env file")
            self.connection = None
            self.cursor = None
            self._initialized = True
            return

        try:
            # keep connection open on the instance (don't use with)
            self.connection = psycopg2.connect(self.env.get_db_url())
            # Use RealDictCursor to get results as dictionaries with proper column names
            from psycopg2.extras import RealDictCursor
            self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)
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
            approved   int DEFAULT 0,
            applied    int DEFAULT 0,

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
            PRIMARY KEY (event_id, student_user_id, slot_id)
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
            logger.error(f"Error connecting to database: {e}")
            self.connection = None
        # self._initialized = True
    
    # ----------- Func that ensure connection ---------
    def ensure_connection(self):
        """
        Check being connection to db or not
        """
        try:
            # Gửi lệnh ping nhẹ để test kết nối
            if self.connection and self.connection.closed == 0:
                with self.connection.cursor() as cur:
                    cur.execute("SELECT 1")
                return # Kết nối vẫn tốt
        except Exception:
            pass # Lỗi thì bỏ qua, xuống dưới reconnect
        
        # Nếu code chạy đến đây nghĩa là kết nối đã chết
        logger.warning("⚠️ Database connection lost. Reconnecting...")
        self.connect()
    # --------------------------------------------

    async def execute_query(self, query: str):
        # ------------------------------
        self.ensure_connection()
        if not self.connection: return None # Safety check
        # -----------------------------------------------

        try:
            data = await self.cursor.execute(query)
            await self.connection.commit()
            return data
        except Exception as e:
            logger.error(f"Error executing query: {e}")
            try:
                if self.connection: await self.connection.rollback()
            except: pass
            return None

    async def fetch_one(self, query: str, params: tuple = ()):
        # ------------------------------
        self.ensure_connection()
        if not self.connection: return None # Safety check
        # -----------------------------------------------
        try:
            await self.cursor.execute(query, params)
            return await self.cursor.fetchone()
        except Exception as e:
            logger.error(f"Error fetching one: {e}")
            return None

    # Synchronous helpers for blocking psycopg2 usage from sync endpoints
    def execute_query_sync(self, query: str, params: tuple = ()):
        """Execute a query and return all results. Creates a new cursor for thread safety."""
        # --- Auto Reconnect ---
        self.ensure_connection()
        # --------------------------------

        if not self.connection:
            logger.error("Database connection not initialized")
            return None

        from psycopg2.extras import RealDictCursor
        cursor = None
        try:
            # Create a new cursor for this operation (thread-safe)
            cursor = self.connection.cursor(cursor_factory=RealDictCursor)
            cursor.execute(query, params)
            # try to fetch rows if any
            if cursor.description:
                rows = cursor.fetchall()
                self.connection.commit()
                # RealDictCursor returns dict-like objects, convert to regular dicts
                return [dict(row) for row in rows]
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
        finally:
            if cursor:
                cursor.close()

    def fetch_one_sync(self, query: str, params: tuple = ()):
        """Fetch a single row. Creates a new cursor for thread safety."""
        # --- Auto Reconnect ---
        self.ensure_connection()
        # --------------------------------
        if not self.connection:
            logger.error("Database connection not initialized")
            return None

        from psycopg2.extras import RealDictCursor
        cursor = None
        try:
            # Create a new cursor for this operation (thread-safe)
            cursor = self.connection.cursor(cursor_factory=RealDictCursor)
            cursor.execute(query, params)
            row = cursor.fetchone()
            # RealDictCursor already returns a dict-like object, convert to regular dict
            if row:
                return dict(row)
            return None
        except Exception as e:
            logger.error(f"Error fetching one sync: {e}")
            try:
                self.connection.rollback()
            except Exception:
                pass
            return None
        finally:
            if cursor:
                cursor.close()


db = DataBase()
logger.info("Database instance created")
