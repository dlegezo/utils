
from gps import *

# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# :::::::::::::::::::::::::::::::::::::: gps stuff :::::::::::::::::::::::::::::::::::::::::
def gps_open():
    gps_session = gps(mode=1)
    gps_session.next()
    gps_session.next()
    gps_session.next()
    gps_session.next()
    gps_session.next()
    gps_session.next()
    return gps_session

def gps_get_latitude(gps_session):
    gps_session.next()
    return gps_session.fix.latitude

def gps_get_longitude(gps_session):
    gps_session.next()
    return gps_session.fix.longitude

def gps_close(gps_session):
    gps_session.close()