def divide_by_2(dec_num):
    rem_num = []
    while dec_num > 0:
        rem = dec_num % 2
        rem_num.append(rem)
        dec_num = dec_num // 2
    
    bin_string = ""
    while rem_num:
        bin_string = bin_string + str(rem_num.pop())
    return bin_string

print(divide_by_2(233))