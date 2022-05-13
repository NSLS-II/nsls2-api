import pprint

import pymongo

from infrastucture import settings

from models.instrument import Instrument

client = pymongo.MongoClient(settings.NSLS2CORE_MONGODB_URI)
db = client["nsls2core"]


async def fetch_all_beamlines():
    instruments = []
    cursor = db.beamlines.find({}, {'_id': 0})
    for doc in cursor:
        pprint.pprint(doc)
        instruments.append(Instrument(**doc))
    return instruments

async def fetch_beamline_root_directory_name(beamline_name : str):
    database = client["nsls2core"]
    collection = database["beamlines"]
    query = {"name": beamline_name.upper()}
    projection = {"_id": 0.0, "last_updated": 0.0}
    beamline_doc = collection.find_one(query, projection=projection)

    if beamline_doc is None:
        return {'error_message': f"No beamline {beamline_name.upper()} exists."}

    try:
        custom_rootdir = beamline_doc['custom_root_directory']
    except KeyError:
        # If the custom root directory field does not exist, just use the TLA
        return str(beamline_name.lower())

    if custom_rootdir:
        return str(custom_rootdir).lower()
    else:
        return str(beamline_name.lower())
