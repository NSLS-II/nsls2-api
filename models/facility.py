from typing import Optional, List

from pydantic.main import BaseModel


class Facility(BaseModel):
    name: str
    pass_facility_id: Optional[str]
