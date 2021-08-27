import json

import fastapi
import re
from typing import List, Optional
import ldap3.utils.dn
from fastapi import Depends, Header

from models.users import User, DataAdmins, DataSessionAccess
from services import bnlpeople_service
from services import pass_service
from services import n2sn_service

from N2SNUserTools.ldap import ADObjects

from infrastucture import settings

router = fastapi.APIRouter()


@router.get('/users/me')
async def get_current_user(x_remote_user: Optional[str] = Header(None)):
    user_info = {"upn": x_remote_user}

    return user_info


# @router.get('/users')
# def get_users(person: User):
#     pass


@router.get('/users/{username}', response_model=User)
async def get_user_by_username(person: User = Depends()):
    ad_person = await n2sn_service.get_user_by_username_async(person.username)

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


@router.get('/users/{username}/proposals')
async def get_proposals_by_username(person: User = Depends()):
    bnl_person = await bnlpeople_service.get_person_by_username_async(person.username)
    proposals = await pass_service.get_proposals_by_person(bnl_person[0]['EmployeeNumber'])
    return proposals

@router.get('/data_session/{username}', response_model=DataSessionAccess)
async def get_datasessions_by_username(person: User = Depends()):
    proposals = await get_proposals_by_username(person)
    proposal_ids = [ sublist['Proposal_ID'] for sublist in proposals ]
    proposal_ids = [f'pass-{str(i)}' for i in proposal_ids]
    dataaccess = DataSessionAccess(all_access=False, data_sessions=proposal_ids)
    return dataaccess

# @router.get('/dataaccess/{username}/{datasession}/{beamline}', response_model=DataSessionAccess)
#     async get_datasession_list(username: str, data_session: str, beamline: )

@router.get('/user/{username}/data-admin-rights', response_model=DataAdmins)
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
    if 'n2sn-dataadmin' in dagrouplist:
        response['nsls2_dataadmin'] = True
        response['lbms_dataadmin'] = True

    if 'nsls2-dataadmin' in dagrouplist:
        response['nsls2_dataadmin'] = True

    if 'lbms-dataadmin' in dagrouplist:
        response['lbms_dataadmin'] = True

    beamline_dataadmin = []

    # TODO: this is not the place to do it... but for now
    f = open("beamlines.yml")
    beamlines = json.load(f)
    for beamline in beamlines:
        tla = str(beamline['name']).lower()
        datagroup_name = f"n2sn-secgrp-dataadmin-{tla}"
        if n2sn_service.is_user_in_group(username, datagroup_name):
            beamline_dataadmin.append(tla)

    response['dataadmin'] = beamline_dataadmin

    return response


@router.get('/user/{username}/data-admin-rights-hack', response_model=DataAdmins)
async def get_user_dataadmin_rights(username: str):
    # userinfo = await n2sn_service.get_groups_by_username_async(username)

    userinfo = [{'sAMAccountName': 'abarbour',
                 'distinguishedName': 'CN=Barbour\\, Andi,OU=CAM - Users,OU=CAM,DC=bnl,DC=gov',
                 'member': None,
                 'memberOf': ['CN=n2sn-instusers-guacctrl-chx,OU=N2SN,OU=CCM,DC=bnl,DC=gov',
                              'CN=n2sn-instusers-chx,OU=N2SN,OU=CCM,DC=bnl,DC=gov',
                              'CN=n2sn-inststaff-csx,OU=N2SN,OU=CCM,DC=bnl,DC=gov',
                              'CN=All_PS_Employees,OU=Automatic,OU=CAM,DC=bnl,DC=gov',
                              'CN=SIX Team,OU=CAM - Deny Cloud Sync,OU=CAM,DC=bnl,DC=gov',
                              'CN=DuoUsers,OU=CAM - Security Groups,OU=CAM,DC=bnl,DC=gov',
                              'CN=PS_AutoDesk_Inventor_Installs,OU=PS - Groups,OU=PS,OU=Research Enclave,DC=bnl,DC=gov',
                              'CN=BSA_Users,OU=CAM - WCM Groups,OU=CAM,DC=bnl,DC=gov',
                              'CN=GPO_Apps_OfficeDocumentSigning_PS,OU=CAM - Security Groups,OU=CAM,DC=bnl,DC=gov',
                              'CN=AO_ADS_Users,OU=CAM - Security Groups,OU=CAM,DC=bnl,DC=gov',
                              'CN=CSX Beamline Team,OU=CAM - Deny Cloud Sync,OU=CAM,DC=bnl,DC=gov',
                              'CN=NSLS-II BL Operations,OU=CAM - Deny Cloud Sync,OU=CAM,DC=bnl,DC=gov',
                              'CN=NSLS2-CRNotify,OU=CAM - Distribution Groups,OU=CAM,DC=bnl,DC=gov',
                              'CN=Bldg. 741 Members,OU=CAM - Deny Cloud Sync,OU=CAM,DC=bnl,DC=gov',
                              'CN=Photon Science Division All,OU=CAM - Deny Cloud Sync,OU=CAM,DC=bnl,DC=gov',
                              'CN=NSLS-II Personnel,OU=CAM - Deny Cloud Sync,OU=CAM,DC=bnl,DC=gov',
                              'CN=NSLS-II Scientific Staff,OU=CAM - Deny Cloud Sync,OU=CAM,DC=bnl,DC=gov',
                              'CN=GCMS_Owners,OU=CAM - Security Groups,OU=CAM,DC=bnl,DC=gov',
                              'CN=PS_NSLS2_MechEng,OU=PS - Groups,OU=PS,OU=Research Enclave,DC=bnl,DC=gov',
                              'CN=GBNL_Employees,OU=CAM - Security Groups,OU=CAM,DC=bnl,DC=gov']}]

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

    beamline_dataadmin = []

    # TODO: this is not the place to do it... but for now
    # f = open("beamlines.yml")
    # beamlines = json.load(f)

    beamlines = [
        {
            "name": "SIX",
            "long_name": "Soft Inelastic X-ray Scattering",
            "pass_name": "Beamline 2-ID",
            "port_name": "2-ID",
            "location_name": "xf02id1"
        },
        {
            "name": "HXN",
            "long_name": "Hard X-ray Nanoprobe",
            "pass_name": "Beamline 3-ID",
            "port_name": "3-ID",
            "location_name": "xf03id1"
        },
        {
            "name": "XFM",
            "long_name": "X-ray Fluorescence Microprobe",
            "pass_name": "Beamline 4-BM",
            "port_name": "4-BM",
            "location_name": "xf04bm"
        },
        {
            "name": "ISR",
            "long_name": "Integrated In situ and Resonant Hard X-ray Studies",
            "pass_name": "Beamline 4-ID",
            "port_name": "4-ID",
            "location_name": "xf04id1"
        },
        {
            "name": "SRX",
            "pass_name": "Beamline 5-ID",
            "long_name": "Submicron Resolution X-ray Spectroscopy",
            "port_name": "5-ID",
            "local_username": "xf05id",
            "location_name": "xf05id2",
            "facility": "NSLS-II"
        },
        {
            "name": "BMM",
            "long_name": "Beamline for Materials Measurement",
            "pass_name": "Beamline 6-BM",
            "port_name": "6-BM",
            "location_name": "xf06bm"
        },
        {
            "name": "QAS",
            "long_name": "Quick X-ray Absorption and Scattering",
            "pass_name": "Beamline 7-BM",
            "port_name": "7-BM",
            "location_name": "xf07bm"
        },
        {
            "name": "SST1",
            "long_name": "Spectroscopy Soft and Tender",
            "pass_name": "Beamline 17-ID-1",
            "port_name": "17-ID-1",
            "location_name": "xf17id1"
        },
        {
            "name": "SST2",
            "long_name": "Spectroscopy Soft and Tender",
            "pass_name": "Beamline 17-ID-2",
            "port_name": "17-ID-2",
            "location_name": "xf17id2"
        },
        {
            "name": "TES",
            "long_name": "Tender Energy X-ray Absorption Spectroscopy",
            "pass_name": "Beamline 8-BM",
            "port_name": "8-BM",
            "location_name": "xf08bm"
        },
        {
            "name": "ISS",
            "long_name": "Inner-Shell Spectroscopy",
            "pass_name": "Beamline 8-ID",
            "port_name": "8-ID",
            "location_name": "xf08id1"
        },
        {
            "name": "IXS",
            "long_name": "Inelastic X-ray Scattering",
            "pass_name": "Beamline 10-ID",
            "port_name": "10-ID",
            "location_name": "xf10id1"
        },
        {
            "name": "CMS",
            "long_name": "Complex Materials Scattering",
            "pass_name": "Beamline 11-BM",
            "port_name": "11-BM",
            "location_name": "xf11bm"
        },
        {
            "name": "CHX",
            "long_name": "Coherent Hard X-ray Scattering",
            "pass_name": "Beamline 11-ID",
            "port_name": "11-ID",
            "location_name": "xf11id1"
        },
        {
            "name": "SMI",
            "long_name": "Soft Matter Interfaces",
            "pass_name": "",
            "port_name": "12-ID",
            "location_name": ["xf12id1", "xf12id2"],
            "endstations": ["SWAXS", "OPLS"]
        },
        {
            "name": "LiX",
            "long_name": "Life Science X-ray Scattering",
            "pass_name": "",
            "port_name": "16-ID",
            "location_name": "xf16id1"
        },
        {
            "name": "XFP",
            "long_name": "X-ray Footprinting of Biological Materials",
            "pass_name": "",
            "port_name": "17-BM",
            "location_name": "xf17bm"
        },
        {
            "name": "AMX",
            "long_name": "Automated Macromolecular Crystallography",
            "pass_name": "",
            "port_name": "17-ID-1",
            "location_name": "xf17id1"
        },
        {
            "name": "FMX",
            "long_name": "Frontier Microfocusing Macromolecular Crystallography",
            "pass_name": "",
            "port_name": "17-ID-2",
            "location_name": "xf17id2"
        },
        {
            "name": "FXI",
            "long_name": "Full Field X-ray Imaging",
            "pass_name": "",
            "port_name": "18-ID",
            "location_name": "xf18id1"
        },
        {
            "name": "CSX",
            "pass_name": "Beamline 23-ID-1",
            "long_name": "Coherent Soft X-ray Scattering beamline",
            "port_name": "23-ID-1",
            "location_name": "xf23id1"
        },
        {
            "name": "IOS",
            "pass_name": "Beamline 23-ID-2",
            "long_name": "In situ and Operando Soft X-ray Spectroscopy",
            "port_name": "23-ID-2",
            "location_name": "xf23id2"
        },
        {
            "name": "HEX",
            "pass_name": "Beamline 27-ID",
            "long_name": "High Energy Engineering X-ray Scattering",
            "port_name": "27-ID",
            "location_name": "xf27id1"
        },
        {
            "name": "PDF",
            "pass_name": "Beamline 28-ID-1",
            "long_name": "Pair Distribution Function",
            "port_name": "28-ID-1",
            "location_name": "xf28id1"
        },
        {
            "name": "XPD",
            "pass_name": "Beamline 28-ID-2",
            "long_name": "X-ray Powder Diffraction",
            "port_name": "28-ID-2",
            "location_name": "xf28id2",
            "endstations": ["maxpd", "tomo"]
        }
    ]

    for beamline in beamlines:
        tla = str(beamline['name']).lower()
        datagroup_name = f"n2sn-inststaff-{tla}"
        if datagroup_name in grouplist:
            beamline_dataadmin.append(tla)

    response['dataadmin'] = beamline_dataadmin

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
# beamline + user -> list of data-sessions
# beamline + user + datasession -> return yes/no
# user -> data_sessions
# beamline -> datasession
# #


# -> give a list --> give a list back of the ones user can see
# basically delete the ones you are not allowed to access from the list (option)
# give list in body...
#
# all_access: true
