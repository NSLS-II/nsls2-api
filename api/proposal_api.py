from typing import List

import fastapi
import httpx

from models.proposal import Proposal

from services import n2sn_service

router = fastapi.APIRouter()


@router.get('/proposals')
def get_all_proposals():
    pass


@router.get('/proposal/{proposal_id}')
def get_proposal():
    pass


#URL = "http://n2snadmin.nsls2.bnl.gov:5000"
#client_to_windows = httpx.AsyncClient(base_url=URL, headers={"X-API-KEY": n2sn_service.api_key})


# X-API-KEY
# "gu-999999-9"

@router.post("/proposal/{proposal_id}")
async def post_proposal(proposal: Proposal):
    await client_to_windows.post("admin/group", json={"name": proposal.proposal_id})
