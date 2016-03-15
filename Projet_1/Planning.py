class Planing(object):
    def __init__(self, nameFile):
        self._n = None
        self._m = None
        self._deliveryTime = []
        self._time = []
        self._totalTime = 0
        self._temp_totalTime = 0
        self._parcours = []
        self._temp_parcours = []
        self._actions = []
        self._temp_actions = []
        self._count = 0
        self._temp_count = 0
        self._name = nameFile
        self._done = False
        self.read_file()
        self.solve(self.get_depart())
        print(self._parcours)
        print(self._totalTime)
        print(self._count)

    def read_file(self):
        temp_data = []
        i = 0
        with open(self._name, 'r') as f:
            read_data = f.read()
        f.closed
        for data in read_data.split("\n"):
            temp_data.append(data)
        self.handle_data(temp_data)

    def handle_data(self, temp_data):
        self._n = int(temp_data[0])
        self._m = int(temp_data[1])
        for del_time in temp_data[2].split(" "):
            self._deliveryTime.append(int(del_time))
        for i in range(self._m):
            temp_time = []
            for time in temp_data[3+i].split(" "):
                temp_time.append(int(time))
            self._time.append(temp_time)

    def get_time_between(self, i, j):
        time = self._time[i][j]
        if time == -1:
            return None
        else:
            return time

    def get_depot_for(self, client):
        if client + self._n <= self._m:
            return client + self._n
        else:
            return None

    def get_client_for(self, depot):
        if depot - self._n >= 0:
            return depot - self._n
        else:
            return None

    def calculate_hour(self, minutes):
        left = minutes % 60
        min = minutes - left
        if left < 10:
            left = "0" + str(left)
        return str(int(8 + (min/60))) + ":" + str(left)

    def get_depart(self):
        return 2 * self._n

    def add_transfert_time(self, total_time):
        total_time += 5
        return total_time

    def save_solution(self, total_time, parcours):
        self._totalTime = total_time
        self._parcours = self.copy_array(parcours)

    def possible(self, i, j):
        return (i >= 0 and i <= self._m and j >= 0 and j <= self._m)

    def compare_results(self, total_time, parcours):
        if(self._totalTime == 0 or total_time < self._totalTime):
            self.save_solution(total_time, parcours)

    def is_all_delivered(self, parcours):
        temp = True
        for i in range(self._n):
            if i+self._n not in parcours:
                temp = False
        for i in range(self._n):
            if i not in parcours:
                temp = False
        return temp

    def add_time(self, total_time, dest_from, dest_to):
        time_to_add = self.get_time_between(dest_from, dest_to)
        total_time += time_to_add
        return total_time

    def already_pass(self, parcours, position, num):
        cpt = 0
        for pos in parcours:
            if position == pos:
                cpt += 1
        return cpt >= num

    def is_client(self, position):
        return position in [i for i in range(self._n)]

    def is_depot(self, position):
        return position in [self._n + i for i in range(self._n)]

    def can_go(self, parcours, total_time, dest_from, dest_to):
        if self.already_pass(parcours, dest_to, 2):
            return False
        if self.time_expired(total_time, dest_to, self.get_time_between(dest_from, dest_to)):
            return False
        if self.is_client(dest_to):
            if self.can_go_to_client(dest_from, dest_to):
                return True
            else:
                return False
        return True

    def can_go_to_client(self, dest_from, dest_to):
        if(len(self._temp_parcours) == 0):
            return False
        depot_target = self.get_depot_for_client(dest_to)
        last_depot_visited = None
        for elm in self._temp_parcours:
            if self.is_depot(elm):
                if not self.depot_already_delivered(elm):
                    last_depot_visited = elm
        if last_depot_visited == depot_target:
            return True
        else:
            return False

    def copy_array(self, array_from):
        temp = []
        for elm in array_from:
            temp.append(elm)

        return temp

    def depot_already_delivered(self, depot):
        client = depot - self._n
        if client in self._temp_parcours:
            return True
        return False

    def get_depot_for_client(self, client):
        return self._n + client

    def get_time_expected(self, position):
        if position in [i for i in range(self._n)]:
            return self._deliveryTime[position]
        else:
            return None

    def time_expired(self, total_time, position, time_to_add):
        time_expected = self.get_time_expected(position)
        if time_expected == None:
            return False
        return time_expected < total_time + time_to_add

    def printRes(self):
        pass

    def solve(self, position):
        self._count += 1
        if(self.is_client(position) or self.is_depot(position)):
            self._temp_totalTime = self.add_transfert_time(self._temp_totalTime)
        if(len(self._temp_parcours) == 0):
            self._temp_parcours.append(position)
        if self.is_all_delivered(self._temp_parcours):
            if self._temp_totalTime == 56:
                    print("coucou")
            self.compare_results(self._temp_totalTime, self._temp_parcours)
            return True
        possibles = []
        for i in range(self._m):
            time = self.get_time_between(position, i)
            if(time != None and self.can_go(self._temp_parcours, 0, position, i)):
                possibles.append(i)
        for possible in possibles:
            self._temp_parcours.append(possible)
            self._temp_totalTime = self.add_time(self._temp_totalTime, position, possible)
            self.solve(possible)
            last_elm = self._temp_parcours[-1]
            time = self.get_time_between(position, last_elm)
            del self._temp_parcours[-1]
            self._temp_totalTime -= time
        return False
