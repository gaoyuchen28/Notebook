# 找零兑换

def recMc(coinlist, change):
    mincoin = change
    if change in coinlist:
        return 1
    else:
        for i in [c for c in coinlist if c <= change]:
            numCoin = 1 + recMc(coinlist, change - i)
            if numCoin < mincoin:
                mincoin = numCoin
    return mincoin

print(recMc([1,5,10,25],63))