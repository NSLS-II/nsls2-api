import fastapi
import re

import ldap3.utils.dn
from fastapi import Depends

from models.users import User, DataAdmins
from services import bnlpeople_service
from services import pass_service
from services import n2sn_service

from N2SNUserTools.ldap import ADObjects

from infrastucture import settings

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


@router.get('/user/{username}/data-admin-rights', response_model=DataAdmins)
async def get_user_dataadmin_rights(username: str):
    userinfo = await n2sn_service.get_groups_by_username_sync(username)
    # For now, I am assuming the first account returned is the one we want
    # TODO: Make the logic of matching multiple accounts better
    ldapgrouplist = userinfo[0]['memberOf']

    # Extract the groups
    grouplist = []
    for group in ldapgrouplist:
        cn = ldap3.utils.dn.parse_dn(group)[0][1]
        grouplist.append(cn)

    # Cull the list to those we care about
    dagrouplist = [x for x in grouplist if re.search("dataadmin", x)]

    response = {}

    # Check for facility data admins
    if 'n2sn-dataadmin' in dagrouplist:
        response['nsls2_dataadmin'] = True
        response['lbms_dataadmin'] = True

    if 'nsls2-dataadmin' in dagrouplist:
        response['nsls2_dataadmin'] = True

    if 'lbms-dataadmin' in dagrouplist:
        response['lbms_dataadmin'] = True

    return response
# 1
#
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
