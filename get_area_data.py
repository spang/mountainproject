#!/usr/bin/python3

import requests
import sys, os

DATADIR = 'data'

areas = dict(spain="106111770", gunks="105798167", leavenworth="105790610",
        mazama="106112166", index="105790635", crowhill="105905492",
        quincy="105908121", cathedral="105908823",
        whitehorse="105909079", seneca="105861910")

def aws_url(area_id):
    return 'http://s3.amazonaws.com/MobilePackages/' + area_id + '.gz'

def aws_img_url(area_id):
    return 'http://s3.amazonaws.com/MobilePackages/' + area_id + '_img.tgz'

if not os.path.exists(DATADIR):
    os.makedirs(DATADIR)

for name, area_id in areas.items():
    area_data_fname = name+"-"+area_id+'.gz'
    area_img_fname = name+"-"+area_id+'_img.tgz'
    r = requests.get(aws_url(area_id))
    if r.ok:
        open(os.path.join(DATADIR, area_data_fname), 'wb').write(r.content)
        print("got file", area_data_fname)
    else:
        print("error getting file", area_data_fname, file=sys.stderr)
    r = requests.get(aws_img_url(area_id))
    if r.ok:
        open(os.path.join(DATADIR, area_img_fname), 'wb').write(r.content)
        print("got file", area_img_fname)
    else:
        print("error getting file", area_img_fname, file=sys.stderr)
