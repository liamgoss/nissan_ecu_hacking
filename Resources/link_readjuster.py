lines = []
with open('helpful_links.txt', 'r') as f:
    lines = f.readlines()
with open('helpful_links.txt', 'w') as f:
    for line in lines:
        if "ADD_DATE" in line:
            index = line.index("\" ADD_DATE")
            line = line[:index] + "\n"
            f.write(line)
        else:
            f.write(line.lstrip())
