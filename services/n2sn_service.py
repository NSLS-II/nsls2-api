from typing import Optional

from infrastucture import settings
from N2SNUserTools.ldap import ADObjects

api_key: Optional[str] = None


async def get_groups_by_username_sync(username: str):
    ad = ADObjects(settings.ACTIVE_DIRECTORY_SERVER, user_search=settings.N2SN_USER_SEARCH,
                   group_search=settings.N2SN_GROUP_SEARCH, authenticate=False,
                   ca_certs_file=settings.BNLROOT_CA_CERTS_FILE)
    # Dunno why I need to do this - TODO: Fix later :)
    ad.__enter__()
    return ad.get_group_by_samaccountname(username)

