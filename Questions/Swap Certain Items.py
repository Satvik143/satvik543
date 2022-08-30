# This Is The Swap Function
def swap (n,m,l):
    c = l[n]
    d = l[m]
    l[n] = d
    l[m] = c

# This Will Ask How Many Items Do You Want To Add To Your List
v = 1
c = int(input("Enter How Many Items To Add List To Swap : "))
l = []

# This Will Add Items To The List
while v <= c:
    l.append(input(f"Enter {v} Item : "))
    v += 1

j = 0
i = 0

# This Will Print The List
while j < len(l):
    print(l[j],end=" ")
    j += 1

print()

# This Will Convert The Str To A Index
n = (input("Swap : "))
i1 = l.index(n,0,len(l))
m = (input("With : "))
i2 = l.index(m,0,len(l))

# This Will Call The Swap Function
swap(i1,i2,l)

j = 0

# This Will Print The Swapped Result
while j < len(l):
    print(l[j],end=" ")
    j += 1