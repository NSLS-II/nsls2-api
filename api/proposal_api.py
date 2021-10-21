from typing import List

import fastapi
import httpx
from fastapi import Depends, Header
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyHeader
from pymongo import MongoClient

from infrastucture import settings
from models.proposal import ProposalIn, ProposalUpdate
from api.facility_api import facility_data

from services import pass_service

client = MongoClient(settings.NSLS2CORE_MONGODB_URI)
# client = motor.motor_asyncio.AsyncIOMotorClient(settings.NSLS2CORE_MONGODB_URI)

router = fastapi.APIRouter()


# @router.get('/proposals')GIST.wauf-bain5gruf
# def get_all_proposals():
#     pass

@router.get('/proposal/{proposal_id}/usernames')
async def get_proposal_usernames(proposal_id: ProposalIn = Depends()):
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
    return JSONResponse(content=result)


@router.get('/proposal/{proposal_id}/users')
async def users(proposal_id: ProposalIn = Depends()):
    database = client["nsls2core"]
    collection = database["proposals"]
    query = {"proposal_id": str(proposal_id.proposal_id)}
    projection = {"users": 1.0, "proposal_id": True, "_id": 0.0}
    result = collection.find_one(query, projection=projection)
    print(result)
    return JSONResponse(content=result)


@router.get('/proposal/{proposal_id}')
async def get_proposal_from_pass(proposal_id: ProposalIn = Depends()):
    database = client["nsls2core"]
    collection = database["proposals"]
    query = {"proposal_id": str(proposal_id.proposal_id)}
    projection = {"_id": 0.0, "last_updated": 0.0}
    result = collection.find_one(query, projection=projection)
    return JSONResponse(content=result)

@router.get('/pass/proposal/{proposal_id}')
async def get_proposal_from_pass(proposal_id: ProposalIn = Depends()):
    proposal = await pass_service.get_proposal(proposal_id.proposal_id)
    return proposal


# @router.post('/proposal/{proposal_id}')


@router.put('/proposal/{proposal_id}')
async def update_proposal(proposal: ProposalUpdate = Depends()):
    facility_info = facility_data[proposal.facility.name]
    msg = {
        'message': f'I am new going to update my local information for Proposal ID {proposal.proposal_id} for the '
                   f'{facility_info["pass_facility_id"]} facility.'}
    return msg


@router.get('/saf/{proposal_id}')
async def get_proposal(proposal_id: ProposalIn = Depends()):
    saf = await pass_service.get_saf_from_proposal(proposal_id.proposal_id)
    return saf

# URL = "http://n2snadmin.nsls2.bnl.gov:5000"
# client_to_windows = httpx.AsyncClient(base_url=URL, headers={"X-API-KEY": n2sn_service.api_key})


# X-API-KEY
# "gu-999999-9"

# @router.post("/proposal/{proposal_id}")
# async def post_proposal(proposal_id: ProposalIn):
#     await client_to_windows.post("admin/group", json={"name": proposal_id.proposal_id})
