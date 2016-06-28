w, h = 10, 5
table = [[5 for x in range(w)] for y in range(h)]

for i in range(w):
    table[0][i] = 0

for j in range(h):
    table[j][0] = 1

print(table)