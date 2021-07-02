import fastapi
from fastapi import Depends

from models.users import Username
from services import bnlpeople_service

router = fastapi.APIRouter()

@router.get('/users')
def get_users():
    pass

@router.get('/user/{username}')
async def get_user_by_username(person: Username = Depends()):
    person = await bnlpeople_service.get_person_by_username_async(person.username)
    return person

@router.get('/user/me')
def get_current_user():
    pass

