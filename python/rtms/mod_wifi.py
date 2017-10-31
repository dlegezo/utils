
# External modile to work with wifi
import wifi
# To get external IP address for open networks
import requests
# My module to work with PostgreSQL
import mod_postgresql
import mod_gps

# Set the right interface name here
interface = 'wlan0'

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# :::::::::::::::::::::::::::::::::::::::::::::::: wifi stuff :::::::::::::::::::::::::::::::::::::::::

# Just look around and return the networks list
def wifi_discover(wifi_interface):
    wifi_list = wifi.Cell.all(wifi_interface)
    return wifi_list

# Add the new networks
def wifi_add(pg_conn, wifi_list, gps_session):
    for wifi_net in wifi_list:
        # if not wifi_net.encrypted:
        mod_postgresql.pg_add_wifi(pg_conn, wifi_net, gps_session, "0.0.0.1")
            # scheme = wifi.Scheme.for_cell(interface, wifi_net.name, wifi_nezzzzzzzt)
            # print scheme
            # scheme.activate()
            # ext_ip = requests.request('GET', 'http://myip.dnsomatic.com').text
            # mod_postgresql.pg_add_wifi(pg_conn, wifi_net, gps_session, ext_ip)
        #else:
        #   mod_postgresql.pg_add_wifi(pg_conn, wifi_net, gps_session, '0.0.0.1')

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# ::::::::::::::::::::::::::::::::::::::::::::::: entry point :::::::::::::::::::::::::::::::::::::::::

# TODO Add Sigfox and ZigBee support \
# XBee + digi
# Yadom.fr + makers.sigfox.com

if __name__ == '__main__':
    pg_conn = mod_postgresql.pg_connect_db()
    gps_session = mod_gps.gps_open()
    try:
        while True:
            wifi_add(pg_conn, wifi_discover(interface), gps_session)
    except KeyboardInterrupt:
        gps_session.close()
        pg_conn.close()

