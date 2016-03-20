import itertools

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
        self._load_possibilities = []
        self._depot_loaded = {}
        self._strategy_current = None
        self._name = nameFile
        self._success = False
        self.read_file()
        self.generate_load_or_not()
        self.solve(self.get_depart())
        self.printRes()
        print(self._totalTime)

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

    def add_transfert_time(self):
        self._temp_totalTime += 5

    def save_solution(self, total_time, parcours):
        self._totalTime = total_time
        self._parcours = self.copy_array(parcours)
        self._actions = self.copy_array(self._temp_actions)

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

    def add_time(self, dest_from, dest_to):
        if dest_from != dest_to:
            time_to_add = self.get_time_between(dest_from, dest_to)
            self._temp_totalTime += time_to_add

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
        if self.is_client(dest_to):
            if self.can_go_to_client(dest_from, dest_to):
                if self.time_expired(total_time, dest_from, dest_to, self.get_time_between(dest_from, dest_to)):
                    return True
                else:
                    return False
            else:
                return False
        return True

    def can_go_to_client(self, dest_from, dest_to):
        if(len(self._temp_parcours) == 0):
            return False
        depot_target = self.get_depot_for(dest_to)
        last_depot_visited = None
        visited = []
        for elm in self._temp_parcours:
            if self.is_depot(elm):
                if not elm in visited:
                    if not self.depot_already_delivered(elm, self._temp_parcours) and self.is_loaded(elm):
                        last_depot_visited = elm
                    visited.append(elm)
        if last_depot_visited == depot_target:
            return True
        else:
            return False

    def is_loaded(self, position):
        value = None
        try:
            value = self._depot_loaded[position]
        except:
            pass
        if value != None: #Si il est dans la liste, c'est qu'il a été loadé
            return True
        else:
            return False

    def copy_array(self, array_from):
        temp = []
        for elm in array_from:
            temp.append(elm)

        return temp

    def depot_already_delivered(self, depot, parcours):
        value = None
        try:
            value = self._depot_loaded[depot]
        except:
            pass
        if value == None:
            return False
        else:
            return value[2]

    def get_time_expected(self, position):
        if position in [i for i in range(self._n)]:
            return self._deliveryTime[position]
        else:
            return None

    def time_expired(self, total_time, dest_from, dest_to, time_to_add):
        if self.is_client(dest_to):
            if not self.client_already_delivered(dest_to, self._temp_parcours):
                time_to_add += 5
            time_expected = self.get_time_expected(dest_to)
            if time_expected == None:
                return False
            return time_expected >= total_time + time_to_add
        return False

    def client_already_delivered(self, position, parcours):
        value = None
        try:
            value = self._depot_loaded[position]
        except:
            pass
        if value == None:
            return False
        else:
            return value[2]

    def printRes(self):
        """
        time_total = 0
        prev = None
        depot = None
        temp_parcours = []
        for elm in self._parcours:
            if prev != None:
                time = self.get_time_between(prev, elm)
                time_total += time
                if self.is_depot(elm):
                    if not self.depot_already_loaded(elm, temp_parcours):
                        print("{} : {}, depot du client {}, chargement fini a {}".format(elm, self.calculate_hour(time_total), self.get_client_for(elm), self.calculate_hour(time_total+5)))
                        time_total += 5
                    else:
                        print("{} : {}, depot du client {}".format(elm, self.calculate_hour(time_total), self.get_client_for(elm)))
                elif self.is_client(elm):
                    print("{} : {}, client {}, dechargement fini a {}".format(elm, self.calculate_hour(time_total), elm, self.calculate_hour(time_total+5)))
                    time_total += 5
                else:
                    print("{} : {}, carrefour".format(elm, self.calculate_hour(time_total)))
            else:
                print("{} : {}, carrefour".format(elm, self.calculate_hour(time_total)))
            print("total_time: {}".format(time_total))
            prev = elm
            temp_parcours.append(elm)
        """
        for line in self._actions:
            print(line)
        print("Temps total : {}".format(self._totalTime))
        print("Nombre d'itérations : {}".format(self._count))

    def add_action(self, parcours, dest_from, position, to_load = False):
        action = ""
        if self.is_depot(position):
            client = self.get_client_for(position)
            if not to_load:
                #Si il a déja été chargé
                self.add_time(dest_from, position)
                hour = self.calculate_hour(self._temp_totalTime)
                action = "{} : {}, depot du client {}".format(position, hour, client)
            else:
                self.add_time(dest_from, position)
                hour_before = self.calculate_hour(self._temp_totalTime)
                self.add_transfert_time()
                hour_after = self.calculate_hour(self._temp_totalTime)
                action = "{} : {}, depot du client {}, chargement fini a {}".format(position, hour_before, client, hour_after)

        elif self.is_client(position):
            depot = self.get_depot_for(position)
            if self.client_already_delivered(position, self._temp_parcours):
                #Si client déja livré, on passe dessus sans déchargement
                self.add_time(dest_from, position)
                hour = self.calculate_hour(self._temp_totalTime)
                action = "{} : {}, client {}".format(position, hour, position)
            else:
                #Sinon, on décharge
                self.add_time(dest_from, position)
                hour_before = self.calculate_hour(self._temp_totalTime)
                self.add_transfert_time()
                hour_after = self.calculate_hour(self._temp_totalTime)
                action = "{} : {}, client {}, dechargement fini a {}".format(position, hour_before, position, hour_after)
                depot = self.get_depot_for(position)
                self._depot_loaded[depot][2] = True

        else:
            self.add_time(dest_from, position)
            hour = self.calculate_hour(self._temp_totalTime)
            action = "{} : {}, carrefour".format(position, hour)

        self._temp_actions.append(action)

    def remove_last_action(self):
        del self._temp_actions[-1]


    def solve(self, position, strategy=None):
        self._count +=1
        #Si premiere itération, on ajoute la position dans le parcours
        if(len(self._temp_parcours) == 0):
            self._temp_parcours.append(position)
            self.add_action(self._temp_parcours, position, position)

        if self._temp_parcours == [6, 8, 4, 5, 4, 5, 2, 3]:
            print(strategy)

        if strategy == [1, 1, 0]:
            print("")

        #Si tous les clients ont été livré, on compare les résultats
        if self.is_all_delivered(self._temp_parcours):
            self.compare_results(self._temp_totalTime, self._temp_parcours)
            return True

        #On détermine les chemins possible
        possibles = []
        for i in range(self._m):
            time = self.get_time_between(position, i)
            if(time != None and self.can_go(self._temp_parcours, self._temp_totalTime, position, i)):
                possibles.append(i)

        #Tous les chemins possible sont déterminé, on les teste)


        for possible in possibles:
            should_load = self.should_load(self._temp_parcours, possible, strategy)
            self._temp_parcours.append(possible)
            time = self._temp_totalTime
            self.add_action(self._temp_parcours, position, possible, should_load)
            if should_load:
                #On ajoute le numero du dépot et son totalTime associé avant chargement et avant meme d'avoir été dessus
                self._depot_loaded[possible] = [time, self._temp_totalTime, False]
            if self.is_depot(possible):
                for strategy in self._load_possibilities:
                    print("{}: {}".format(strategy, self._temp_parcours))
                    self.remove_last_position()
                    if self.solve(possible, strategy):
                        self._success = True
            else:
                print("{}: {}".format(strategy, self._temp_parcours))
                if self.solve(possible, None):
                    self._success = True
                self.remove_last_position()


        return self._success

    def remove_last_position(self):
        last_position = self._temp_parcours[-1]
        dest_from = self._temp_parcours[-2]
        time = self.get_time_between(dest_from, last_position)
        if self.is_depot(last_position):
            try:
                time_loaded = self._depot_loaded[last_position]
                if self._temp_totalTime == time_loaded[1]:
                    estimated = self._temp_totalTime - time
                    if time_loaded[0] != estimated:
                        self.remove_time(time + 5)
                        self._depot_loaded[last_position][2] = False
                    else:
                        self.remove_time(time)
            except:
                self.remove_time(time)
            else:
                self.remove_time(time)
        elif self.is_client(last_position):
            cpt = 0
            for elm in self._temp_parcours:
                if elm == last_position:
                    cpt += 1
            if cpt == 1:
                self.remove_time(time + 5)
                depot = self.get_depot_for(last_position)
                self._depot_loaded[depot][2] = False
            else:
                self.remove_time(time)
        else:
            self.remove_time(time)




        del self._temp_parcours[-1]
        #self.remove_time(time)
        self.remove_last_action()

    def remove_time(self, time):
        self._temp_totalTime -= time

    """
    def solve_(self, position):
        if self._temp_parcours == [6, 8, 5, 4, 5, 1, 3]:
            print("")
            #Il faut mtn faire si le camion charge, et si le camion charge pas.
        self._count += 1
        if(len(self._temp_parcours) == 0):
            self._temp_parcours.append(position)
        if self.is_all_delivered(self._temp_parcours):
            self.compare_results(self._temp_totalTime, self._temp_parcours)
            return True
        possibles = []
        for i in range(self._m):
            time = self.get_time_between(position, i)
            if(time != None and self.can_go(self._temp_parcours, self._temp_totalTime, position, i)):
                possibles.append(i)
        for possible in possibles:
            self._temp_parcours.append(possible)
            self._temp_totalTime = self.calculate_time_total(self._temp_parcours)
            self.solve(possible)
            del self._temp_parcours[-1]
            self._temp_totalTime = self.calculate_time_total(self._temp_parcours)
        return False
    """

    def generate_load_or_not(self):
        self._load_possibilities = [list(i) for i in itertools.product([0, 1], repeat=self._n)]

    def should_load(self, parcours, position, strategy):
        if strategy == None:
            return False
        if self.is_depot(position):
            if parcours == [6, 8, 4, 5, 4, 5, 2, 3, 1]:
                print(strategy)
            indice = position - self._n
            if strategy[indice] == 0:
                #Si on ne charge pas au premier passage
                return position in parcours
            else:
                return not position in parcours
        else:
            return False





