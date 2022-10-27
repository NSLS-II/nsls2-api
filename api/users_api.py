import json

import fastapi
import re
from typing import List, Optional
import ldap3.utils.dn
from fastapi import Depends, Header
from pymongo import MongoClient

from models.users import User, DataAdmins, DataSessionAccess
from services import bnlpeople_service
from services import n2sn_service

from N2SNUserTools.ldap import ADObjects
from infrastucture import settings

client = MongoClient(settings.NSLS2CORE_MONGODB_URI)

router = fastapi.APIRouter()


def get_facility_dataadmin_roles(username: str):
    database = client["nsls2core"]
    collection = database["facilities"]
    query = {}
    query["data_admins"] = {
        "$elemMatch": {
            "$eq": username
        }
    }
    projection = {"id": 1}

    result = collection.find(query, projection=projection)
    facility_list = []
    for doc in result:
        facility_list.append(str(doc['id']))
    return facility_list


def get_beamline_dataadmin_roles(username: str):
    database = client["nsls2core"]
    collection = database["beamlines"]
    query = {}
    query["data_admins"] = {
        "$elemMatch": {
            "$eq": username
        }
    }
    projection = {"name": 1}

    result = collection.find(query, projection=projection)
    beamline_list = []
    for doc in result:
        beamline_list.append(str(doc['name']).lower())
    return beamline_list


def get_datasessions_for_username(username: str):
    database = client["nsls2core"]
    collection = database["proposals"]
    result = collection.find({
        "users": {
            "$elemMatch": {
                "username": username
            }
        }
    },
        {
            "data_session": 1.0
        })

    datasession_list = []
    for doc in result:
        datasession_list.append(str(doc['data_session']))
    return datasession_list


#@router.get('/users/me')
async def get_current_user(x_remote_user: Optional[str] = Header(None)):
    user_info = {"upn": x_remote_user}

    return user_info


# @router.get('/users')
# def get_users(person: User):
#     pass


#@router.get('/users/{username}', response_model=User)
async def get_user_by_username(person: User = Depends()):
    ad_person = await n2sn_service.get_user_by_username_async(person.username)

    bnl_person = await bnlpeople_service.get_person_by_username_async(person.username)

    # pass_person = await pass_service.get_user(person.username)
    # person.username = bnl_person['ActiveDirectoryName']
    # person.first_name = bnl_person[0]['FirstName']
    # person.last_name = bnl_person[0]['LastName']
    # person.email = bnl_person[0]['BNLEmail']
    # person.life_number = bnl_person[0]['EmployeeNumber']

    user = User(username=ad_person[0]['sAMAccountName'],
                email=ad_person[0]['mail'],
                life_number=ad_person[0]['employeeID'])
    return user


@router.get('/users/{bnl_id}', response_model=User)
async def get_user_by_life_number(person: User = Depends()):
    ad_person = await n2sn_service.get_user_by_id_async(person.life_number)

    # pass_person = await pass_service.get_user(person.username)
    # person.username = bnl_person['ActiveDirectoryName']
    # person.first_name = bnl_person[0]['FirstName']
    # person.last_name = bnl_person[0]['LastName']
    # person.email = bnl_person[0]['BNLEmail']
    # person.life_number = bnl_person[0]['EmployeeNumber']

    user = User(username=ad_person[0]['sAMAccountName'],
                email=ad_person[0]['mail'],
                life_number=ad_person[0]['employeeID'])
    return user


# Commented out because it's very slow at the moment
# @router.get('/users/{username}/proposals')
# async def get_proposals_by_username(person: User = Depends()):
#     person = await n2sn_service.get_user_by_username_async(person.username)
#     proposals = await pass_service.get_proposals_by_person(person[0]['employeeID'])
#     return proposals


@router.get('/data_session/{username}', response_model=DataSessionAccess)
async def get_datasessions_by_username(person: User = Depends()):
    facility_admin = get_facility_dataadmin_roles(person.username)
    beamline_admin = get_beamline_dataadmin_roles(person.username)
    datasession_list = get_datasessions_for_username(person.username)
    # print(f"{person.username} is a data admin for the following facilities: {facility_admin}")
    dataaccess = DataSessionAccess(all_access=False, data_sessions=datasession_list,
                                   facility_all_access=facility_admin,
                                   beamline_all_access=beamline_admin)
    return dataaccess


#@router.get('/user/{username}/data-admin-rights', response_model=DataAdmins)
async def get_user_dataadmin_rights(username: str):
    userinfo = await n2sn_service.get_groups_by_username_async(username)
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
    if 'n2sn-right-dataadmin' in dagrouplist:
        response['nsls2_dataadmin'] = True
        response['lbms_dataadmin'] = True

    if 'nsls2-right-dataadmin' in dagrouplist:
        response['nsls2_dataadmin'] = True

    if 'lbms-right-dataadmin' in dagrouplist:
        response['lbms_dataadmin'] = True

    beamline_dataadmin = []

    # TODO: this is not the place to do it... but for now
    f = open("beamlines.yml")
    beamlines = json.load(f)
    for beamline in beamlines:
        tla = str(beamline['name']).lower()
        datagroup_name = f"n2sn-right-dataadmin-{tla}"
        if n2sn_service.is_user_in_group(username, datagroup_name):
            beamline_dataadmin.append(tla)

    response['dataadmin'] = beamline_dataadmin

    return response

