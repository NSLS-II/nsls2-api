from typing import Optional, List

from pydantic import BaseModel

class User(BaseModel):
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    life_number: Optional[str] = None
    orcid: Optional[str] = None
    globus_username: Optional[str] = None
    pass_unique_id: Optional[str] = None

class DataAdmins(BaseModel):
    nsls2_dataadmin: bool = False
    lbms_dataadmin: bool = False
    dataadmin: Optional[list] = None
