from typing import Optional, List

from pydantic.main import BaseModel


class Proposal(BaseModel):
    name: str
