#task 1


# age = int(input("Please enter your age \n"))
# print("You born at : " , 2021-age, " \n")


# year = int(input("Please enter the year of your birthday \n"))
# print("You are : " , 2021-year ," years old \n")


# num = int(input("Please enter any number\n"))
# total = 0
# for i in range(num+1):
#     total += i
# avg = total / num

# print("sum of nums =: ",total)
# print("avg of nums =: ",avg)

# num = int(input("Please enter any number to build a pyramid\n"))
# for i in range(num+1):
#     for j in range(num-i):
#         print(" ",end ="")
#     for k in range((i*2)-1):
#         print("*",end ="")
#     print("\n")


# num = int(input("Please enter any number \n"))
# print("even") if (num%2 == 0) else print("odd")

# line = input("please enter any string\n")
# for char in "aeiou":
#     line = line.replace(char,'')

# print(line)

# my_list = [1,2,3]
# file = open("/home/ahmed/Desktop/ITI workspace/Python/file",'w')
# file.write(str(my_list))
# file.close()


# my_list = [1,2,3,4]
# print(sum(my_list))

# def is_even_num(a_list):
#     even_list=[]
#     for num in a_list:
#         if (num %2) ==0:
#             even_list.append(num)
#     return even_list

# print(is_even_num([1,2,3,4,5,6,7,8,10,11,13,14]))


class my_class:
    def __init__(self):
        self.data = ""

    def set_string(self,user_input):
        if isinstance(user_input,str):
            self.data = user_input
        else:
            print("wrong input")

    def print_string(self):
        print(self.data)


test = my_class()

test.set_string("xyz")
test.print_string()