from datetime import timedelta
from typing import Optional


def create_access_token(*args, **kwargs):
    raise NotImplementedError("create_access_token is implemented in backend.backend; this placeholder exists only for import-time compatibility")


def create_refresh_token(*args, **kwargs):
    raise NotImplementedError("create_refresh_token is implemented in backend.backend; this placeholder exists only for import-time compatibility")


def get_current_user():
    # Placeholder for dependency compatibility. Real implementation is in backend.backend
    raise NotImplementedError("Use backend.current_user instead")


def require_roles(*roles: str):
    # Provide a stub so imports succeed; backend defines a full require_roles
    def dep(user=None):
        raise NotImplementedError("Use backend.require_roles instead")
    return dep
