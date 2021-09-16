import matplotlib.pyplot as plt
from matplotlib import axes
import numpy as np
import sys


# define Python user-defined exceptions
class NotEnoughBytes(Exception):
    """Raise if not enough bytes specified"""
    def __init__(self, message="Please provide at least one (1) byte to graph!!"):
        self.message = message
        super().__init__(self.message)

def get_codes_by_ID(filename, *args):
    lines = []
    with open(filename, 'r') as f:
        lines = f.readlines()

    codes_to_graph = []
    for x in args:
        codes_to_graph.append(x)

    codes_to_extract_from = []
    for line in lines:
        #print(line[:11])
        if line[:11].lstrip() in codes_to_graph:
            #print(f"{line[:11]} found with value: {line[11:]}")
            codes_to_extract_from.append(line[11:].lstrip())
        else:
            pass
    return codes_to_extract_from
def codeToDecimalValues(code):
    '''
    :param code:
    :return:
    '''
    # Remove spaces and \n (newline) chars
    # EX: 28 00 45 88 00 00 00 00 into 2800458800000000
    new_code = code.replace(" ", '')
    new_code = new_code.lstrip().rstrip()

    # Break string into sets of 2
    # EX: 2800458800000000 into [28,00,45,88,00,00,00,00]
    code_list = [new_code[i:i+2] for i in range(0, len(new_code), 2)]

    # Convert all values from HEX to decimal (Base 16 to base 10)
    decimal_code_list = [int(x, 16) for x in code_list]
    # If you want a list of bytes formatted like: 0x4, 0x14, etc then uncomment the line declaring the following list
    # hex_code_list = [hex(x) for x in decimal_code_list]

    return decimal_code_list

# You won't want to graph all of the bits (at least I don't see why we would want to?)
#           So I want it to be like, "pick an index to graph," so like how codes are formatted with A,B, etc on
#           https://github.com/Knio/carhack/blob/master/Cars/Nissan.markdown
# So we will pass the code and the position(s) in the code you want to graph
def get_timestamp(filename, ID):
    # PASS THE NON SORTED PACKET DISSECTION THROUGH HERE
    all_lines = []
    all_times = []
    with open(filename, 'r') as f:
        # Wireshark's packet dissection gives a lot of data, personally I just want the ID and the data sent
        #           So this one sorts out all of the excess information
        all_lines = f.readlines()
    for line in all_lines:
        if "STD: " in line:
            if ID in line:
                timestamp = str(line[8:line.index("CAN")]).lstrip().rstrip()
                all_times.append(float(timestamp))
    #print(all_times)
    return(all_times)


def createGraph(codes,times, *args):
    # Code is a list of lists of decimal values
    #       EX: [[4, 20, 0, 8, 96, 207, 66, 0], [4, 56, 09, 8, 96, 207, 66, 0],[4, 78, 69, 8, 96, 207, 66, 0]]

    ######################################################
    # WARNING I AM SORRY THE FOLLOWING CODE IS VERY UGLY #
    #       IT IS NOT MEMORY EFFICIENT WHATSOEVER        #
    #    BUT IT GETS THE JOB DONE SO FOR NOW ITS FINE    #
    ######################################################

    change_in_values0 = []
    change_in_values1 = []
    change_in_values2 = []
    change_in_values3 = []
    change_in_values4 = []
    change_in_values5 = []
    change_in_values6 = []
    change_in_values7 = []

    for code in codes:
        #for position in args:
            #change_in_values0.append(code[position])
        change_in_values0.append(code[0])
        change_in_values1.append(code[1])
        change_in_values2.append(code[2])
        change_in_values3.append(code[3])
        change_in_values4.append(code[4])
        change_in_values5.append(code[5])
        change_in_values6.append(code[6])
        change_in_values7.append(code[7])
    if len(args) == 0:
        raise NotEnoughBytes
    elif len(args) == 1:
        ydata0 = np.asarray(change_in_values0)
        del change_in_values1
        del change_in_values2
        del change_in_values3
        del change_in_values4
        del change_in_values5
        del change_in_values6
        del change_in_values7
    elif len(args) == 2:
        ydata0 = np.asarray(change_in_values0)
        ydata1 = np.asarray(change_in_values1)
        del change_in_values2
        del change_in_values3
        del change_in_values4
        del change_in_values5
        del change_in_values6
        del change_in_values7
    elif len(args) == 3:
        ydata0 = np.asarray(change_in_values0)
        ydata1 = np.asarray(change_in_values1)
        ydata2 = np.asarray(change_in_values2)
        del change_in_values3
        del change_in_values4
        del change_in_values5
        del change_in_values6
        del change_in_values7
    elif len(args) == 4:
        ydata0 = np.asarray(change_in_values0)
        ydata1 = np.asarray(change_in_values1)
        ydata2 = np.asarray(change_in_values2)
        ydata3 = np.asarray(change_in_values3)
        del change_in_values4
        del change_in_values5
        del change_in_values6
        del change_in_values7
    elif len(args) == 5:
        ydata0 = np.asarray(change_in_values0)
        ydata1 = np.asarray(change_in_values1)
        ydata2 = np.asarray(change_in_values2)
        ydata3 = np.asarray(change_in_values3)
        ydata4 = np.asarray(change_in_values4)
        del change_in_values5
        del change_in_values6
        del change_in_values7
    elif len(args) == 6:
        ydata0 = np.asarray(change_in_values0)
        ydata1 = np.asarray(change_in_values1)
        ydata2 = np.asarray(change_in_values2)
        ydata3 = np.asarray(change_in_values3)
        ydata4 = np.asarray(change_in_values4)
        ydata5 = np.asarray(change_in_values5)
        del change_in_values6
        del change_in_values7
    elif len(args) == 7:
        ydata0 = np.asarray(change_in_values0)
        ydata1 = np.asarray(change_in_values1)
        ydata2 = np.asarray(change_in_values2)
        ydata3 = np.asarray(change_in_values3)
        ydata4 = np.asarray(change_in_values4)
        ydata5 = np.asarray(change_in_values5)
        ydata6 = np.asarray(change_in_values6)
        del change_in_values7
    elif len(args) == 8:
        ydata0 = np.asarray(change_in_values0)
        ydata1 = np.asarray(change_in_values1)
        ydata2 = np.asarray(change_in_values2)
        ydata3 = np.asarray(change_in_values3)
        ydata4 = np.asarray(change_in_values4)
        ydata5 = np.asarray(change_in_values5)
        ydata6 = np.asarray(change_in_values6)
        ydata7 = np.asarray(change_in_values7)

    # change_in_valsX is a list of ints; the ints are only the bytes chosen by the *args
    print(f"Number of values collected: {len(change_in_values0)}")

    xdata = np.asarray(times)



    plt.xlim(min(xdata), max(xdata))




    #########################################
    # IT GETS WORSE, I AM SORRY, IT IS LATE #
    # IF THIS CODE WORKS THEN IM KEEPING IT #
    # PLEASE FORK AND MAKE THIS FUNC BETTER #
    #########################################

    # UPDATE IT WORKS AND I MADE IT *SLIGHTLY* LESS UGLY
    # Thankfully I didn't commit the super ugly version, so I spared your eyes, fellow programmer

    n = 150  # Plot every 150th value (there's so many values to plot, smaller time frames in your capture
    #                           allow for a smaller n)
    plt.plot(xdata[::n], ydata0[::n])
    plt.title("Byte 0 vs. Time")
    plt.show()

    try:
        plt.plot(xdata[::n], ydata1[::n])
        plt.title("Byte 1 vs. Time")
        plt.show()
    except:
        pass
    try:
        plt.plot(xdata[::n], ydata2[::n])
        plt.title("Byte 2 vs. Time")
        plt.show()
    except:
        pass
    try:
        plt.plot(xdata[::n], ydata3[::n])
        plt.title("Byte 3 vs. Time")
        plt.show()
    except:
        pass
    try:
        plt.plot(xdata[::n], ydata4[::n])
        plt.title("Byte 4 vs. Time")
        plt.show()
    except:
        pass
    try:
        plt.plot(xdata[::n], ydata5[::n])
        plt.title("Byte 5 vs. Time")
        plt.show()
    except:
        pass
    try:
        plt.plot(xdata[::n], ydata6[::n])
        plt.title("Byte 6 vs. Time")
        plt.show()
    except:
        pass
    try:
        plt.plot(xdata[::n], ydata7[::n])
        plt.title("Byte 7 vs. Time")

        plt.show()
    except:
        pass



# Get your unsorted packet dissection file, and the ID you want to graph
# Only extract the codes that originate from the arbitration ID specified
codes = get_codes_by_ID('vroom_full.txt', '0x000001f9')
vals = []
for msg in codes:
    # For each code, change all the hex bytes to decimal
    vals.append(codeToDecimalValues(msg))
# Get all of time timestamps for the corresponding codes collected
times = get_timestamp("vroom_full_unsorted.txt", "0x000001f9")
# Graph the specified byte change in with respect to time

createGraph(vals, times, 0, 1, 2, 3, 4, 5, 6, 7)

