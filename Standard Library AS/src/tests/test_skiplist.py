from skiplist import *

# s = SkipListDictDefault(int)
s = SkipListDict(capacity=10)
# for i in range(0, 20, 5):
#     s[i] = i
# print(tuple(s.items(start_key=5)))
s[1] = 1
for i in range(100):
    s.setdefault(i, i)
print(s)
