#!/usr/bin/env python

from sh import gunzip
from glob import glob

import re, os, json

OUTDIR="data-unzipped"

if not os.stat(OUTDIR):
    print "created dir ", OUTDIR
    os.makedirs(OUTDIR)

for dataFile in glob("data/*.gz"):
    outFile = os.path.join(OUTDIR, re.search('(\d+).gz$', dataFile).groups()[0])
    if not os.stat(outFile):
        gunzip('-c', dataFile, _out=outFile)
        print "unzipped", dataFile, "to", outFile

# then, go through the data files and create a new JSON file that maps
# mpId [of route] -> { latitude, longitude, grade, protection }

allRoutes = dict()
allAreas = dict()

for dataFile in glob("data-unzipped/*"):
    data = json.load(file(dataFile))
    allRoutes.update(dict([(route['mpId'], route) for route in data['routes']]))
    # parentId of a route gives its area. parent of an area is the parent area.
    areas = dict([(area['id'], area) for area in data['areas']])
    allAreas.update(areas)
    # stupid algorithm to fill in missing latitude/longitude with values for
    # parent areas
    for area in areas.values():
        if area['parentId']:
            parent = allAreas[area['parentId']]
            while area['latitude'] == 0:
                area['latitude'] = parent['latitude']
                area['longitude'] = parent['longitude']
                # grandparent it up
                if parent['parentId'] == 0:
                    # no latitude / longitude available for this area
                    break
                parent = allAreas[parent['parentId']]
    allAreas.update(areas)

json.dump(allRoutes, file('routes.json', 'w'),
        sort_keys=True, indent=4, separators=(',', ': '))
print "routes dumped to routes.json"
json.dump(allAreas, file('areas.json', 'w'),
        sort_keys=True, indent=4, separators=(',', ': '))
print "areas dumped to areas.json"
