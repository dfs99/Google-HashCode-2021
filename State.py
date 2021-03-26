from copy import deepcopy
import itertools
from math import ceil


class State:

    def __init__(self, time, streets, cars, intersections):
        # the time states the depth.
        self.__time = time
        self.__streets = deepcopy(streets)
        self.__cars = deepcopy(cars)
        self.__intersections = deepcopy(intersections)
        # Thus, a greedy best first search algorithm is going to be used. f(n) = h(n)
        self.__heuristic_value = 9999
        self.__current_light_semaphores = None

    @property
    def time(self):
        return self.__time

    @time.setter
    def time(self, new_time):
        self.__time = new_time

    @property
    def streets(self):
        return self.__streets

    @property
    def cars(self):
        return self.__cars

    @property
    def intersections(self):
        return self.__intersections

    @property
    def heuristic_value(self):
        return self.__heuristic_value

    def evaluate_state(self):
        # añadir como valor el máximo de calles que le falten a un coche sobre todos los coches totales en el mapa.
        # por tanto es admisible ya que no sobreestimamos.
        max_number_of_streets = 0
        for s in self.streets:
            for c in s.cars:
                max_number_of_streets += len(c.path_covered)
        self.__heuristic_value = (ceil(max_number_of_streets/len(self.cars)))


    def get_successors(self):
        children = []
        all_light_schedules = []
        for intersection in self.intersections:
            all_light_schedules.append(intersection.bool_light_schedule)

        # each set is a possible alternative.
        all_alternatives = semaphore_lights_for_all_intersections(all_light_schedules)

        # each alternative stores an option for every semaphore in the city plan.
        for alternative in all_alternatives:
            # for each alternative there will be a child.
            current_child = deepcopy(self)
            # free all the cars.
            for s in current_child.streets:
                for c in s.cars:
                    if c.already_moved is True:
                        c.already_moved = False
            # update the semaphores in the city plan.
            current_child.__current_light_semaphores = alternative
            # loop over every intersection to update the new semaphores' values.
            # for intersection in current_child.intersections:
            for i in range(0, len(current_child.intersections)):
                # the intersections are in order.
                # update the intersection schedule for each one.
                current_child.intersections[i].current_light_schedule = alternative[i]

                # perform all the updates within streets and cars if the street has a green semaphore.
                for j in range(0, len(current_child.intersections[i].street_in)):
                    # if it contains a 1 the semaphore is green
                    if current_child.intersections[i].current_light_schedule[j] == 1:
                        # the semaphore has been activated. Thus perform updates.
                        # get the instance of the current street. In street_in only the id is stored.
                        current_street_id = current_child.intersections[i].street_in[j]
                        street = current_child.get_street(current_street_id)
                        # We do have now access to the street.
                        # only one car can be removed.
                        #one_car_only = False
                        for car in street.cars:
                            # update for each car the time in the current street.
                            car.update_time_taken_to_cover_a_street()
                            if car.already_moved is False:
                                car.already_moved = True
                                removed_car = street.remove_car(car)
                                if removed_car is not None:
                                    #one_car_only = True
                                    # remove the car from the current street which has been already visited.
                                    street.move_car_from_street_to_street(removed_car)
                                    # update the car's values.
                                    removed_car.update_path_covered()
                                    # move the car to the next street. Update the current street.
                                    removed_car.current_street = removed_car.get_the_next_street()
                                    removed_car.time_taken_to_cover_a_street = 0
                                    for j_street in current_child.streets:
                                        # append the car in its new street.
                                        if j_street.id == removed_car.current_street:
                                            j_street.initial_add_car(removed_car)
            # add the child.
            current_child.time = current_child.time - 1
            # evaluate the child.
            current_child.evaluate_state()
            children.append(current_child)

        return children

    def __eq__(self, other):
        if isinstance(other, State):
            if self.time == other.time and self.cars == other.cars and self.intersections == other.__intersections and \
                    self.streets == other.streets:
                return True
            return False
        else:
            return False
        
    def __hash__(self):
        return id(self)

    def end_state(self):
        if self.time == 0:
            # check that all cars have reached the goal
            #goal_state = True
            #for c in self.cars:
            #    if len(c.path_covered) != 0:
             #       goal_state = False

            #return goal_state
            return True
        else:
            return False

    def get_street(self, street_id):
        for street in self.streets:
            if street.id == street_id:
                return street
        return None

    def __str__(self):
        msg = "TIME:\t " + str(self.time) + "\n"
        msg += "Intersection schedule:\t" + str(self.__current_light_semaphores) + "\n"
        for s in self.streets:
            msg += str(s) + "\n"
        msg += "heuristic value = " + str(self.__heuristic_value) + "\n"
        return msg


# OPERATORS
def semaphore_lights_for_all_intersections(all_possible_schedules):
    # se devuelven todas las posibles alternativas de encendido de semáforos.
    return itertools.product(*all_possible_schedules)
