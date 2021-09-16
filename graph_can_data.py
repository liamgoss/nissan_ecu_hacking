import matplotlib.pyplot as plt
import numpy as np



filename = "vroom_full.txt"
lines = []
with open(filename, 'r') as f:
    lines = f.readlines()

codes_to_graph = ['0x000002d1']
codes_to_extract_from = []
for line in lines:
    #print(line[:11])
    if line[:11].lstrip() in codes_to_graph:
        #print(f"{line[:11]} found with value: {line[11:]}")
        codes_to_extract_from.append(line[11:].lstrip())
    else:
        pass
def codeToDecimalValues(code):
    '''
    :param code:
    :return:
    '''
    new_code = code.replace(" ", '')
    code_list = [new_code[i:i+2] for i in range(0, len(new_code), 2)]
    decimal_code_list = [int(x, 16) for x in code_list]
    # If you want a list of bytes formatted like: 0x4, 0x14, etc then uncomment the line declaring the following list
    # hex_code_list = [hex(x) for x in decimal_code_list]
    print(code_list)
    print(decimal_code_list)
    return decimal_code_list

# You won't want to graph all of the bits (at least I don't see why we would?)
#           So I want it to be like, "pick an index to graph," so like how codes are formatted with A,B, etc on
#           https://github.com/Knio/carhack/blob/master/Cars/Nissan.markdown
# So we will pass the code and the position(s) in the code you want to graph
def createGraph(codes, *args):
    # Code is a list of lists of decimal values
    #       EX: [[4, 20, 0, 8, 96, 207, 66, 0], [4, 56, 09, 8, 96, 207, 66, 0],[4, 78, 69, 8, 96, 207, 66, 0]]

    change_in_values = []
    for code in codes:
        for position in args:
            change_in_values.append(code[position])
    print(change_in_values)

    '''    
    xdata = np.asarray(code)
    print(len(xdata))
    ydata = list(range(0, len(code)))
    print(len(ydata))


    # Plot the data:
    plt.plot(xdata, ydata)


    plt.show()
    '''

tmp_list = ["28 00 45 88 00 00 00 00", "28 00 45 a1 00 00 00 00"]

list_of_codes = []
for x in tmp_list:
    list_of_codes.append(codeToDecimalValues(x))
createGraph(list_of_codes, 3)

# TODO: Comment this so as not to confuse everyone; even looking at this I'm kinda like WTF is this code again??
#createGraph(codes_to_extract_from)