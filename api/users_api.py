import fastapi
from fastapi import Depends

from models.users import User
from services import bnlpeople_service
from services import pass_service

router = fastapi.APIRouter()

@router.get('/users/me')
def get_current_user():
    # TODO: This requires auth to be implemented so we know who the current user is!
    return {"username": "currentuser"}


@router.get('/users')
def get_users(person: User):
    pass

@router.get('/users/{username}')
async def get_user_by_username(person: User = Depends()):
    bnl_person = await bnlpeople_service.get_person_by_username_async(person.username)
    pass_person = await pass_service.get_user(person.username)
    return person

#1
# @router.get('/user/{username}/data-admin-rights'}
#
#
# @router.get("/users/{username}/proposal/count")
#
# /users/{username}/proposals?beamline=bmm?CYCLE=
# --> list of proposals for that user
#
# cout = None
# peroposal =
# [
# {
#     proposal_id="",
#     cycle="",
#     data_session="", # implicit
#     beamline=""
# }
# ]
#
# #2
# /proposals/{proposalid}/users
# --> list of users for that proposal
#
# #3
# @router.post("/users/{username}/proposals")
# input: list of data_sessions : str
# return: list of ones I can see (from the input list)
#
#
#
#








