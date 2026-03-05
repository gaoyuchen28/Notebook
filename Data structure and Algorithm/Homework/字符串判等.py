# 描述
# 判断两个由大小写字母和空格组成的字符串在忽略大小写，且忽略空格后是否相等。
# 输入
# 两行，每行包含一个字符串。
# 输出
# 若两个字符串相等，输出YES，否则输出NO。

s1 =input()
s2 =input()
s1 =s1.lower()
s2 =s2.lower()
s1 =s1.replace(" ","")
s2 =s2.replace(" ","")
if s1 == s2:
    print("YES")
else:
    print("NO")




