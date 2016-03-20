# coding: utf8
import itertools

class Planing(object):
    def __init__(self, nameFile):
        self.n = None
        self.m = None
        self.deliveryTime = []
        self.time = []
        self.totalTime = 0
        self.parcours = []
        self.count = 0
        self.actions = []

        self._limit = 1000000

        self._temp_totalTime = 0
        self._temp_parcours = []
        self._temp_actions = []
        self._temp_count = 0

        self._load_possibilities = []

        self._depot_loaded = {}

        self._name = nameFile
        self._success = False

        self.read_file()
        self.generate_load_or_not()
        self.solve(self.get_depart())
        self.printRes()

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
        self.n = int(str(temp_data[0]))
        self.m = int(str(temp_data[1]))
        for del_time in temp_data[2].split(" "):
            self.deliveryTime.append(int(str(del_time)))
        for i in range(self.m):
            temp_time = []
            for time in temp_data[3+i].split(" "):
                temp_time.append(int(str(time)))
            self.time.append(temp_time)

    def get_time_between(self, i, j):
        time = self.time[i][j]
        if time == -1:
            return None
        else:
            return time

    def get_depot_for(self, client):
        if client + self.n <= self.m:
            return client + self.n
        else:
            return None

    def get_client_for(self, depot):
        if depot - self.n >= 0:
            return depot - self.n
        else:
            return None

    def calculate_hour(self, minutes):
        left = minutes % 60
        min = minutes - left
        if left < 10:
            left = "0" + str(left)
        return str(int(8 + (min/60))) + ":" + str(left)

    def get_depart(self):
        return 2 * self.n

    def add_transfert_time(self):
        self._temp_totalTime += 5

    def save_solution(self, total_time, parcours):
        self.totalTime = total_time
        self.parcours = self.copy_array(parcours)
        self.actions = self.copy_array(self._temp_actions)

    def possible(self, i, j):
        return (i >= 0 and i <= self.m and j >= 0 and j <= self.m)

    def compare_results(self, total_time, parcours, strategy):
        if(self.totalTime == 0 or total_time < self.totalTime):
            self.save_solution(total_time, parcours)

    def is_all_delivered(self, parcours):
        temp = True
        for i in range(self.n):
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
        return position in [i for i in range(self.n)]

    def is_depot(self, position):
        return position in [self.n + i for i in range(self.n)]

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
        if self.client_already_delivered(self.get_depot_for(dest_to), self._temp_parcours):
            return True
        depot_target = self.get_depot_for(dest_to)
        return self.get_last_loaded() == depot_target

    def get_last_loaded(self):
        max = None
        depot = None
        for key in self._depot_loaded.keys():
            if max == None or max < self._depot_loaded[key][1]:
                if not self._depot_loaded[key][2]:
                    max = self._depot_loaded[key][1]
                    depot = key

        return depot

    def is_loaded(self, position):
        value = None
        try:
            value = self._depot_loaded[position]
        except:
            pass
        return value != None #Si il est dans la liste, c'est qu'il a été loadé

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
        if position in [i for i in range(self.n)]:
            return self.deliveryTime[position]
        else:
            return None

    def time_expired(self, total_time, dest_from, dest_to, time_to_add):
        if self.is_client(dest_to):
            if not self.client_already_delivered(self.get_depot_for(dest_to), self._temp_parcours):
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
            return False
        if value == None:
            return False
        else:
            return value[2]

    def printRes(self):
        if self.totalTime == 0:
            print("Trajet impossible dans le temps imparti")
        else:
            for line in self.actions:
                print(line)
            print("Temps total : {}".format(self.totalTime))
            print("Nombre d'itérations : {}".format(self.count))

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
            if self.client_already_delivered(depot, self._temp_parcours):
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
        self.count +=1
        #Si premiere itération, on ajoute la position dans le parcours
        if(len(self._temp_parcours) == 0):
            self._temp_parcours.append(position)
            self.add_action(self._temp_parcours, position, position)

            for strategy in self._load_possibilities:
                    if self.solve(position, strategy):
                        self._success = True

        #Si tous les clients ont été livré, on compare les résultats
        if self.is_all_delivered(self._temp_parcours):
            self.compare_results(self._temp_totalTime, self._temp_parcours, strategy)
            return True

        #On détermine les chemins possible
        possibles = []
        for i in range(self.m):
            time = self.get_time_between(position, i)
            if(time != None and self.can_go(self._temp_parcours, self._temp_totalTime, position, i)):
                possibles.append(i)

        #Tous les chemins possible sont déterminé, on les teste)
        for possible in possibles:
            self._temp_parcours.append(possible)
            should_load = self.should_load(self._temp_parcours, possible, strategy)
            time = self._temp_totalTime
            self.add_action(self._temp_parcours, position, possible, should_load)
            if should_load:
                #On ajoute le numero du dépot et son totalTime associé avant chargement et avant meme d'avoir été dessus
                self._depot_loaded[possible] = [time, self._temp_totalTime, False]
            if self.enough_time_remaining() and not self.time_passed_better() and not self.iteration_limit():
                if self.solve(possible, strategy):
                    self._success = True
            self.remove_last_position()

        return self._success

    def iteration_limit(self):
        return self.count >= self._limit

    def time_passed_better(self):
        if self.totalTime != 0:
            return self._temp_totalTime > self.totalTime
        else:
            return False


    def enough_time_remaining(self):
        clients = self.clients_remaining()
        depots = self.depots_remaining()
        total = clients + depots
        if total == 0:
            return True
        time = (total * 5) + total - 1

        flag = False
        cpt = 0
        for delivery in self.deliveryTime:
            if not self.client_already_delivered((cpt + self.n), self._temp_parcours):
                if delivery >= self._temp_totalTime + time:
                    flag = True
            cpt += 1

        return flag

    def clients_remaining(self):
        cpt = 0
        cpt += self.n - len(self._depot_loaded)
        if cpt != self.n:
            for key in self._depot_loaded.keys():
                if self._depot_loaded[key][2] == False:
                    cpt += 1

        return cpt

    def depots_remaining(self):
        return self.n - len(self._depot_loaded)

    def remove_last_position(self):
        last_position = self._temp_parcours[-1]
        dest_from = self._temp_parcours[-2]
        time = self.get_time_between(dest_from, last_position)
        if self.is_depot(last_position):
            try:
                time_loaded = self._depot_loaded[last_position]
                if self._temp_totalTime == time_loaded[1]:
                    self.remove_time(time + 5)
                    del self._depot_loaded[last_position]
                else:
                    self.remove_time(time)
            except:
                self.remove_time(time)
        elif self.is_client(last_position):
            depot = self.get_depot_for(last_position)
            try:
                delivered = self._depot_loaded[depot][2]
                if delivered:
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
            except:
                self.remove_time(time)

        else:
            self.remove_time(time)

        del self._temp_parcours[-1]
        self.remove_last_action()

    def remove_time(self, time):
        self._temp_totalTime -= time

    def generate_load_or_not(self):
        temp = [list(i) for i in itertools.product([0, 1], repeat=self.n)]
        for elm in temp:
            count = elm.count(0)
            if count <= 1:
                self._load_possibilities.append(elm)

    def should_load(self, parcours, position, strategy):
        if self.is_depot(position):
            indice = position - self.n
            if strategy[indice] == 0:
                #Si on ne charge pas au premier passage
                return self.already_pass(parcours, position, 2)
            else:
                return not self.already_pass(parcours, position, 2)
        else:
            return False
