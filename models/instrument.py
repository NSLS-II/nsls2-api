from typing import Optional, List

from pydantic.main import BaseModel


class Instrument(BaseModel):
    name: str
    full_name: str
    port_name: str
    description: str
    network_name: Optional[str]
    endstations: List[str] = []

