

class car:
    def __init__(self):
        self.__distance = 0
        self.__time = 0
        self.__speed = 0

    def set_distance(self,distance):
        self.__distance = distance
    def set_time(self,time):
        self.__time = time

    def get_speed(self):
        self.__speed = self.__distance / self.__time
        return self.__speed

my_car = car()

my_car.set_distance(int(input("please enter the distance covered \n")))
my_car.set_time(int(input("please enter the time \n")))
print("speed = ",my_car.get_speed() , " km/h")
