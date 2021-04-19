
num = int(input("Please enter any number\n"))
total = 0
for i in range(num+1):
    total += i
avg = total / num

print("sum of nums =: ",total)
print("avg of nums =: ",avg)