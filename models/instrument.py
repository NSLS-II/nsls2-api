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


class InstrumentBase(BaseModel):
    name: str
    full_name: str
    port_name: str
    description: str
    network_name: Optional[str] = None


class Instrument(InstrumentBase):
    endstations: List[str] = []


class Endstation(InstrumentBase):
    pass
