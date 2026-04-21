# 博物馆大盗

n = 5
weight = [2,3,4,5,9]
value = [3,4,8,8,10]

capacity = 20

def analysis(weight, value, capacity):
    dp = [[0]*(capacity+1) for i in range(n+1)]
    for i in range(1, n+1):
        for w in range(1,capacity+1):
            if weight[i-1] > w:
                dp[i][w] = dp[i-1][w]
            else:
                dp[i][w] = max(dp[i-1][w], dp[i-1][w-weight[i-1]]+value[i-1])
    
    return dp[n][capacity]

print(analysis(weight, value, capacity))