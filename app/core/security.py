from passlib.hash import bcrypt 
from datetime import datetime ,timedelta,timezone
from uuid import UUID
import jwt
from jwt.expections import ExpiredSignatureError,InvalidTokenError
from app.config import settings
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
def hash_password(plain_password:str)  -> str:
    """One-directional: produces a hash containing an embedded random
    salt. Never call this to 'check' a password — only to store one."""
    hashed = bcrypt.hashpw(
        plain_password.encode("utf-8"),
        bcrypt.gensalt(),
    )
    return hashed.decode("utf-8")
def verify_password(plain_password:str, hashed_password: str)->str:
    """Re-hashes the attempt using the salt embedded in hashed_password,
    then compares — this is what actually checks a login, never a
    manual == comparison of two hashes."""
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8"),
    )

## JWT access token
def create_access_token(user_id: UUID)->str:
    expire = datetime.now(timezone.utc)+timedelta(
        minutes = ACCESS_TOKEN_EXPIRE_MINUTES
    )
    payload = {
        "sub":str(user_id),
        "exp":expire,
    }
    return jwt.encode(payload,settings.JWT_SECRET_KEY,algorithm=ALGORITHM)
def decode_access_token(token:UUID)->str:
    """Verifies signature and expiration. Raises specific, catchable
    errors — the caller (a FastAPI dependency, later) decides how each
    one becomes an HTTP response; this function doesn't know about
    HTTP at all."""
    try:
        return jwt.decode(token,settings.JWT_SECRET_KEY,algorithm = [ALGORITHM])
    except ExpiredSignatureError:
        raise
    except InvalidTokenError:
        raise

 