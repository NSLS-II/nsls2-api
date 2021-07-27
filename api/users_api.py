import fastapi
from fastapi import Depends

from models.users import User
from services import bnlpeople_service

router = fastapi.APIRouter()

@router.get('/users/me')
def get_current_user():
    return {"username": "currentuser"}

@router.get('/users')
def get_users(person: User):
    pass

@router.get('/users/{username}')
async def get_user_by_username(person: User = Depends()):
    person = await bnlpeople_service.get_person_by_username_async(person.username)
    return person



