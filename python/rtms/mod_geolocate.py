
# Get the longitude and latitude by 2 nearby WiFi devices MACs
# It could be only routers, any devices indexed by Google will fit
# Please replace <your Google API key> with your real one or ask me for mine
# Usage: mod_geolocate.py <first MAC> <second MAC>
# E.g. by two KL wireless networks:
# mod_geolocate.py 34:BD:C8:17:33:10 34:BD:C8:17:33:14
# Denis Legezo, 2016

import urllib2
import json
import sys

GOOGLE_API_KEY='key_here'

def geo_get_coords(mac1, mac2, json_file):
        url = 'https://www.googleapis.com/geolocation/v1/geolocate?key='+GOOGLE_API_KEY
        wifi_array = [{'macAddress': mac1},
                      {'macAddress': mac2}]
        postdata = {'wifiAccessPoints': wifi_array}

        req = urllib2.Request(url)
        req.add_header('Content-Type','application/json')
        data = json.dumps(postdata)
        ret = urllib2.urlopen(req,data)
        ret_json = ret.read()
        f = open(json_file, 'w')
        f.write(ret_json)
        f.close()

        with open(json_file) as data_file:
            data = json.load(data_file)

        print(data['location']['lat'])
        print(data['location']['lng'])
        data_file.close()

# Entry point
if __name__=="__main__":
    try:
        geo_get_coords(sys.argv[1], sys.argv[2], './json')
    except IndexError:
        print 'Usage: mod_geolocate.py <first MAC> <second MAC>'
