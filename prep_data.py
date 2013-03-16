#!/usr/bin/env python

from sh import gunzip
from glob import glob

import re, os

OUTDIR="data-unzipped"

if not os.stat(OUTDIR):
    print "created dir ", OUTDIR
    os.makedirs(OUTDIR)

for dataFile in glob("data/*.gz"):
    outFile = os.path.join(OUTDIR, re.search('(\d+).gz$', dataFile).groups()[0])
    gunzip('-c', dataFile, _out=outFile)
    print "unzipped", dataFile, "to", outFile
