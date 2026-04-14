# 分发糖果

def candy(ratings):
    cds = [1]*len(ratings)
    for i in range(1,len(ratings)):
        if ratings[i-1] < ratings[i]:
            cds[i] = cds[i-1]+1
        elif ratings[i-1] == ratings[i]:
            cds[i] = 1
        else: # 如果比前面低的话要讨论很多方案
            cds[i] = 1
            if cds[i-1] == 1:
                for k in range(i-1, -1, -1): # 这个必须要倒叙
                    cds[k] += 1
                    if k > 0 and (ratings[k] >= ratings[k-1] or cds[k]>cds[k-1]):
                        break
    return cds

ratings = "122"

print(candy(ratings))
