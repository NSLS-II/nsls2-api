from typing import List

import fastapi

from models.proposal import Proposal

from services import n2sn_service

router = fastapi.APIRouter()


@router.get('/proposals')
def get_all_proposals():
    pass


@router.get('/proposal/{proposal_id}')
def get_proposal():
    pass



# X-API-KEY
# "gu-999999-9"
