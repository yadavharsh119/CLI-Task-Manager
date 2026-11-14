from pwdlib import PasswordHash
import jwt
from datetime import timedelta, timezone, datetime
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from config import JWT_ALGORITHM, JWT_SECRET, TOKEN_EXPIRE_MINUTES

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return password_hash.verify(password, hashed)


def create_access_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    payload = {"sub": str(user_id), "exp": expire}
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user_id(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return int(payload["sub"])
    except Exception as e:
        print("JWT Error", type(e).__name__, e)
        raise HTTPException(status_code=401, detail="invalid or expired token")
