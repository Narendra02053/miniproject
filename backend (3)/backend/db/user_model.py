from datetime import datetime
from typing import Optional

from .connection import get_users_col


def _users():
    """Return the users collection if MongoDB is available."""
    return get_users_col()


def create_user(email: str, password_hash: Optional[str] = None) -> Optional[dict]:
    users_col = _users()
    if users_col is None:
        return None

    doc = {
        "email": email.lower(),
        "password_hash": password_hash,
        "created_at": datetime.utcnow(),
        "last_login": datetime.utcnow(),
    }
    result = users_col.insert_one(doc)
    doc["_id"] = result.inserted_id
    return doc


def get_user(email: str) -> Optional[dict]:
    users_col = _users()
    if users_col is None:
        return None
    return users_col.find_one({"email": email.lower()})


def update_last_login(user_id, timestamp: Optional[datetime] = None) -> None:
    users_col = _users()
    if users_col is None:
        return
    users_col.update_one({"_id": user_id}, {"$set": {"last_login": timestamp or datetime.utcnow()}})
