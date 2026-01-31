from typing import Annotated, List
import jwt
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlalchemy import select

from .database import engine, Base, get_db
from .models import User
from .security import get_password_hash, verify_password, create_access_token
from .schemas import UserSchema, UserCreate, Token, UserDetails
from .config import settings

Base.metadata.create_all(bind=engine)

app = FastAPI(title="System z Rolami (RBAC)")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Nieprawidłowy token uwierzytelniający",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception

    user = db.get(User, user_id)
    if user is None:
        raise credentials_exception
    return user


def require_admin_role(current_user: User = Depends(get_current_user)):
    user_roles = current_user.roles.split(",")
    if "ROLE_ADMIN" not in user_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Brak uprawnień administratora (wymagana rola ROLE_ADMIN)"
        )
    return current_user


@app.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(
        user_data: UserCreate,
        db: Session = Depends(get_db),
        admin_user: User = Depends(require_admin_role)
):
    existing_user = db.scalar(select(User).where(User.email == user_data.email))
    if existing_user:
        raise HTTPException(status_code=400, detail="Email jest już zajęty")

    hashed_pw = get_password_hash(user_data.password)

    new_user = User(
        email=user_data.email,
        hashed_password=hashed_pw,
        roles=user_data.roles
    )
    db.add(new_user)
    db.commit()
    return {"message": f"Użytkownik {user_data.email} utworzony z rolami: {user_data.roles}"}


@app.post("/login", response_model=Token)
def login(user_data: UserSchema, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.email == user_data.email))

    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Niepoprawny email lub hasło",
        )

    roles_list = user.roles.split(",")

    access_token = create_access_token(
        data={
            "sub": user.id,
            "roles": roles_list
        }
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/user_details", response_model=UserDetails)
def get_user_details(token: str = Depends(oauth2_scheme)):
    try:
        # NAPRAWA: Używamy settings.secret_key zamiast starego SECRET_KEY
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return {
            "user_id": payload.get("sub"),
            "roles": payload.get("roles"),
            "exp": payload.get("exp")
        }
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nieprawidłowy token"
        )
