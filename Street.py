
class Street:

    def __init__(self, id, time):
        self.__id = id
        self.__time_to_cross = time
        self.__cars = []

    @property
    def id(self):
        return self.__id

    @property
    def time_to_cross(self):
        return self.__time_to_cross

    @property
    def cars(self):
        return self.__cars

    def initial_add_car(self, car):
        self.__cars.append(car)

    def remove_car(self, car):
        # we do not check here the semaphore light nor the time.
        # the car must be at the end of the street.
        if car.time_taken_to_cover_a_street >= self.time_to_cross:
            return car
        return None
    
    def move_car_from_street_to_street(self, car):
        self.cars.remove(car)

    def remove_car_at_goal(self, car):
        if car.car_achieved_goal(car, self.time_to_cross):
            # the car has reached the goal, it can be deleted.
            self.cars.remove(car)

    def add_car(self, car):
        # update car values such as current street, path and time to cover.
        # after that queue up into the car list.

        # delete the old street from the path.
        car.update_path_covered()
        # update the street name
        car.current_street = car.get_the_next_street()
        if car.current_street == self.id:
            self.initial_add_car(car)

    def __str__(self):
        msg = "Street name:" + str(self.id) + "\nHas the following cars on it: "
        for c in self.cars:
            msg += str(c) + " | "
        return msg
