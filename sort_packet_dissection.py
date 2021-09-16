# This script was written to simplify the output of Wireshark's packet dissection feature (saved as .txt)
import sys
filename = 'vroom.txt'  # Your .txt packet dissection file
hex_value = 54
all_lines = []
lines_with_hex_value = []

with open(filename, 'r') as f:
    all_lines = f.readlines()
# Python gets iffy about reading and writing to a file in the same with statement so I'm writing two

if False: # Change this to false after you run it once on a file, it likes to delete everything if it's been run on a file already
        # Also I highly recommend that you copy the .txt file into another directory / back it up (just in case)
    with open(filename, 'w') as f:
        # Wireshark's packet dissection gives a lot of data, personally I just want the ID and the data sent
        #           So this one sorts out all of the excess information
        for line in all_lines:
            if "STD: " in line:
                f.write(line[line.index("STD:")+4:])
    sys.exit(0)

# The following loop will search all of the codes for those with the hex_value in its data (NOT its ID)
codes_with_hex = []
for line in all_lines:
    #print(line)
    if str(hex_value) in line and str(hex_value) not in line[:11]:
        #print(line)
        codes_with_hex.append(line)

print(f"\n\nNumber of codes containing {hex_value}: {len(codes_with_hex)}")

# Now the following sequence of code will show how many times each ID (that contains the hex in its data) occurs
print("\n__ID occurrences__:")
ids = []

for code in codes_with_hex:
    ids.append(code[:11])

occur = [[x,ids.count(x)] for x in set(ids)]
for i in range(0, len(occur)):
    print(f"{occur[i][0]} occurs with '{hex_value}' exactly {occur[i][1]} time(s)")

