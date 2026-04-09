# remove all adjacent duplicates
def rremove(s):
    sb = ""
    n = len(s)
    i = 0
    while i < n:
        repeat = False      
        while i < n-1 and s[i]==s[i+1]:
            repeat = True
            i += 1
        
        if not repeat:
            sb += s[i]
        i += 1
    
    if n == len(sb):
        return sb
    return rremove(sb)

s = "geeksforgeek"
result = rremove(s)
print(result)