from datetime import datetime
from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from auth.utils import encode_jwt, decode_jwt, validate_password
from users.schemas import AccountCreate, AccountResponse
from core.models import Account
from core.models.db_helper import db_helper
from users.crud import get_account_by_name

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/jwt/login/")

class TokenInfo(BaseModel):
    access_token: str
    token_type: str

router = APIRouter(prefix="/jwt", tags=["JWT"])

async def validate_auth_user(
    username: str = Form(...),
    password: str = Form(...),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> Account:
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
    )

    account = await get_account_by_name(session, username)
    if not account or not validate_password(password, account.password):
        raise unauthed_exc

    if not account.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account inactive",
        )

    return account

@router.post("/login/", response_model=TokenInfo)
async def login(
    account: Account = Depends(validate_auth_user),
):
    token = encode_jwt(
        user_id=account.id,  # Используем ID вместо username
        additional_payload={
            "username": account.username,
            "admin": account.admin
        }
    )
    return {"access_token": token, "token_type": "Bearer"}

async def get_current_account(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> Account:
    try:
        payload = decode_jwt(token)
        account_id = int(payload["sub"])  # Получаем ID из sub
    except (InvalidTokenError, KeyError, ValueError) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {e}",
        )

    account = await session.get(Account, account_id)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found",
        )

    if not account.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account inactive",
        )

    return account

@router.get("/accounts/me/", response_model=AccountResponse)
async def read_account_me(
    account: Depends(get_current_account),
):
    return AccountResponse.model_validate(account)