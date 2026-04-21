# 利用动态规划解决找零问题_2(返回找钱组合)


def dpMakeChange(change, coinList, mincoin, coinUsed):
    for cent in range(1,change+1):
        count = cent
        newcoin = 1
        for i in [c for c in coinList if c <= cent]:
            if mincoin[cent - i] + 1 < count:
                count = mincoin[cent - i] + 1
                newcoin = i
        mincoin[cent] = count
        coinUsed[cent] = newcoin
    return mincoin[change]

def printChange(coinUsed, change):
    coin = change
    while coin > 0:
        print(coinUsed[coin],end = ", ")
        coin = coin - coinUsed[coin]

coinUsed = [0]*64

dpMakeChange(63, [1,5,10,21,25], [0]*64, coinUsed)
printChange(coinUsed, 63)