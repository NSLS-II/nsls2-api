from typing import Optional, List

from pydantic import BaseModel, EmailStr


class User(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    life_number: str
    orcid: Optional[str]
    globus_username: Optional[EmailStr]
    pass_unique_id: Optional[str]
