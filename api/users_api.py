from typing import List

import fastapi

from models.users import User

router = fastapi.APIRouter()

@router.get('/users')
def get_all_users():
    pass

@router.get('/user/{username}')
def get_user_by_username():
    pass

@router.get('/user/me')
def get_current_user():
    pass

