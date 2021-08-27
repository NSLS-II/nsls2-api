import asyncio
from typing import Optional

import pymongo
from motor import motor_asyncio
from pymongo import MongoClient

from infrastucture import settings
from N2SNUserTools.ldap import ADObjects

api_key: Optional[str] = None

# client = motor_asyncio.AsyncIOMotorClient(settings.N2SN_CACHE_DB_CONNECTION)
client = pymongo.MongoClient(settings.N2SN_CACHE_DB_CONNECTION)
db = client['n2sn-cache']
groups_collection = db.get_collection('groups')


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


def is_user_in_group(username: str, group: str):
    _user_found = False
    # users = await get_users_in_group_async(group)
    users = get_group_from_database_cache(group)
    _user_found: bool = any([user for user in users if user['sAMAccountName'] == username])
    return _user_found


def get_group_from_database_cache(group: str):
    doc = groups_collection.find_one({'group_name': {'$eq': f"{group}"}})
    users = doc['members']
    return users
