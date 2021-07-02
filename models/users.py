from typing import Optional, List

from pydantic import BaseModel

class Username(BaseModel):
    username: str

class User(Username):
    first_name: str
    last_name: str
    email: str
    life_number: str
    orcid: Optional[str]
    globus_username: Optional[str]
    pass_unique_id: Optional[str]
