def divide_8(dec_num):
    rem_num = []
    while dec_num >0:
        rem = dec_num % 8
        rem_num.append(rem)
        dec_num = dec_num//8
    
    bin_string = ""
    while rem_num:
        bin_string = bin_string +str(rem_num.pop())

    return bin_string

decimal = int(input())
print(divide_8(decimal))