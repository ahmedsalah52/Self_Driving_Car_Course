#task 1
import math




user_input = 0
max_num = -math.inf
min_num = math.inf
while(1):
    try: 
        user_input = input("Enter a number : ")
        if user_input == 'done':
            break
        user_input = int(user_input)
        if user_input > max_num:
            max_num = user_input
        elif user_input < min_num:
            min_num = user_input
        else:
            pass
    except:
        print("invalid input")

print("max = ", max_num)
print("min = ", min_num)

