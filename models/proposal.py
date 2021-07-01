from typing import Optional, List

from pydantic.main import BaseModel


class Proposal(BaseModel):
    proposal_id: str
    users_admin: List[str]  # PI(s)
    users: List[str]
