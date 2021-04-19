num = int(input("Please enter any number to build a pyramid\n"))
for i in range(num+1):
    for j in range(num-i):
        print(" ",end ="")
    for k in range((i*2)-1):
        print("*",end ="")
    print("\n")
