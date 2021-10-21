from enum import Enum
from typing import Optional, List

from pydantic.main import BaseModel

class FacilityName(Enum):
    nsls2="nsls2"
    lbms="lbms"

class Facility(BaseModel):
    name: str
    id: str
    fullname: str
    pass_facility_id: str

class Cycles(BaseModel):
    name: str
