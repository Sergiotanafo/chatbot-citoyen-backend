"""
app/api/auth.py
Contrôleur HTTP pour l'authentification et l'inscription des administrateurs.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.auth import Token, UserCreate, UserResponse
from app.repositories.user_repository import UserRepository
from app.security.auth import verify_password, create_access_token
from app.security.deps import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentification"])


@router.post("/login", response_model=Token, summary="Connexion et obtention du jeton JWT")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_repo = UserRepository(db)
    user = user_repo.get_by_username(form_data.username)

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nom d'utilisateur ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.username, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=UserResponse, summary="Création d'un compte utilisateur")
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    user_repo = UserRepository(db)
    if user_repo.get_by_username(user_in.username):
        raise HTTPException(status_code=400, detail="Ce nom d'utilisateur est déjà utilisé")

    return user_repo.create(user_in)


@router.get("/me", response_model=UserResponse, summary="Informations sur le compte connecté")
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

