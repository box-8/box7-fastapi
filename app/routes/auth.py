from fastapi import APIRouter, Response, Cookie, Request
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from app.auth.auth import (
    login_user,
    register_user,
    logout_user,
    check_auth_status,
    get_current_user_info
)
from app.models.user import UserLogin, UserRegistration

# Configuration du router
router = APIRouter()

def add_cors_headers(response: Response, request: Request):
    origin = request.headers.get("origin")
    allowed_origins = [
        "https://box7-react-68938d4bd5ee.herokuapp.com",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]
    if origin in allowed_origins:
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Credentials"] = "true"
    return response

@router.post("/login")
async def login(request: Request, response: Response, user_data: UserLogin):
    """Endpoint de login qui retourne un token JWT et crée une session"""
    result = await login_user(response, user_data)
    return add_cors_headers(response, request)

@router.post("/register")
async def register(request: Request, response: Response, user_data: UserRegistration):
    """Endpoint d'enregistrement d'un nouvel utilisateur"""
    result = await register_user(user_data)
    response.status_code = 201
    return add_cors_headers(response, request)

@router.post("/logout")
async def logout(request: Request, response: Response, session: Optional[str] = Cookie(None)):
    """Endpoint de déconnexion qui supprime la session"""
    result = await logout_user(response, session)
    return add_cors_headers(response, request)

@router.get("/check-auth")
async def check_auth(request: Request, response: Response, session: Optional[str] = Cookie(None)):
    """Vérifie si l'utilisateur est authentifié via le cookie de session"""
    result = await check_auth_status(session)
    return add_cors_headers(response, request)

@router.get("/me")
async def read_users_me(request: Request, response: Response, session: Optional[str] = Cookie(None)):
    """Récupère les informations de l'utilisateur connecté"""
    result = await get_current_user_info(session)
    return add_cors_headers(response, request)
