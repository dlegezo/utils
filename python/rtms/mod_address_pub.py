
# Simple resolver Coords -> post address
# Sample: mod_address.py '55.763112 37.615814'
# Denis Legezo, 2016

# Add post address by the coords to the database
from geopy.geocoders import GoogleV3
import sys

# Let's add post address
def get_place(coords):
    geolocator = GoogleV3()
    return geolocator.reverse(coords)[0][0]

if __name__=="__main__":
    try:
        # E.g. for Moscow center
        # get_place('55.763112 37.615814')
        print get_place(sys.argv[1])
    except IndexError:
        print "Usage: mod_address.py '<lat> <long>'"