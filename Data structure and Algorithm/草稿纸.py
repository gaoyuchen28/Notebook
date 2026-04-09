# Printing Pyramid Patterns
def prints(num):
    if num == 1:
        print("*")
        return
    else:
        prints(num-1)
        for i in range(num):
            print("*", end = " ")
        print("\n", end = "")
prints(5)