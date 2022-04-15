from enum import Enum
from typing import Optional, List, Dict

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
    port: Optional[str] = None
    locations: Optional[List[str]] = None



class InstrumentWithInternalDetails(Instrument):
    nsls2_redhat_satellite_location_name: Optional[str] = None
    service_accounts: Optional[Dict[str, str]] = None
    pass_id: Optional[str] = None
    pass_name: Optional[str] = None
    
