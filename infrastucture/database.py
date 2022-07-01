import pprint

import pymongo
from bson import Regex

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
    query = {"name": Regex(f"{beamline_name}", "i")}
    projection = {"_id": 0.0, "last_updated": 0.0}
    beamline_doc = collection.find_one(query, projection=projection)

    if beamline_doc is None:
        raise RuntimeError(f"No beamline {beamline_name} exists.")

    # Now we have a document for the beamline, return the custom root directory
    # if it exists, or just the default (beamline name) if it doesn't.
    return beamline_doc.get('custom_root_directory', str(beamline_name.lower()))
