from fastapi import APIRouter, Depends, status, HTTPException, Request
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from core.config import settings
from schemas import user_schema
from services import auth_service
from db.deps import get_db

router = APIRouter()

@router.post(
    "/register",
    response_model=user_schema.User,
    status_code=status.HTTP_201_CREATED
)
async def create_user(
    user: user_schema.UserCreate,
    db: Session = Depends(get_db)
):
    """
    Endpoint pro registraci nového uživatele.
    - Přijme data odpovídající schématu UserCreate.
    - Zavolá servisní logiku pro vytvoření uživatele.
    - Vrátí data odpovídající schématu User (bez hesla).
    """
    return auth_service.create_user(db=db, user=user)


@router.post("/login", response_model=user_schema.Token)
async def login_for_access_token(
        user_credentials: user_schema.UserLogin,
        db: Session = Depends(get_db)
):
    """
    Endpoint pro přihlášení uživatele a získání JWT tokenu.
    """
    user = auth_service.authenticate_user(db, user_credentials)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nesprávné přihlašovací údaje",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = auth_service.create_access_token(
        data={"sub": user.email}
    )

    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/validate")
async def validate_token(request: Request):
    """
    Tento endpoint slouží POUZE pro interní ověření tokenu z API Gateway.
    Vrátí 200 OK, pokud je token platný, jinak 401.
    """
    token = None
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith('Bearer '):
        token = auth_header.split(" ")[1]

    if token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token not found")

    try:
        # Pokusíme se dekódovat token. Pokud selže (neplatný podpis, vypršel),
        # vyvolá se JWTError.
        jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    # Pokud dekódování projde, token je platný.
    return {"status": "ok"}