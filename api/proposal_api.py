import pprint
from typing import List, Dict

import fastapi
import httpx
from pathlib import Path
from fastapi import Depends, Header
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyHeader
from pymongo import MongoClient

from infrastucture import settings
from infrastucture.database import fetch_beamline_root_directory_name
from models.proposal import ProposalIn, ProposalUpdate
from models.facility import Cycle
from api.facility_api import facility_data

client = MongoClient(settings.NSLS2CORE_MONGODB_URI)
# client = motor.motor_asyncio.AsyncIOMotorClient(settings.NSLS2CORE_MONGODB_URI)

router = fastapi.APIRouter()


# Handle special cases where the workflow user is *not* workflow-{beamline_tla}
WORKFLOW_USERS = {
    "sst1": "workflow-sst",
    "sst2": "workflow-sst",
}
SYNCHWEB_BEAMLINES = {"amx", "fmx", "lix"}

# Handle special cases where the softioc user is *not* softioc-{beamline_tla}
IOC_USERS = {
    "sst2": "softioc-sst",
}

LSDC_BEAMLINES = {"amx", "fmx", "nyx"}

def get_workflow_user(beamline):
    beamline_lower = beamline.lower()
    return WORKFLOW_USERS.get(beamline_lower, f"workflow-{beamline_lower}")

def get_ioc_user(beamline):
    beamline_lower = beamline.lower()
    return IOC_USERS.get(beamline_lower, f"softioc-{beamline_lower}")

@router.get('/proposals/commissioning')
async def get_commissioning_proposals(return_json: bool = True):
    database = client["nsls2core"]
    collection = database["proposals"]

    pipeline = [
        {
            "$match": {
                "pass_type_id": "300005"
            }
        },
        {
            "$project": {
                "proposal_id": 1.0
            }
        },
        {
            "$group": {
                "_id": None,
                "proposal_id": {
                    "$addToSet": "$proposal_id"
                }
            }
        }
    ]

    cursor = collection.aggregate(
        pipeline,
        allowDiskUse=False
    )

    result = {"commissioning_proposals": []}
    for doc in cursor:
        result['commissioning_proposals'].extend(doc['proposal_id'])

    if return_json:
        return JSONResponse(content=result)

    return result

@router.get('/proposals/{cycle}')
async def get_proposals_for_cycle(cycle: str):
    database = client["nsls2core"]
    collection = database["cycles"]
    query = {"name": str(cycle)}
    projection = {"proposals": 1.0, "_id": 0.0}
    cursor = collection.find(query, projection=projection)
    result = []
    for doc in cursor:
        result.append(doc)
    return result

@router.get('/proposal/{proposal_id}/usernames')
async def get_proposal_usernames(proposal_id: ProposalIn = Depends(), return_json: bool = True):
    database = client["nsls2core"]
    collection = database["proposals"]

    pipeline = [
        {
            "$match": {
                "proposal_id": str(proposal_id.proposal_id)
            }
        },
        {
            "$project": {
                "users": 1.0
            }
        },
        {
            "$group": {
                "_id": None,
                "usernames": {
                    "$addToSet": "$users.username"
                }
            }
        },
        {
            "$addFields": {
                "usernames": {
                    "$filter": {
                        "input": {
                            "$first": u"$usernames"
                        },
                        "as": "un",
                        "cond": {
                            "$ne": [
                                "$$un",
                                None
                            ]
                        }
                    }
                }
            }
        }
    ]

    cursor = collection.aggregate(
        pipeline,
        allowDiskUse=False
    )

    result = {"usernames": []}
    for doc in cursor:
        result["usernames"].extend(doc["usernames"])

    if return_json:
        return JSONResponse(content=result)

    return result


@router.get('/proposal/{proposal_id}/users')
async def get_proposal_users(proposal_id: ProposalIn = Depends()):
    database = client["nsls2core"]
    collection = database["proposals"]
    query = {"proposal_id": str(proposal_id.proposal_id)}
    projection = {"users": 1.0, "proposal_id": True, "_id": 0.0}
    proposal_doc = collection.find_one(query, projection=projection)
    if proposal_doc is None:
        return {'error_message': f"No proposal {str(proposal_id.proposal_id)} found."}
    return JSONResponse(content=proposal_doc)


@router.get('/proposal/{proposal_id}/directories')
async def get_proposal_directories(proposal_id: ProposalIn = Depends(), testing: bool = False):
    database = client["nsls2core"]
    collection = database["proposals"]

    # First get the proposal details from the database
    query = {"proposal_id": str(proposal_id.proposal_id)}
    projection = {"_id": 0.0, "last_updated": 0.0}
    proposal_doc = collection.find_one(query, projection=projection)

    if proposal_doc is None:
        return {'error_message': f"No proposal {str(proposal_id.proposal_id)} found."}

    # Ensure we set a sensible default incase there are no cycles listed for the proposal.
    proposal_doc.setdefault('cycles', [])
    
    data_session = proposal_doc['data_session']
    beamlines = proposal_doc['instruments']
    cycles = proposal_doc['cycles']
    proposal_type = proposal_doc['type']

    # if any of the above are null or zero length, then we don't have
    # enough information to create any directories
    insufficient_information = False
    error_msg = []

    if data_session is None:
        insufficient_information = True
        error_msg.append(f"Proposal {str(proposal_id.proposal_id)} does not contain a data_session.")

    if (len(cycles) == 0) and (proposal_type !=  "Beamline Commissioning (beamline staff only)"):
        insufficient_information = True
        error_msg.append(f"Proposal {str(proposal_id.proposal_id)} does not contain any cycle information.")

    if len(beamlines) == 0:
        insufficient_information = True
        error_msg.append(f"Proposal {str(proposal_id.proposal_id)} does not contain any beamlines.")

    directories = []

    if testing:
        pprint.pprint(f"Testing is TRUE {testing}")
        root = Path('/nsls2/data/.testing')
    else:
        pprint.pprint(f"Testing is FALSE {testing}")
        root = Path('/nsls2/data')

    for beamline in beamlines:

        # First lets check if this is a commissioning proposal
        if proposal_type == "Beamline Commissioning (beamline staff only)":
            pprint.pprint(f"Proposal {str(proposal_id.proposal_id)} is a commissioning proposal.")
            # Now just set the cycle directory to be the commissioning one
            cycles = ['commissioning']

        for cycle in cycles:
            beamline_tla = str(beamline).lower()
            beamline_dir = await fetch_beamline_root_directory_name(beamline_tla.upper())
            users_acl: list[dict[str, str]] = []
            groups_acl: list[dict[str, str]] = []

            users_acl.append({'nsls2data': 'rw'})
            users_acl.append({f"{get_workflow_user(beamline)}": "rw"})
            users_acl.append({f"{get_ioc_user(beamline)}": "rw"})
            groups_acl.append({str(data_session): "rw"})

            # Add LSDC beamline users for the appropriate beamlines
            if beamline_tla in LSDC_BEAMLINES:
                users_acl.append({f"lsdc-{beamline_tla}": "rw"})

            groups_acl.append({'n2sn-right-dataadmin': "rw"})
            groups_acl.append({f"n2sn-right-dataadmin-{beamline_tla}": "rw"})

            if beamline_tla in SYNCHWEB_BEAMLINES:
                users_acl.append({'synchweb': 'r'})

            directory = {'path': root / beamline_dir / 'proposals' / str(cycle) / str(data_session),
                         'owner': 'nsls2data', 'group': str(data_session), 'group_writable': True,
                         'users': users_acl, 'groups': groups_acl}
            directories.append(directory)

    if insufficient_information:
        response = {'error_message': error_msg}
        return response

    return directories


@router.get('/proposal/{proposal_id}/group-membership')
async def get_proposal_groups(proposal_id: ProposalIn = Depends()):
    database = client["nsls2core"]
    collection = database["proposals"]

    # First get the proposal details from the database
    query = {"proposal_id": str(proposal_id.proposal_id)}
    projection = {"_id": 0.0, "last_updated": 0.0}
    proposal_doc = collection.find_one(query, projection=projection)

    if proposal_doc is None:
        return {'error_message': f"No proposal {str(proposal_id.proposal_id)} found."}

    data_session = proposal_doc['data_session']

    if data_session is None:
        return {'error_message': f"No data session found for proposal {str(proposal_id.proposal_id)}."}

    usernames = await get_proposal_usernames(proposal_id, return_json=False)

    response = {}

    response['groupname'] = str(data_session)
    response['usernames'] = usernames['usernames']

    return response


@router.get('/proposal/{proposal_id}')
async def get_proposal(proposal_id: ProposalIn = Depends()):
    database = client["nsls2core"]
    collection = database["proposals"]
    query = {"proposal_id": str(proposal_id.proposal_id)}
    projection = {"_id": 0.0, "last_updated": 0.0}
    proposal_doc = collection.find_one(query, projection=projection)
    if proposal_doc is None:
        return {'error_message': f"No proposal {str(proposal_id.proposal_id)} found."}
    return JSONResponse(content=proposal_doc)


@router.put('/proposal/{proposal_id}')
async def update_proposal(proposal: ProposalUpdate = Depends()):
    facility_info = facility_data[proposal.facility.name]
    msg = {
        'message': f'I am new going to update my local information for Proposal ID {proposal.proposal_id} for the '
                   f'{facility_info["pass_facility_id"]} facility.'}
    return msg


# Commented out because it is very slow at the moment
# @router.get('/saf/{proposal_id}')
# async def get_proposal(proposal_id: ProposalIn = Depends()):
#     saf = await pass_service.get_saf_from_proposal(proposal_id.proposal_id)
#     return saf

# URL = "http://n2snadmin.nsls2.bnl.gov:5000"
# client_to_windows = httpx.AsyncClient(base_url=URL, headers={"X-API-KEY": n2sn_service.api_key})


# X-API-KEY
# "gu-999999-9"

# @router.post("/proposal/{proposal_id}")
# async def post_proposal(proposal_id: ProposalIn):
#     await client_to_windows.post("admin/group", json={"name": proposal_id.proposal_id})
