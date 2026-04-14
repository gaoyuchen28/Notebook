# 找零兑换优化

def recMc(coinlist, change, knowresult):
    mincoin = change
    if change in coinlist:
        knowresult[change] = 1
        return 1
    elif knowresult[change] > 0:
        return knowresult[change]
    else:
        for i in [c for c in coinlist if c <= change]:
            numCoin = 1 + recMc(coinlist, change - i, knowresult)
            if numCoin < mincoin:
                mincoin = numCoin
                knowresult[change] = mincoin
    return mincoin

print(recMc([1,5,10,25],63, [0]*64))