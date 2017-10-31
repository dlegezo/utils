# :::::::::::::::::::::::::::::::: RTMS G4 sensors locator :::::::::::::::::::::::::::::::::
# ::::::::::::::::::::::::::::::::: Denis Legezo, 2015 :::::::::::::::::::::::::::::::::::::

# ::::::::::::::::::::::::::::::::::::: global stuff :::::::::::::::::::::::::::::::::::::::
# To discover and connect to sensors
import mod_bt
# To save findings in PostgreSQL
import mod_postgresql
# To get coordinates
import mod_gps

# We know part of the name (RTMS), so let's find sensors using it
# Other method is to use the known bluetooth ID's
rtms_name = 'RTMS'

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# ::::::::::::::::::::::::::::::::::::::::::::::::: Entry point :::::::::::::::::::::::::::::::::::::::

if __name__=="__main__":
    
    # In case if I need to clean the list of sensors
    #mod_postgresql.pg_clear_db(rtms_conn)

    # Connect to Postgresql
    pg_conn = mod_postgresql.pg_connect_db()
    gps_session = mod_gps.gps_open()

    # The main device searching loop
    try:
        while True:
            bt_devices = mod_bt.bt_discover()
            # print('cycle')
            if bt_devices != []:
                print 'found something!'
                for bt_device in bt_devices:
                    # mod_bt.bt_connect(bt_device)
                    # mod_bt.bt_send(bt_device)
                    pg_cursor_sel = mod_postgresql.pg_get_existing(pg_conn, 'btid', 'tab_rtms')
                    rtms_sensors = mod_postgresql.pg_get_existing_list(pg_cursor_sel)
                    pg_cursor_ins = mod_postgresql.pg_add_new(pg_conn, rtms_sensors, bt_devices, gps_session)
    except KeyboardInterrupt:
        # Cleaning and exit
        gps_session.close()
        mod_postgresql.pg_close_db(pg_conn, pg_cursor_sel, pg_cursor_ins)
