from typing import Optional

import httpx
from httpx import Response

from infrastucture import settings
from .helpers import _call_async_webservice

api_key: Optional[str] = None

base_url = settings.PASS_API_URL

async def get_proposal(proposal_id: int):
    url = f'{base_url}/Proposal/GetProposal/{settings.PASS_API_KEY}/NSLS-II/{proposal_id}'
    print(url)
    proposal = await _call_async_webservice(url)
    return proposal

async def get_saf_from_proposal(proposal_id: int):
    url = f'{base_url}/SAF/GetSAFsByProposal/{settings.PASS_API_KEY}/NSLS-II/{proposal_id}'
    print(url)
    saf = await _call_async_webservice(url)
    return saf

async def get_commissioning_proposals_by_year(year: int):
    url = f"{base_url}Proposal/GetProposalsByType/{settings.PASS_API_KEY}/NSLS-II/{year}/300005/NULL"
    proposals = await _call_async_webservice(url)
    return proposals

async def get_pass_resources_async():
    url = f'{base_url}/Resource/GetResources/{settings.PASS_API_KEY}/NSLS-II'
    resources = await _call_async_webservice(url)
    return resources

async def get_cycles_async():
    url = f'{base_url}/Proposal/GetCycles/{settings.PASS_API_KEY}/NSLS-II'
    print(url)
    cycles = await _call_async_webservice(url)
    return cycles

async def get_proposals_allocated_async():
    url = f'{base_url}/Proposal/GetProposalsAllocated/{settings.PASS_API_KEY}/NSLS-II'
    allocated_proposals = await _call_async_webservice(url)
    return allocated_proposals

async def get_proposals_by_person(bnl_id : str):
    url = f'{base_url}/Proposal/GetProposalsByPerson/{settings.PASS_API_KEY}/NSLS-II/null/null/{bnl_id}/null'
    print(url)
    proposals = await _call_async_webservice(url)
    return proposals
