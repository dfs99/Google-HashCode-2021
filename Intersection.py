

class Intersection:

    def __init__(self, id):
        # lists of streets coming in and coming out.
        self.__id = id
        self.__street_in = []
        self.__street_out = []
        self.__light_schedule = []
        self.__bool_light_schedule = []
        self.__current_light_schedule = []

    @property
    def id(self):
        return self.__id

    @property
    def street_in(self):
        return self.__street_in

    @property
    def street_out(self):
        return self.__street_out

    @property
    def light_schedule(self):
        return self.__light_schedule

    @property
    def bool_light_schedule(self):
        return self.__bool_light_schedule

    @property
    def current_light_schedule(self):
        return self.__current_light_schedule

    @current_light_schedule.setter
    def current_light_schedule(self, new_light_schedule):
        self.__current_light_schedule = new_light_schedule

    def set_light_schedule(self):
        # we could check whether the street is going to be used or not and prune all that stuff.
        for street in self.__street_in:
            self.__light_schedule.append((street, False))

        # contains a matrix with every possibility.
        for i in range(0, len(self.street_in)+1):
            self.__bool_light_schedule.append([])
            for j in range(0, len(self.street_in)):
                self.__bool_light_schedule[i].append(0)
                if i == j:
                    self.__bool_light_schedule[i][j] = 1

        # all the semaphores are initialized at 0
        for i in range(0, len(self.street_in)):
            self.__current_light_schedule.append(0)
    
    def set_streets_in(self, street):
        self.__street_in.append(street)

    def set_streets_out(self, street):
        self.__street_out.append(street)

    def __eq__(self, other):
        if isinstance(other, Intersection):
            return True if self.id == other.id else False

    def __str__(self):
        msg = " Intersection id:" + str(self.id) + " streets coming in: (end of the streets) " + \
              str(self.__street_in) + "\n streets coming out: (start of the streets) " + str(self.__street_out) + \
            "\n All the semaphores in the intersection: " + str(self.light_schedule)
        return msg
