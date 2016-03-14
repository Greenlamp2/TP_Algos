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
        self._parcours = parcours

    def possible(self, i, j):
        return (i >= 0 and i <= self._m and j >= 0 and j <= self._m)

    def solve(self, position):
        self._done = False
        self._temp_count += 1

        total_time = 0
        parcours = []



        #Fin de la condition d'arret

        parcours.append(position)
        if self.is_depot(position) or self.is_client(position):
            total_time = self.add_transfert_time(total_time)
        for i in range(self._m):
            time = self.get_time_between(position, i)
            if(time != None and self.can_go(position, i)):
                total_time = self.add_time(total_time, position, i)
                parcours.append(i)
                a, b = self.solve(i)
                parcours.append(a)
                total_time += b
        #Condition d'arret de la fonction recursive avec un return True
        if self.is_all_delivered(parcours):
            #Checker les temps
            self.compare_results(total_time, parcours)

        return parcours, total_time

    def compare_results(self, total_time, parcours):
        if(self._totalTime == 0 or total_time < self._totalTime):
            self.save_solution(total_time, parcours)

    def is_all_delivered(self, parcours):
        temp = True
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

    def can_go(self, parcours, dest_from, dest_to):
        if self.already_pass(parcours, dest_to, 1):
            return False
        if self.time_expired(dest_to, self.get_time_between(dest_from, dest_to)):
            return False
        if self.is_depot(dest_from):
            if self.is_client(dest_to):
                if self._temp_parcours[-1] == dest_from:
                    return True

        return True

    def get_time_expected(self, position):
        if position in [i for i in range(self._n)]:
            return self._deliveryTime[position]
        else:
            return None

    def time_expired(self, position, time_to_add):
        time_expected = self.get_time_expected(position)
        if time_expected == None:
            return False
        return time_expected < self._temp_totalTime+ time_to_add

    def printRes(self):
        pass