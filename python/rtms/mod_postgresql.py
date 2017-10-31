
from psycopg2 import *
# To get sensors' position
from bluetooth import *

pg_db_name = "rtms"
# Now setted for Moscow city center table
pg_table_name = "tab_wifi_cao"

# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# :::::::::::::::::::::::::::::::::::: sensors stuff :::::::::::::::::::::::::::::::::::::::
# Connect to the database
def pg_connect_db():
    pg_conn_str = "host=localhost dbname="+pg_db_name+" user=postgres password=1"
    pg_conn = connect(pg_conn_str)
    return pg_conn

# Clear and exit
def pg_close_db(pg_conn, pg_cursor_ins, pf_cursor_sel):
    pg_conn.commit()
    pg_cursor_ins.close()
    pg_cursor_sel.close()
    pg_conn.close()

# Get the already found sensors from the database, we'll not add it twice
# TODO may be better catch exception if the primary key is the same
def pg_get_existing(rtms_conn, column, table):
    pg_cursor_sel = rtms_conn.cursor()
    pg_cursor_sel.execute('SELECT %s FROM %s' % (column, table))
    return pg_cursor_sel

# Make a list from already added sensors
def pg_get_existing_list(pg_cursor):
    rtms_list = []
    for dev in pg_cursor:
        rtms_list.append(dev[0])
    return rtms_list

# Add new sensors to the database
# TODO Change text to macaddr in tables for bt and wifi
def pg_add_new(pg_conn, rtms_list, bt_devices, gps_session):
    pg_cursor_ins = pg_conn.cursor()
    for bt_device in bt_devices:
        print 'Checking %s' % bt_device
        if bt_device not in rtms_list:
            print '%s wasnt in the base before' % bt_device
            # If rtms_name in lookup_name(bt_device):
            print 'its RTMS alright! adding %s' % bt_device
            # Get actual coordinates
            gps_session.next()
            try:
                pg_cursor_ins.execute('INSERT INTO tab_wifi_cao (btid, friendly, latitude, longitude) \
                    VALUES (%s, %s, %s, %s)', (bt_device, lookup_name(bt_device), \
                                               gps_session.fix.latitude, gps_session.fix.longitude))
                pg_conn.commit()
            except IntegrityError:
                pass
    return pg_cursor_ins

# Clear sensors database
def pg_clear_db(pg_conn):
    pg_cursor_del = pg_conn.cursor()
    pg_cursor_del.execute('DELETE FROM rtms_table WHERE true')
    pg_conn.commit()
    return pg_cursor_del

# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# :::::::::::::::::::::::::::::::::::::: wifi stuff ::::::::::::::::::::::::::::::::::::::::
# Add wifi network
def pg_add_wifi(pg_conn, wifi_net, gps_session, ext_ip):
    pg_cursor_add = pg_conn.cursor()
    if not pg_existing_wifi(pg_conn, wifi_net.address):
        print 'new wifi network %s' % wifi_net.address
        # Get actual coordinates
        gps_session.next()
        try:
            if wifi_net.encrypted:
                print gps_session.fix.latitude
                pg_cursor_add.execute('INSERT INTO tab_wifi_cao (address, ssid, encrypted, encryption_type, latitude, \
                                                                 longitude, ip) \
                            VALUES (%s, %s, %s, %s, %s, %s, %s)', (wifi_net.address, wifi_net.ssid, \
                                                               wifi_net.encrypted, wifi_net.encryption_type, \
                                                               gps_session.fix.latitude, gps_session.fix.longitude, ext_ip))
            else:
                print gps_session.fix.latitude
                pg_cursor_add.execute('INSERT INTO tab_wifi_cao (address, ssid, encrypted, latitude, longitude, ip) \
                            VALUES (%s, %s, %s, %s, %s, %s)', (wifi_net.address, wifi_net.ssid, \
                                                               wifi_net.encrypted, gps_session.fix.latitude, \
                                                               gps_session.fix.longitude, ext_ip))
            pg_conn.commit()
        except IntegrityError:
            pass
    pg_cursor_add.close()

# Is address already among wifi networks in the database
# TODO may be exception and no existence check also?
def pg_existing_wifi(pg_conn, address):
    pg_cursor_sel = pg_conn.cursor()
    pg_cursor_sel.execute('SELECT address FROM tab_wifi_cao')
    wifi_list = []
    for wifi_net in pg_cursor_sel:
        wifi_list.append(wifi_net[0])
    if address in wifi_list:
        pg_cursor_sel.close()
        return True
    else:
        pg_cursor_sel.close()
        return False
