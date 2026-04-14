# Convert a String to an Integer
def Convert(str):
    if len(str) == 1:
        return int(str[0])
    else:
        return 10*Convert(str[:(len(str)-1)]) + int(str[len(str)-1])

print(Convert("02345"))