import json

from pymongo import MongoClient
from starlette.config import Config

from N2SNUserTools.ldap import ADObjects

import script_settings

config = Config(".env-scripts")
N2SN_CACHE_DB_CONNECTION = config('N2SN_CACHE_DB_CONNECTION', cast=str)
NSLS2CORE_MONGODB_URI = config('NSLS2CORE_MONGODB_URI', cast=str)


if __name__ == '__main__':
    client = MongoClient(N2SN_CACHE_DB_CONNECTION)
    client = MongoClient(NSLS2CORE_MONGODB_URI)
    db = client.nsls2core

    f = open('beamlines.yml')
    beamlines = json.load(f)
    f.close()

    for beamline in beamlines:
        tla = str(beamline['name']).lower()
        datagroup_name = f"n2sn-secgrp-dataadmin-{tla}"
        print(f"Getting data admins for {tla}")
        with ADObjects(script_settings.ACTIVE_DIRECTORY_SERVER, user_search=script_settings.N2SN_USER_SEARCH,
                   group_search=script_settings.N2SN_GROUP_SEARCH, authenticate=False,
                   ca_certs_file=script_settings.BNLROOT_CA_CERTS_FILE) as ad:
            users = ad.get_group_members(datagroup_name)
        document = {}
        document['group_name'] = datagroup_name
        document['members'] = users

        print(f"Updating database cache for {datagroup_name} group members")

        # filter = "{'group_name': {'$eq': 'n2sn-secgrp-dataadmin-csx'}"
        # insert_result = groups.update_one(filter, document, upsert=True)

        insert_result = groups.insert_one(document)

        print(insert_result)



