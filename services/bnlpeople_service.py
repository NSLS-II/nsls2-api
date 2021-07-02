from typing import Optional

import httpx
from httpx import Response

from models.validation_error import ValidationError

base_url = 'https://api.bnl.gov/BNLPeople'


async def _call_bnlpeople_webservice(url: str):
    async with httpx.AsyncClient() as client:
        resp: Response = await client.get(url)
        if resp.status_code != 200:
            raise ValidationError(resp.text, status_code=resp.status_code)
    results = resp.json()
    return results


async def get_all_people_async():
    url = f'{base_url}/api/BNLPeople'
    people = await _call_bnlpeople_webservice(url)
    return people


async def get_person_by_username_async(username: str):
    url = f'{base_url}/api/BNLPeople?accountName={username}'
    person = await _call_bnlpeople_webservice(url)
    return person


async def get_person_by_lifenumber_async(lifenumber: str):
    url = f'{base_url}/api/BNLPeople?employeeNumber={lifenumber}'
    person = await _call_bnlpeople_webservice(url)
    return person


async def get_person_by_email_async(email: str):
    url = f'{base_url}/api/BNLPeople?email={email}'
    person = await _call_bnlpeople_webservice(url)
    return person


async def get_people_by_department_async(department_code: str):
    url = f'{base_url}/api/BNLPeople?departmentCode={department_code}'
    people = await _call_bnlpeople_webservice(url)
    return people


async def get_people_by_status_async(status: str):
    if status.title() not in ("Active", "Inactive", "Pending"):
        raise ValueError("Status must be either 'Active', 'Inactive', 'Pending'")
    url = f"{base_url}/api/BNLPeople?status={status}"
    people = await _call_bnlpeople_webservice(url)
    return people


async def get_people_by_calcstatus_async(calculated_status: str):
    if calculated_status.title() not in ("Active", "Inactive"):
        raise ValueError("Calculated Status must be either 'Active', 'Inactive'")
    url = f'{base_url}/api/BNLPeople?status={calculated_status}'
    people = await _call_bnlpeople_webservice(url)
    return people
