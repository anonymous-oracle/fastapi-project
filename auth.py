from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordBearer
import jwt
from fastapi.exceptions import HTTPException
from config import JWT_ALGORITHM, SECRET_KEY
from hashing import check_pwd
from crud import read_user


# `openssl rand -hex 32` -> to generate the secret
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def authenticate_user(username: str, password: str):
    user = await read_user(username=username)
    if user == None:
        return False
    if check_pwd(password, user.password, user.salt) == False:
        return False
    return user


def get_token(payload: dict):
    """payload: must be a dict object"""
    token = jwt.encode(payload=payload, key=SECRET_KEY, algorithm=JWT_ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, key=SECRET_KEY, algorithms=[JWT_ALGORITHM])
        user = await read_user(id=payload.get("id"))
    except:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return user
