import httpx
from httpx import Response, Timeout

from models.validation_error import ValidationError


async def _call_async_webservice(url: str):
    async with httpx.AsyncClient(timeout=httpx.Timeout(5.0, read=20.0)) as client:
        resp: Response = await client.get(url)
        if resp.status_code != 200:
            raise ValidationError(resp.text, status_code=resp.status_code)
    results = resp.json()
    return results

