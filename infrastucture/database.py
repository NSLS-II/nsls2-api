import pprint

import pymongo

from infrastucture import settings

from models.instrument import Instrument

client = pymongo.MongoClient(settings.N2SN_CACHE_DB_CONNECTION)
db = client["nsls2-core"]


async def fetch_all_beamlines():
    instruments = []
    cursor = db.beamlines.find({}, {'_id': 0})
    for doc in cursor:
        pprint.pprint(doc)
        instruments.append(Instrument(**doc))
    return instruments
