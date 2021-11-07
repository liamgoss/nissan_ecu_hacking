# Welcome to Nissan_USB2CAN (AKA usb2can2py) by Liam Goss
# I wrote this because I could not find any decent software to work with the Korlan usb2can device I bought
# The usb2can drivers for windows are much easier so I am writing this code for use on windows (via bootcamp on my mac)
# Resources
# https://python-can.readthedocs.io/en/master/api.html
# https://python-obd.readthedocs.io/en/latest/



import math, time, sys
from datetime import datetime
import obd
import usb.core
import usb.backend.libusb1

# I am fiddling around with modifying the python-can library
# You should change the below import statements from 'can_custom' to 'can'
import can_custom as can
from can_custom.interfaces.usb2can.usb2canabstractionlayer import *


# SYS_DEBUG can be set to True if you want to use the logging library to have a very verbose output
# FUNC_DEBUG is a variable that will be checked in functions and then *certain* tracebacks and print statements will
#               be executed accordingly
SYS_DEBUG = False
FUNC_DEBUG = True

if SYS_DEBUG:
    import logging
    logging.basicConfig(level=logging.DEBUG)

def send_msg(channel, id, data):
    '''
    send_msg() uses the 'can' library to send a message to the can bus
    :param id:
    :param data:
    :param interface:
    :return:
    '''

    with can.interface.Bus(bustype='usb2can', channel=channel, bitrate=500000) as bus:
        arbitration_id = id
        msg = can.Message(arbitration_id=arbitration_id, data=data, is_extended_id=True)
        try:
            bus.send(msg)
            print(f"Message sent on channel {channel}")
        except can.CanError:
            print("Message NOT sent")
            return

    print("__{0}/{1} Data__".format('0x' + str(hex(arbitration_id))[2:].zfill(8), arbitration_id))
    print(f"hex: {hex(data[0])}, {hex(data[1])}, {hex(data[2])}, {hex(data[3])}, {hex(data[4])}, {hex(data[5])}, "
          f"{hex(data[6])}, {hex(data[7])}")
    print(f"dec: {data[0]}, {data[1]}, {data[2]}, {data[3]}, {data[4]}, {data[5]}, {data[6]}, {data[7]}")

def calculate_horsepower(final_speed, delta_time, init_speed=0.00):
    '''
    :param speed: in MPH
    :param time: in seconds
    :param mass: in kg
    :return:
    '''
    mass = 1505.9267  # Mass (kg) of a base 2008 Nissan 350z, change accordingly if needed
    # An alternative formula for calculating horsepower is (torque [lb-ft] * RPM) / 5252 but I don't know how to
    #               reliably get live torque data. Maybe I'll introduce another function with some basic estimates?
    # Google says that 90% of the Z's torque (268 lb-ft) is available between 2,000 and 7,000 RPM and that it gets
    #               306 HP @ 6,800 RPM; from there we can probably reverse engineer some values, but either way we are
    #               guessing without a dyno
    # Or you could also do: (Force [lbs] * Radius of rear wheel+tire [feet] * RPM) / 5252
    # But I figured with tire and rim size variations, it isn't the best standard use case, but the formula is here
    #               in case you'd like to implement it
    # If you REALLY want to get fancy, the coefficient of drag is 0.3 (0.29 for grand tourismo? don't quote me on that)
    #               so feel free to do some wicked math and submit a pull request :)

    # The math here, although I think checks out (grade wise I did amazing in physics but my gosh my understanding of
    #                          it is much much less), but it seems off. I think I need to set it up to handle taking the
    #                          time between 2 speeds and not just assuming it starts at 0

    # If you can weigh your own car and change this value, that would be ideal, but I cannot so I am using the internet
    init_speed = init_speed / 2.237  # MPH to m/s: divide MPH by 2.237
    final_speed = final_speed / 2.237
    # time will be in the correct units [seconds]
    # Avg. HP = (((1/2)mv^2)/t)/746
    # 1/2mv^2 is the kinetic energy of an object; m in kg, v in m/s
    # t is time (in seconds) it takes to achieve v (in this theory, from zero - we can do some algebra and physics
    #                                  to get it from a nonzero start)
    # Gives us a the expression so far (in parentheses) gives us Joules/second which is equivalent to Watts
    # 1 HP = 746 Watts so we divide by 746 to cancel out watts and solve for HP

    init_kinetic_energy = 0.5 * mass * (init_speed * init_speed)
    final_kinetic_energy = 0.5 * mass * (final_speed * final_speed)
    delta_kinetic_energy = final_kinetic_energy - init_kinetic_energy
    #print(f"Kinetic energy: {delta_kinetic_energy} Joules (J)")
    watts = delta_kinetic_energy / float(delta_time)
    horsepower = watts / 746.00
    horsepower = int(math.ceil(horsepower)) # round up to nearest whole number - could round down but I mean it's an ego thing at this point
    print(f"Horsepower: {horsepower} HP")

    # After I get the math down solid I will add code to generate graphs and then later on these can be placed on a GUI

    return horsepower

def get_metrics():
    # This function will get the current speed of the car and start a stopwatch at t=0
    # Then it will go X amount of seconds and grab the final speed, then return this to be fed into calculate_horsepower()
    # Using ID 280
    final_speed = 60.0
    init_speed = 0.0
    delta_time = 5.0
    return final_speed, delta_time, init_speed

def listen(channel, askUser=False, numCodes=100):
    '''
    :param askUser: ~ if True, ask the user for the filename
    :return:
    '''
    bus = can.interface.Bus(bustype='usb2can', channel=channel, bitrate=500000)
    print(str(bus.state) + '\n' + str(bus.channel_info))
    if bus.state.value != 1:
        raise Exception("Your bus is not active!")
    time.sleep(0.5)

    if askUser:
        filename = input("Enter the basename (without extension) for file: ")
        filename = filename + ".log"
    else:
        filename = datetime.now().strftime("%Y%m%d-%H%M%S")
        filename = filename + ".log"
    print(filename)
    listener = can.CanutilsLogWriter(filename, channel=channel, append=False)

    if numCodes == 'inf':
        #raise Exception("Okay, I lied, 'inf' isn't ready yet...")
        try:
            while True:
                listener.on_message_received(bus.recv())
        except KeyboardInterrupt:
            listener.stop()  # Doesn't stop loop :(
    else:
        i = 0
        while i < int(numCodes):
            listener.on_message_received(bus.recv())
            i = i + 1
    print("Closing listener...")
    print(f"Session saved to {filename}")
    listener.stop()

# Arbitration ID and data must be in the following (hex) format
id = 0x0000060D
data = [0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED, 0x69, 0x69]  # placeholder hex values
#send_msg(channel='BC0EF943',id,data)


# In order to listen until CTRL+C is pressed, set numCodes='inf'
# Otherwise, if you want X amount of codes read, set numCodes=X
listen(channel='BC0EF943', askUser=False, numCodes='inf')


#final_speed, delta_time, initial_speed, = get_metrics()
#hp = calculate_horsepower(final_speed, delta_time, initial_speed) # final speed, delta time, init speed


