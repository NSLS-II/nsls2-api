import json

from pymongo import MongoClient
from starlette.config import Config
from N2SNUserTools.ldap import ADObjects

import script_settings

config = Config(".env-scripts")
NSLS2CORE_MONGODB_URI = config('NSLS2CORE_MONGODB_URI', cast=str)

if __name__ == '__main__':
    client = MongoClient(NSLS2CORE_MONGODB_URI)
    db = client.nsls2core
    collection = db["beamlines"]

    f = open('beamlines.yml')
    beamlines = json.load(f)
    f.close()

    for beamline in beamlines:
        # Default operator account name to location name
        if 'operator' in beamline:
            operator = beamline['local_username']
        else:
            operator = beamline['location_name']

        with ADObjects(script_settings.ACTIVE_DIRECTORY_SERVER, user_search=script_settings.N2SN_USER_SEARCH,
                   group_search=script_settings.N2SN_GROUP_SEARCH, authenticate=False,
                   ca_certs_file=script_settings.BNLROOT_CA_CERTS_FILE) as ad:

            users = ad.get_user_by_samaccountname(operator)
            if len(users) == 0:
                raise RuntimeError(f"Unable to find user {operator}, please check.")

            if len(users) != 1:
                raise RuntimeError(
                    f"Login (Username) {operator} is not unique. Please check."
                )

            # Get operator account AD object
            user = users[0]

            proposal_groups = []
            for group in user["memberOf"]:
                group_name = group.split(",", 1)[0].split("=", 1)[1]
                if group_name.startswith("pass"):
                    proposal_groups.append(group_name)


        document = {}
        document['operator'] = operator
        document['active_proposals'] = proposal_groups

        print(f"Syncing active proposals for operator account {operator}.")

        # filter = "{'group_name': {'$eq': 'n2sn-right-dataadmin-csx'}"
        # insert_result = groups.update_one(filter, document, upsert=True)

        insert_result = collection.insert_one(document)

        print(insert_result)
