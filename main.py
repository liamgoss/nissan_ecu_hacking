# Welcome to Nissan_USB2CAN (AKA usb2can2py) by Liam Goss
# I wrote this because I could not find any decent software to work with the Korlan usb2can device I bought
# The usb2can drivers for windows are much easier so I am writing this code for use on windows (via bootcamp on my mac)
# Resources
# https://python-can.readthedocs.io/en/master/api.html
# https://python-obd.readthedocs.io/en/latest/
import sys

import can
import obd
import usb.core
import usb.backend.libusb1
import logging
# logging.basicConfig(level=logging.DEBUG)
from can.interfaces.usb2can.usb2canabstractionlayer import *
from can.interfaces.usb2can import Usb2canBus


# The korlan usb2can doesn't like to be detected by this code on Windows 10
#           Could be a driver issue on my end (it shows up as USB and not a COM port like I would prefer, but that
#           likely is a feature not an error)
# Right now this code is being written for Windows 10, but I plan on making this work on Linux as well (i.e. raspbian)

# ID for speed is (maybe) 354, 355, or 280 and ID for RPM is 1F9
# TODO: figure out live torque/horsepower calculation --- can we get crankshaft position and do some angular velocity type physics?

def send_msg(id, data, interface=None):
    '''
    send_msg() uses the 'can' library to send a message to the can bus
    :param id:
    :param data:
    :param interface:
    :return:
    '''
    # NOTE: it's possible that this wont find the usb because of the following, non-fatal errors:
    '''
    Kvaser canlib is unavailable.
    fcntl not available on this platform
    libc is unavailable
    '''
    # As for the above to-do, it could also be due to the library looking for COM ports and not USB
    interfaces = can.interface.detect_available_configs()
    print(interfaces)
    channel = interfaces[0]['channel']
    # TODO: add interface selection code
    if type(data) == list:
        print("Type is list")
    # print(interfaces)
    # Running on a virtual CAN bus for now since that allows at least a basic test of functionality
    with can.interface.Bus(bustype='virtual', channel=channel, bitrate=500000) as bus:
        # data = [0x20, 0x00, 0x1f, 0xbd, 0x00, 0x00, 0x00, 0x00]
        arbitration_id = id
        msg = can.Message(arbitration_id=arbitration_id, data=data, is_extended_id=True)
        try:
            bus.send(msg)
            print(f"Message sent on virtual {bus.channel_info}")
        except can.CanError:
            print("Message NOT sent")
            return
    print("__{0}/{1} Data__".format('0x' + str(hex(arbitration_id))[2:].zfill(8), arbitration_id))
    print(f"hex: {hex(data[0])}, {hex(data[1])}, {hex(data[2])}, {hex(data[3])}, {hex(data[4])}, {hex(data[5])}, "
          f"{hex(data[6])}, {hex(data[7])}")
    print(f"dec: {data[0]}, {data[1]}, {data[2]}, {data[3]}, {data[4]}, {data[5]}, {data[6]}, {data[7]}")


# Arbitration ID and data must be in the following (hex) format
id = 0x000001f9
data = [0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED, 0x69, 0x69]
send_msg(id, data, 'vcan0')


# The following code is deprecated code but I am keeping it here in case you find it useful :)
'''
# The vendor and Product ID correspond to the ID's of the usb2can found  in W10 device manager or various linux commands 
VENDOR_ID = '0483'
PRODUCT_ID = 1234

device = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)

if device is None:
    raise ValueError("No matching USB device found!")
print("Device found!")
usb.core.util.claim_interface(device, 0)
'''
'''
dev = usb.core.find(find_all=True)
# loop through devices, printing vendor and product ids in decimal and hex
for cfg in dev:
  print('Decimal VendorID=' + str(cfg.idVendor) + ' & ProductID=' + str(cfg.idProduct) + '\n')
  print('Hexadecimal VendorID=' + hex(cfg.idVendor) + ' & ProductID=' + hex(cfg.idProduct) + '\n\n')
'''
'''
ports = obd.scan_serial()
print(ports)
obd.logger.setLevel(obd.logging.DEBUG)

connection = obd.OBD()

if connection.is_connected():
    print("OBD2 connected on {0} using {1}".format(connection.port_name()), connection.protocol_name())
    print("RPM Reads:")

    rpm = obd.commands.RPM
    print(rpm)
else:
    print("OBD2 not connected...")
print("Closing connection (if any)")
connection.close()
'''


