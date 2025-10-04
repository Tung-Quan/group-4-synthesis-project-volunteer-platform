import fastapi 
from dotenv import load_dotenv,dotenv_values
import psycopg2
import os
import logging
import bcrypt
from fastapi import FastAPI
from pydantic import BaseModel

load_dotenv()


# Set up logging as [ Date-Time ]  [ Level ]  [ Module ]  Message
LOG_FORMAT = "[ %(asctime)s ]  [ %(levelname)s ]  %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT, datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger(__name__)


class ENV:
    #read .env in the root directory
    #load .env variables into ENV class attributes
    #for example, ENV.DB_HOST = os.getenv("DB_HOST")
    
    def __init__(self):
        self.DATABASE_USER = dotenv_values(".env").get("DATABASE_USER")
        self.DATABASE_PASSWORD = dotenv_values(".env").get("DATABASE_PASSWORD")
        self.DATABASE_HOST = dotenv_values(".env").get("DATABASE_HOST")
        self.DATABASE_NAME = dotenv_values(".env").get("DATABASE_NAME")
        self.PORT = dotenv_values(".env").get("PORT", 8000)
    
    def get_db_url(self):
        return f"postgresql://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}/{self.DATABASE_NAME}?sslmode=require&channel_binding=require"
    
    def get_port(self):
        return int(self.PORT)
    
    
# initialize database connection and use instance pattern for this class
import threading


class DataBase:
    """Thread-safe singleton that holds a persistent psycopg2 connection.

    Notes:
    - __new__ ensures only one instance is created.
    - __init__ is guarded by _initialized so initialization happens once.
    - Do not use a `with psycopg2.connect(...) as conn:` here because that
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
            # keep connection open on the instance (don't use `with`)
            self.connection = psycopg2.connect(self.env.get_db_url())
            self.cursor = self.connection.cursor()
            logger.info("Database connected successfully")
            
            
            #CREATE DATABASE ENUMS
            self.cursor.execute(
        """
        DO $$ BEGIN 
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'user_type') THEN
                CREATE TYPE user_type AS ENUM ('STUDENT', 'ORGANIZER', 'BOTH');
            END IF;
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'event_status') THEN
                CREATE TYPE event_status AS ENUM ('OPEN', 'CLOSED', 'ARCHIVED');
            END IF;
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'app_status') THEN
                CREATE TYPE app_status AS ENUM ('PENDING', 'APPROVED', 'REJECTED', 'CANCELLED');
            END IF;
        END $$;
        """
            )
            logger.info("Enums ensured")
            
            #CREATE TABLES users IF NOT EXISTS
            self.cursor.execute(
        """
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
        """
            )
            
            
            #CREATE TABLES events IF NOT EXISTS
            self.cursor.execute(
        """
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
        """
            )
            
            #CREATE TABLES applications IF NOT EXISTS
            self.cursor.execute(
        """CREATE TABLE IF NOT EXISTS applications (
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
        """
            )
            
            #CREATE TABLES tags IF NOT EXISTS
            self.cursor.execute(
        """CREATE TABLE IF NOT EXISTS tags (
            id   uuid PRIMARY KEY DEFAULT gen_random_uuid(),
            name text NOT NULL UNIQUE
        );
        """
            )
            
            #CREATE TABLES event_tags IF NOT EXISTS
            self.cursor.execute(
        """CREATE TABLE IF NOT EXISTS event_tags (
            event_id uuid NOT NULL REFERENCES events(id) ON DELETE CASCADE,
            tag_id   uuid NOT NULL REFERENCES tags(id)   ON DELETE CASCADE,
            CONSTRAINT pk_event_tags PRIMARY KEY (event_id, tag_id)
        );
        CREATE INDEX IF NOT EXISTS idx_event_tags_event ON event_tags(event_id);
        CREATE INDEX IF NOT EXISTS idx_event_tags_tag   ON event_tags(tag_id);
        """ 
            )
            
            
            #CREATE TABLES event_slots IF NOT EXISTS
            self.cursor.execute(
        """CREATE TABLE IF NOT EXISTS event_slots (
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
        """
            )
            
            #CREATE TABLES saved_events IF NOT EXISTS
            self.cursor.execute(
        """CREATE TABLE IF NOT EXISTS saved_events (
            user_id  uuid NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            event_id uuid NOT NULL REFERENCES events(id) ON DELETE CASCADE,
            saved_at timestamptz NOT NULL DEFAULT now(),
            CONSTRAINT pk_saved_events PRIMARY KEY (user_id, event_id)
        );
        """
            )
            
            #CREATE TABLE notifications IF NOT EXISTS
            self.cursor.execute(
        """CREATE TABLE IF NOT EXISTS notifications (
            id         uuid PRIMARY KEY DEFAULT gen_random_uuid(),
            user_id    uuid NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            type       text NOT NULL,    -- 'APP_APPROVED' | 'APP_REJECTED' | 'SYSTEM' ...
            payload    jsonb,
            is_read    boolean NOT NULL DEFAULT false,
            created_at timestamptz NOT NULL DEFAULT now()
        );
        CREATE INDEX IF NOT EXISTS idx_notifications_user    ON notifications(user_id);
        CREATE INDEX IF NOT EXISTS idx_notifications_is_read ON notifications(is_read);
        """
            )
            
            #CREATE TABLE audit_logs IF NOT EXISTS
            self.cursor.execute(
        """CREATE TABLE IF NOT EXISTS audit_log (
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

        """
            )
            
            #CREATE TABLE reports IF NOT EXISTS
            self.cursor.execute(
        """CREATE TABLE IF NOT EXISTS reports (
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
        """
            )
            
            #CREATE TABLE consents IF NOT EXISTS
            self.cursor.execute(
        """CREATE TABLE IF NOT EXISTS consents (
            user_id         uuid PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
            email_marketing boolean NOT NULL DEFAULT false,
            data_sharing    boolean NOT NULL DEFAULT false,
            updated_at      timestamptz NOT NULL DEFAULT now()
        );
        """
            )
            
            logger.info("All tables ensured")
            
            #CREATE helpful Views
            self.cursor.execute(
        """
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
        """
            )
            
            logger.info("Views created or replaced")
            
            
        except Exception as e:
            # re-raise to make failures visible during startup
            raise
        self._initialized = True
    

    def execute_query(self, query: str):
        try:
            data = self.cursor.execute(query)
            self.connection.commit()

            if len(data) == 0:
                logger.info("No data found.")
                return []
            
            return data
        except Exception as e:
            logger.error(f"Error executing query: {e}")
            self.connection.rollback()
            return None
    

# Create a global database instance
db = DataBase()
logger.info("Database instance created")


app = fastapi.FastAPI()
# DEFINE USERS REALTED APIs
class LoginRequest(BaseModel):
    email: str
    password: str


@app.post("/api/login")
def login(request: LoginRequest):
    query = f"SELECT password_hash FROM users WHERE email = '{request.email}'"
    user = db.execute_query(query)
    if user and bcrypt.checkpw(request.password.encode('utf-8'), user[0]['password_hash'].encode('utf-8')):
        return {"message": "Login successful"}
    return {"message": "Invalid email or password"}, 401

  
class ProfileRequest(BaseModel):
    user_id: str
    
@app.get("/api/profile")
def profile(request: ProfileRequest):
    query = f"SELECT id, email, display_name, type, is_active, created_at, updated_at FROM users WHERE id = '{request.user_id}'"
    user = db.execute_query(query)
    if user:
        return {"user": user[0]}, 200
    return {"message": "User not found"}, 404



# EVENT APIs
@app.get("/api/events")
def events():
    query = "SELECT id, title, description, start_time, end_time, location FROM events"
    events = db.execute_query(query)
    if events:
        return {"events": events}, 200
    return {"message": "No events found"}, 404

class createEventRequest(BaseModel):
    title: str
    description: str
    location: str
    starts_at: str  # ISO 8601 format
    ends_at: str    # ISO 8601 format
    capacity: int
    organizer_id: str
@app.post("/api/envents")
def create_event(request: createEventRequest):
    query = f"""
    INSERT INTO events (title, description, location, starts_at, ends_at, capacity, created_by)
    VALUES ('{request.title}', '{request.description}', '{request.location}', '{request.starts_at}', '{request.ends_at}', {request.capacity}, '{request.organizer_id}')
    RETURNING id;
    """
    event_id = db.execute_query(query)
    if event_id:
        return {"message": "Event created successfully", "event_id": event_id[0]['id']}, 201
    return {"message": "Failed to create event"}, 500

class UpdateEventRequest(BaseModel):
    event_id: str
    title: str
    description: str
    location: str
    starts_at: str  # ISO 8601 format
    ends_at: str    # ISO 8601 format
    capacity: int
    organizer_id: str
@app.put("/api/events")
def update_event(request: UpdateEventRequest):
    query = f"""
    SELECT created_by FROM events WHERE id = '{request.event_id}';
    """
    
    event = db.execute_query(query)
    if not event:
        return {"message": "Event not found"}, 404
    if event[0]['created_by'] != request.organizer_id:
        return {"message": "Unauthorized"}, 403

    query = f"""
    UPDATE events
    SET title = '{request.title}',
        description = '{request.description}',
        location = '{request.location}',
        starts_at = '{request.starts_at}',
        ends_at = '{request.ends_at}',
        capacity = {request.capacity},
        updated_at = now()
    WHERE id = '{request.event_id}';
    """
    
    success = db.execute_query(query)
    if success is not None:
        return {"message": "Event updated successfully"}, 200
    
    return {"message": "Failed to update event"}, 500
    
