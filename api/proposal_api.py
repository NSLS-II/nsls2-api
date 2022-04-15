from typing import List

from bson.json_util import dumps

import fastapi
import httpx
from fastapi import Depends, Header
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyHeader
from pymongo import MongoClient
import motor.motor_asyncio 


from models.proposal import Proposal, ProposalIn, ProposalUpdate
from api.facility_api import facility_data

from services import pass_service
from infrastucture import settings


client = MongoClient(settings.NSLS2CORE_MONGODB_URI)
#client = motor.motor_asyncio.AsyncIOMotorClient(settings.NSLS2CORE_MONGODB_URI)

router = fastapi.APIRouter()

#@router.get('/proposals')
def get_all_proposals():
    pass

# This uses the pass API to get the proposal info
#@router.get('/pass/proposal/{proposal_id}')
async def get_proposal(proposal_id: ProposalIn = Depends()):
    proposal = await pass_service.get_proposal(proposal_id.proposal_id)
    return proposal

# @router.get('/proposal/{proposal_id}/user')
# async def get_proposal_users(proposal_id: ProposalIn = Depends()):
#     database = client["nsls2core"]
#     collection = database["proposals"]

#     query = {}
#     query["proposal_id"] = str(proposal_id.proposal_id)
#     projection = {}
#     projection["users"] = 1.0
#     result = collection.find_one(query, projection=projection)

#     return JSONResponse(content=result)



#@router.get('/proposal/{proposal_id}')
async def get_proposal(proposal_id: ProposalIn = Depends()):
    database = client["nsls2core"]
    collection = database["proposals"]

    query = {}
    query["proposal_id"] = str(proposal_id.proposal_id)

    projection = {}
    projection["_id"] = 0.0
    projection["last_updated"] = 0.0

    result = collection.find_one(query, projection=projection)

    return JSONResponse(content=result)





@router.put('/proposal/{proposal_id}')
async def update_proposal(proposal: ProposalUpdate = Depends()):
    facility_info = facility_data[proposal.facility.name]
    msg = {
        'message': f'I am new going to update my local information for Proposal ID {proposal.proposal_id} for the '
                   f'{facility_info["pass_facility_id"]} facility.'}
    return msg

#@router.get('/saf/{proposal_id}')
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
