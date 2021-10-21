from typing import Optional, List

from pydantic.main import BaseModel
from .facility import FacilityName


class ProposalIn(BaseModel):
    proposal_id: int

    class Config:
        schema_extra = {
            "example": {
                "proposal_id": 304947,
            }
        }

class ProposalUpdate(BaseModel):
    proposal_id: int
    facility: FacilityName = FacilityName.nsls2