# 利用动态规划解决找零问题_1


def dpMakeChange(change, coinList, mincoin):
    for cent in range(1,change+1):
        count = cent
        for i in [c for c in coinList if c <= cent]:
            if mincoin[cent - i] + 1 < count:
                count = mincoin[cent - i] + 1
        mincoin[cent] = count
    return mincoin[change]

print(dpMakeChange(63, [1,5,10,21,25], [0]*64))