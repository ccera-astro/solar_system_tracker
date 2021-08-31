#!/usr/bin/python
import time
import ephem
import math
import argparse
import sys

objects = {"mars" : ephem.Mars(), "sun" : ephem.Sun(), "venus" : ephem.Venus(),
    "mercury" : ephem.Mercury(), "moon" : ephem.Moon(), "jupiter" : ephem.Jupiter(),
    "saturn" : ephem.Saturn(), "neptune" : ephem.Neptune(), "uranus" : ephem.Uranus(),
    "pluto" : ephem.Pluto()}

parser = argparse.ArgumentParser()

parser.add_argument('--latitude', default='44.90', help="Local latitude")
parser.add_argument('--longitude', default='-76.03', help="Local longitude")
parser.add_argument ('--elevation', default=100.0, type=float, help="Local elevation (meters)")
parser.add_argument('--interval', default=5.0, type=float, help="Update interval")
parser.add_argument('--object', default="mars", help="object name")
parser.add_argument('--iters', default=10, type=int, help="Iterations")
parser.add_argument('--satellite', default=False, help="satellite mode", action="store_true")
parser.add_argument('--catalog', default=False, help="catalog object mode", action="store_true")
parser.add_argument('--file', default=None, help="dB file (either .edb or tle file")
args = parser.parse_args()


#
# Establish our location
#
me = ephem.Observer()
me.lat = args.latitude
me.lon = args.longitude
me.elevation = args.elevation


#
# Iterate on position for given object
#

#
# Solar-system object
#
if (args.satellite == False and args.catalog == False):
    obj = objects[args.object]

#
# Catalog object--using .edb catalogs
#
if (args.catalog == True):
	found = False
	fp = open (args.file, "r")
	while True:
		l = fp.readline()
		l.strip('\n')
		if (args.object in l):
			obj = ephem.readdb(l)
			found = True
			break
	if (found == False):
		raise KeyError("Object %s not found in catalog" % args.object)

#
# Satellite object using TLEs
#			
elif (args.satellite == True):
	found = False
	fp = open (args.file, "r")
	while True:
		l1 = fp.readline()
		if (l1 == ""):
			break
		if (l1 == None):
			break
		l1.strip('\n')
		if (args.object in l1):
			l2 = fp.readline().strip("\n")
			l3 = fp.readline().strip("\n")
			obj = ephem.readtle(l1, l2, l3)
			found = True
			break
	if (found == False):
		raise KeyError("Object %s not found in TLE data" % args.object)
	
for x in range(args.iters):
    me.date = ephem.now()
    obj.compute(me)
    #
    # We use sys.stdout so the we can explicitly flush the buffer on every write
    #
    sys.stdout.write("%s: RA:%s DEC:%s AZ:%s EL:%s\n" % (args.object, obj.ra, obj.dec, obj.az, obj.alt))
    sys.stdout.flush()
    time.sleep(args.interval)
