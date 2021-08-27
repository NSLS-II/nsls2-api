from typing import List

import fastapi
import httpx
from fastapi import Depends, Header

from models.proposal import ProposalIn

from services import pass_service

router = fastapi.APIRouter()


@router.get('/proposals')
def get_all_proposals():
    pass


@router.get('/proposal/{proposal_id}')
async def get_proposal(proposal_id: ProposalIn = Depends()):
    proposal = await pass_service.get_proposal(proposal_id.proposal_id)
    return proposal

@router.get('/saf/{proposal_id}')
async def get_proposal(proposal_id: ProposalIn = Depends()):
    saf = await pass_service.get_saf_from_proposal(proposal_id.proposal_id)
    return saf

#URL = "http://n2snadmin.nsls2.bnl.gov:5000"
#client_to_windows = httpx.AsyncClient(base_url=URL, headers={"X-API-KEY": n2sn_service.api_key})


# X-API-KEY
# "gu-999999-9"

# @router.post("/proposal/{proposal_id}")
# async def post_proposal(proposal_id: ProposalIn):
#     await client_to_windows.post("admin/group", json={"name": proposal_id.proposal_id})
