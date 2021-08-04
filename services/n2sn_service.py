from typing import Optional

from infrastucture import settings
from N2SNUserTools.ldap import ADObjects

api_key: Optional[str] = None


async def get_groups_by_username_async(username: str):
    with ADObjects(settings.ACTIVE_DIRECTORY_SERVER, user_search=settings.N2SN_USER_SEARCH,
                   group_search=settings.N2SN_GROUP_SEARCH, authenticate=False,
                   ca_certs_file=settings.BNLROOT_CA_CERTS_FILE) as ad:
        userdetails = ad.get_group_by_samaccountname(username)
    return userdetails

async def get_users_in_group_async(group: str):
    with ADObjects(settings.ACTIVE_DIRECTORY_SERVER, user_search=settings.N2SN_USER_SEARCH,
                   group_search=settings.N2SN_GROUP_SEARCH, authenticate=False,
                   ca_certs_file=settings.BNLROOT_CA_CERTS_FILE) as ad:
        users = ad.get_group_members(group)
    return users

async def is_user_in_group_async(username: str, group: str):
    _user_found = False
    users = await get_users_in_group_async(group)
    _user_found = any([user for user in users if user['sAMAccountName'] == username])
    return _user_found

