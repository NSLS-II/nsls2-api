from typing import Optional, List

from pydantic.main import BaseModel


class ProposalIn(BaseModel):
    proposal_id: int

    class Config:
        schema_extra = {
            "example": {
                "proposal_id": 304947,
            }
        }
