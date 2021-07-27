from typing import Optional

import httpx
from httpx import Response

from infrastucture import settings
from .helpers import _call_async_webservice

api_key: Optional[str] = None

base_url = settings.PASS_API_URL

async def get_proposal():
    return


async def get_pass_resources_async():
    url = f'{base_url}/Resource/GetResources/{settings.PASS_API_KEY}/NSLS-II'
    resources = await _call_async_webservice(url)
    return resources

async def get_cycles_async():
    url = f'{base_url}/Proposal/GetCycles/{settings.PASS_API_KEY}/NSLS-II'
    print(url)
    cycles = await _call_async_webservice(url)
    return cycles

