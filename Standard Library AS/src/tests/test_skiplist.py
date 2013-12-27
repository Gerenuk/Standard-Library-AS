from skiplist import SkipListDict

s = SkipListDict()
for i in range(20):
    s[i] = i
print(tuple(s.items(start_key=5)))
