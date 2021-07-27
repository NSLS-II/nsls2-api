import httpx
from httpx import Response

from models.validation_error import ValidationError


async def _call_async_webservice(url: str):
    async with httpx.AsyncClient() as client:
        resp: Response = await client.get(url)
        if resp.status_code != 200:
            raise ValidationError(resp.text, status_code=resp.status_code)
    results = resp.json()
    return results

