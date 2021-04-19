my_file = open("mbox-short.txt",'r')
counter = 0
text = my_file.read()
for line in text.splitlines():
    try:
        #print (line.split())
        if line.split()[0] == 'From':
            print(line.split()[1])
            counter+=1
    except:
        pass
print(counter)