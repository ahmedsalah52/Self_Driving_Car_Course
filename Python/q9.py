
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

test.set_string(input("please enter any string \n"))
test.print_string()


