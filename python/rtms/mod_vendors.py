
# Add vendors and street addresses to the bases
from netaddr import *
from psycopg2 import *
from geopy.geocoders import GoogleV3

# Let's know the vendor
def get_org_by_mac(mac):
    try:
        mac_obj = EUI(mac)
        oui = mac_obj.oui
        return oui.registration().org
    except NotRegisteredError:
        return 'No Vendor'

# Get vendor and address by MAC and GPS coordinates
def get_vendors(table_dest, table_source, clause):
    pg_conn = connect("host=localhost dbname=rtms user=postgres password=1")
    pg_cursor = pg_conn.cursor()
    wifi_list = []

    # Copy needed networks
    pg_cursor.execute("DELETE FROM %s WHERE True" % table_dest)
    pg_cursor.execute("INSERT INTO %s (address, encrypted, ssid, encryption_type, latitude, longitude) \
        SELECT address, encrypted, ssid, encryption_type, latitude, longitude \
        FROM %s WHERE %s" % (table_dest, table_source, clause))

    # Get addresses list
    pg_cursor.execute("SELECT address, latitude, longitude FROM %s" % table_dest)
    for dev in pg_cursor:
        wifi_list.append(dev)

    # Add vendor for every address
    for netw in wifi_list:
        pg_cursor.execute("UPDATE %s SET vendor='%s' WHERE address='%s'" % (table_dest, get_org_by_mac(netw[0]), netw[0]))
        # pg_cursor.execute("UPDATE %s SET place='%s' WHERE address='%s'" % (table_dest, get_place(str(netw[1])+ ' ' + str(netw[2])),\
        #                                                                 netw[0]))

    pg_conn.commit()
    pg_cursor.close()
    pg_conn.close()

# Let's copy needed data form tab_wifi and add vendors to it
def get_rtms_vendors(table_dest, table_source, clause):
    pg_conn = connect("host=localhost dbname=rtms user=postgres password=1")
    pg_cursor = pg_conn.cursor()
    rtms_list = []

    # Copy needed networks
    pg_cursor.execute("DELETE FROM %s WHERE True" % table_dest)
    pg_cursor.execute("INSERT INTO %s (btid, friendly, latitude, longitude) \
        SELECT btid, friendly, latitude, longitude \
        FROM %s WHERE %s" % (table_dest, table_source, clause))

    # Get addresses list
    pg_cursor.execute("SELECT btid, latitude, longitude FROM %s" % table_dest)
    for dev in pg_cursor:
        rtms_list.append(dev)

    # Add vendor for every address
    for netw in rtms_list:
        pg_cursor.execute("UPDATE %s SET vendor='%s' WHERE btid='%s'" % (table_dest, get_org_by_mac(netw[0]), netw[0]))
        # pg_cursor.execute("UPDATE %s SET place='%s' WHERE btid='%s'" % (table_dest, get_place(str(netw[1])+ ' ' + str(netw[2])),\
        #                                                                 netw[0]))

    pg_conn.commit()
    pg_cursor.close()
    pg_conn.close()

# Let's add post address
def get_place(coords):
    # TODO Get the names of the place
    geolocator = GoogleV3()
    return geolocator.reverse(coords)[0][0]

if __name__=="__main__":
    get_vendors('tab_wifi_vendor', 'tab_wifi', "True")
    # get_rtms_vendors('tab_rtms_vendor', 'tab_rtms', "True")

    # TODO RTMS uses different colums. Better to add vendors with PL\Python in View
    # http://www.postgresql.org/docs/9.0/static/plpython.html