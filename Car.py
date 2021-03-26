from copy import deepcopy


class Car:

    def __init__(self, path: list):
        # path: sequence of streets is going trough
        # the car starts at the end of the street, thus at the intersection's beginning
        self.__path = deepcopy(path)
        self.__current_street = self.path[0]
        # it will start with the whole path and the streets will be deleted on demand.
        self.__path_covered = deepcopy(path)
        # if the street needs 2 secs, the car must update this value up to 2 sec, then it
        # will be queued up waiting to move forward.
        self.__time_taken_to_cover_a_street = 0
        # when the car reaches the goal, it can be deleted.
        self.__already_moved = False

    @property
    def already_moved(self):
        return self.__already_moved

    @already_moved.setter
    def already_moved(self, new_value):
        self.__already_moved = new_value

    @property
    def time_taken_to_cover_a_street(self):
        return self.__time_taken_to_cover_a_street

    @time_taken_to_cover_a_street.setter
    def time_taken_to_cover_a_street(self, new_time):
        self.__time_taken_to_cover_a_street = new_time

    def update_time_taken_to_cover_a_street(self):
        # add the time for every round.
        self.__time_taken_to_cover_a_street += 1

    @property
    def path(self):
        return self.__path

    @property
    def path_covered(self):
        return self.__path_covered

    @property
    def current_street(self):
        return self.__current_street

    @current_street.setter
    def current_street(self, new_street):
        self.__current_street = new_street

    def car_achieved_goal(self, street_time):
        return True if (len(self.path_covered) == 0 and self.time_taken_to_cover_a_street == street_time) else False

    def update_path_covered(self):
        # delete the street from the path covered.
        if self.current_street in self.path_covered:
            self.path_covered.remove(self.current_street)

    def get_the_next_street(self):
        if len(self.path_covered) > 0:
            return self.path_covered[0]
        return None

    def __str__(self):
        msg = "Car with path: " + str(len(self.path)) + " It has gone through: " + str(len(self.path_covered))
        return msg
