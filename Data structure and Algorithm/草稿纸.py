# Length of longest palindromic sub-string
def test(n, left, right, count):
    if left > right:
        return count
    if left == right:
        return count +1
    if n[left] == n[right]:
        count = test(n, left+1, right-1, count+2)
        return max(count, max(test(n, left+1, right, 0), test(n,left, right-1,0)))
    return max(test(n, left+1, right, 0), test(n,left, right-1,0))

if __name__ == "__main__":
    str = "abca"
    n = len(str)
    
    print(test(str, 0, n - 1, 0))