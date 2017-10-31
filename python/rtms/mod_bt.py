
from bluetooth import *
import serial
import os

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# ::::::::::::::::::::::::::::::::::::::::::::::: bluetooth stuff :::::::::::::::::::::::::::::::::::::
# Take a look around
def bt_discover():
    bt_devices = discover_devices(duration=3, flush_cache=True, lookup_names=False)
    return bt_devices
    # To ask for bt services do following
    # if len(bt_devices) > 0:
    #     try:
    #         service = find_service(address=bt_devices[0])
    #         pprint(service)
    #     except IndexError:
    #         pass

# Connect via serial port
def bt_connect(btid):
    # Let's add sensor ID to the rfcomm.conf
    print 'making rfcomm.conf'
    bt_conf_file = open('/etc/bluetooth/rfcomm.conf', 'w')
    bt_conf_file.write('rfcomm0 {\n')
    bt_conf_file.write('\tbind yes;\n')
    bt_conf_file.write('\tdevice %s;\n' % btid)
    bt_conf_file.write('\tchannel 1;\n')
    bt_conf_file.write('\tcomment "Serial Port";\n')
    bt_conf_file.write('\t}\n')
    bt_conf_file.close()

    # Let's add sensor pass to the pincodes
    print 'making pincodes'
    if not os.path.exists('/var/lib/bluetooth/%s/' % btid):
        os.makedirs('/var/lib/bluetooth/%s/' % btid)
    bt_conf_file = open('/var/lib/bluetooth/%s/pincodes' % btid, 'w+')
    bt_conf_file.write('admin')
    bt_conf_file.close()

    print 'binding all'
    os.system('sudo rfcomm bind all')

# Send some commands to the sensor
def bt_send(btid):
    print 'opening serial'
    bluetoothSerial = serial.Serial("/dev/rfcomm1", baudrate=9600)
    print 'writing serial'
    bluetoothSerial.write('\xFF\xA1\x01')
    try:
        rtms_out_file = open('./out', 'w+')
        rtms_out_file.write(bluetoothSerial.read())
        # print bluetoothSerial.readline()
        # print bluetoothSerial.readline()
        bluetoothSerial.close()
    except serial.SerialException:
        print 'serial exception'
        bluetoothSerial.close()

if __name__ == '__main__':
    # try:
    #     while True:
    #         bt_devices = bt_discover()
    #         if len(bt_devices) > 0:
    #             for bt_device in bt_devices:
    #                 bt_connect(bt_device)
    #                 bt_send(bt_device)
    # except KeyboardInterrupt:
    #     pass

    bluetoothSerial = serial.Serial("/dev/rfcomm0", baudrate=9600)
    rtms_out_file = open('./out', 'a+')
    rtms_out_file.write(bluetoothSerial.readlines())
    bluetoothSerial.close()
