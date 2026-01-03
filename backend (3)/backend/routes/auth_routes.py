from datetime import datetime

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr, Field
from passlib.context import CryptContext
from passlib.exc import PasswordSizeError
from google.oauth2 import id_token
from google.auth.transport import requests

from db.user_model import create_user, get_user, update_last_login

router = APIRouter(prefix="/api/auth", tags=["Auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def _hash_password(password: str) -> str:
    try:
        return pwd_context.hash(password)
    except PasswordSizeError:
        raise HTTPException(
            status_code=400,
            detail="Password must be 72 characters or fewer. Please choose a shorter password.",
        )


def _verify_password(password: str, password_hash: str) -> bool:
    try:
        return pwd_context.verify(password, password_hash)
    except PasswordSizeError:
        raise HTTPException(
            status_code=400,
            detail="Password must be 72 characters or fewer. Please choose a shorter password.",
        )


class AuthInput(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=64)


class GoogleLoginInput(BaseModel):
    credential: str


def _serialize_user(user_doc):
    if not user_doc:
        return None
    return {
        "id": str(user_doc.get("_id")),
        "email": user_doc.get("email"),
        "created_at": user_doc.get("created_at"),
        "last_login": user_doc.get("last_login"),
    }


@router.post("/login")
def login_user(payload: AuthInput):
    try:
        user = get_user(payload.email)
        if user:
            password_hash = user.get("password_hash")
            if not password_hash or not _verify_password(payload.password, password_hash):
                raise HTTPException(status_code=401, detail="Invalid email or password.")

            now = datetime.utcnow()
            update_last_login(user["_id"], now)
            user["last_login"] = now
            return {"status": "success", "user": _serialize_user(user), "mode": "login"}

        # Create a new user (auto-register)
        password_hash = _hash_password(payload.password)
        new_user = create_user(payload.email, password_hash)
        if not new_user:
            raise HTTPException(status_code=503, detail="MongoDB is unavailable. Please try again later.")

        return {"status": "success", "user": _serialize_user(new_user), "mode": "register"}
    except PasswordSizeError:
        raise HTTPException(
            status_code=400,
            detail="Password must be 72 characters or fewer. Please choose a shorter password.",
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"[AUTH] Error: {e}")
        raise HTTPException(status_code=500, detail="Authentication failed. Please try again.")


@router.post("/google")
def login_google(payload: GoogleLoginInput):
    try:
        # Verify the token
        # Note: In a production app, you should also verify the 'aud' claim matches your Client ID.
        idinfo = id_token.verify_oauth2_token(payload.credential, requests.Request())

        email = idinfo.get("email")
        if not email:
            raise HTTPException(status_code=400, detail="Google token missing email")

        user = get_user(email)
        if user:
            now = datetime.utcnow()
            update_last_login(user["_id"], now)
            user["last_login"] = now
            return {"status": "success", "user": _serialize_user(user), "mode": "login"}

        # Create new user with no password (Google only)
        new_user = create_user(email, password_hash=None)
        if not new_user:
            raise HTTPException(status_code=503, detail="MongoDB is unavailable. Please try again later.")

        return {"status": "success", "user": _serialize_user(new_user), "mode": "register"}

    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid Google token")
    except Exception as e:
        print(f"[AUTH] Google Login Error: {e}")
        raise HTTPException(status_code=500, detail="Google authentication failed")

