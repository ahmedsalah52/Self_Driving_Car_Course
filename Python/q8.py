
def is_even_num(a_list):
    even_list=[]
    for num in a_list:
        if (num %2) ==0:
            even_list.append(num)
    return even_list

print(is_even_num([1,2,3,4,5,6,7,8,10,11,13,14]))
