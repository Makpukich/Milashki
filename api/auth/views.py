from fastapi import APIRouter, Depends, Form, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from jwt import InvalidTokenError
from pydantic import BaseModel

from auth.utils import encode_jwt, decode_jwt, validate_password, hash_password
from fastapi import APIRouter, Depends, Form, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from jwt import InvalidTokenError
from pydantic import BaseModel

from auth.utils import encode_jwt, decode_jwt, validate_password, hash_password
from users.schemas import AccountResponse, AccountCreate, AccountLogin
from core.models import Account
from core.models.db_helper import db_helper
from users.crud import get_account_by_name, create_account

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/jwt/login")


class TokenInfo(BaseModel):
    access_token: str
    token_type: str


class RegisterRequest(AccountCreate):
    pass


router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post("/register", response_model=AccountResponse)
async def register_user(
        account_in: AccountCreate,
        session: AsyncSession = Depends(db_helper.session_dependency),
) -> Account:
    existing = await get_account_by_name(session, account_in.username)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists",
        )
    account_in.password = hash_password(account_in.password)
    account = await create_account(session=session, account_in=account_in )

    return account


async def validate_auth_user(
        account_in: AccountLogin,
        session: AsyncSession = Depends(db_helper.session_dependency),
) -> Account:
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
    )
    account = await get_account_by_name(session, account_in.username)
    if not account:
        raise unauthed_exc

    if not validate_password(account_in.password, account.password):
        raise unauthed_exc

    if not account.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account inactive",
        )

    return account


@router.post("/login", response_model=TokenInfo)
async def login(
        account_in: AccountLogin,
        session: AsyncSession = Depends(db_helper.session_dependency),
):
    account = await validate_auth_user(
        account_in=account_in,
        session=session
    )

    jwt_payload = {
        "sub": str(account.id),
        "username": account.username,
        "admin": account.admin,
        "iat": datetime.utcnow(),
    }

    token = encode_jwt(jwt_payload)
    return {"access_token": token, "token_type": "Bearer"}


async def get_current_account(
        token: str = Depends(oauth2_scheme),
        session: AsyncSession = Depends(db_helper.session_dependency),
) -> Account:
    try:
        payload = decode_jwt(token)
        account_id = int(payload["sub"])
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


@router.get("/me", response_model=AccountResponse)
async def read_account_me(
        account: Account = Depends(get_current_account),
):
    return AccountResponse.model_validate(account)