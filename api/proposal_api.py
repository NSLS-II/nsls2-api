from typing import List

import fastapi

from models.proposal import Proposal

router = fastapi.APIRouter()

@router.get('/proposals')
def get_all_proposals():
    pass

@router.get('/proposal/{proposal_id}')
def get_proposal():
    pass


