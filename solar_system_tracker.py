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
parser.add_argument('--interval', default=5.0, type=float, help="Update interval")
parser.add_argument('--object', default="mars", help="Solar system object")
parser.add_argument('--iters', default=10, type=int, help="Iterations")
args = parser.parse_args()


#
# Establish our location
#
me = ephem.Observer()
me.lat = args.latitude
me.lon = args.longitude


#
# Iterate on position for given object
#

obj = objects[args.object]

for x in range(args.iters):
    me.date = ephem.now()
    obj.compute(me)
    #
    # We use sys.stdout so the we can explicitly flush the buffer on every write
    #
    sys.stdout.write("%s: RA:%s DEC:%s AZ:%s EL:%s\n" % (args.object, obj.ra, obj.dec, obj.az, obj.alt))
    sys.stdout.flush()
    time.sleep(args.interval)
