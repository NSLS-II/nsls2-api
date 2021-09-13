from enum import Enum
from typing import Optional, List

from pydantic.main import BaseModel


class BeamlineName(Enum):
    six = "six"
    amx = "amx"
    fmx = "fmx"
    csx = "csx"
    ios = "ios"
    pdf = "pdf"
    xpd = "xpd"


class Instrument(BaseModel):
    name: str
    long_name: str
    alternative_name: str = None
    pass_id: str
    locations: Optional[List[str]] = None
