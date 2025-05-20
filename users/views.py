from fastapi import APIRouter

from users import crud
from users.schemas import AccountCreate

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post("/")
def create_user(user: AccountCreate):
    return crud.create_account(account_in=user)