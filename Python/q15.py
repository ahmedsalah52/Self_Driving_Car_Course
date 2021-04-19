file_name = input("please enter the file name \n")

file = open(file_name,'r')
for word in file.read().split():
    print(word.upper())

file.close()