# coding: utf8
import itertools

class Planning(object):
    """
    Constructeur
    Paramètre:
        nameFile: Nom du fichier contenant les données à traiter.

    attributs:
        - n: Le nombre de client
        - m: Le nombre total de carrefour, client et dépots
        - deliveryTime: le temps limite de livraison des clients
        - time: les temps d'accès entres les différents carrefour/clients/depots
        - totalTime: le temps total du trajet optimal
        - parcours: les numéros des lieux visités du trajet optimal
        - count: le nombre total d’appel à la méthode solve()
        - actions: contient pour chaque entrée de parcours les informations
                   des actions effectuées à ce lieu
        - _limit: le nombre limite d'itération pour les gros fichier data (comme data6)
        - _temp_totalTime: variable temporaire contenant le temps du trajet testé
        - _temp_parcours: variable temporaire contenant le parcours du trajet testé
        - _temp_actions: variable temporaire contenant les actions du trajet testé
        - _load_possibilities: les différentes stratégies de passage dans les dépots
                               si il doit charger ou pas le camion pour le test en cours
        - _depot_loaded: variable contenant des informations lorsque le camion est chargé.
                         notemment l'heure de chargement ainsi que si la cargaison a été livrée.
        - _name: le nom du fichier de donnée
        - _success: si l'algorithme a trouvé une solution
    """
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

        self._load_possibilities = []

        self._depot_loaded = {}

        self._name = nameFile
        self._success = False

        #On parcourt le fichier pour récupérer les données, si le fichier est incorrect,
        #Le programme s'arrete avec un message d'erreur
        if self.read_file():
            #On génère les stratégies de chargement dans les dépots
            self.generate_load_or_not()
            #On apelle la méthode solve qui est récursive et qui va générer le résultat
            self.solve(self.get_depart())
            #On affiche les actions du trajet optimal
            self.printRes()

    """
    read_file
    Description:
        Permet de lire le fichier data et d'y extraire les informations dans un tableau qui nous servira
        à placer les bonnes valeurs dans les bonnes variable.
    paramètre:
    """
    def read_file(self):
        #Initialisation du tableau
        temp_data = []
        i = 0
        #On met le contenu du fichier dans une variable
        with open(self._name, 'r') as f:
            read_data = f.read()
        f.closed
        #On parcourt cette variable pour inclure chaques lignes dans le tableau
        for data in read_data.split("\n"):
            temp_data.append(data)
        #On apelle la méthode qui va remplir les variables avec les bonnes données
        return self.handle_data(temp_data)

    def handle_data(self, temp_data):
        try:
            #Les 2 premieres lignes contienne n et m
            self.n = int(temp_data[0])
            self.m = int(temp_data[1])

            #La 3e ligne, les delivery time séparé par un espace
            for del_time in temp_data[2].split(" "):
                self.deliveryTime.append(int(del_time))

            #Puis on parcours les m lignes restantes qui contiennent les temps entre les carrefours/clients/depot
            for i in range(self.m):
                temp_time = []
                #On sait qu'on a toutes les informations sur la lignes séparé par un espace
                for time in temp_data[3+i].split(" "):
                    temp_time.append(int(time))
                self.time.append(temp_time)
            return True
        except:
            #SI une erreur est survenue, c'est que le fichier data ne respecte pas la sémantique
            print("Erreur dans votre fichier data, veuillez le vérifier")
            return False

    """
    get_time_between
    Description:
        Retourne le temps entre 2 carrefours/clients/depots, et retourne None si ils ne sont pas reliés
    paramètre:
        - i: le point de départ
        - j: le point d'arrivée
    """
    def get_time_between(self, i, j):
        time = self.time[i][j]
        if time == -1:
            return None
        else:
            return time

    """
    get_depot_for
    Description:
        Retourne le numéro du dépot associé à un client
    paramètre:
        - client: le client dont on veut savoir son numéro de dépot
    """
    def get_depot_for(self, client):
        if client + self.n <= self.m:
            return client + self.n
        else:
            return None

    """
    get_client_for
    Description:
        Retourne le numéro du client associé à un dépot
    paramètre:
        - depot: le depot dont on veut savoir son numéro de client
    """
    def get_client_for(self, depot):
        if depot - self.n >= 0:
            return depot - self.n
        else:
            return None

    """
    calculate_hour
    Description:
        Retourne un string contenant l'heure calculé à partir de 8h et dont on a jouter les minutes,
        affichera l'heure correctement, par exemple: 9h30
    paramètre:
        - minutes: le nombre de minutes à ajouter à 8h
    """
    def calculate_hour(self, minutes):
        left = minutes % 60
        min = minutes - left
        #Si le nombre de minute restante est inférieur à 10, on ajoutera un petit 0 à gauche
        if left < 10:
            left = "0" + str(left)
        return str(int(8 + (min/60))) + "h" + str(left)

    """
    get_depart
    Description:
        Retourne le carrefour de départ
    paramètre:
    """
    def get_depart(self):
        return 2 * self.n

    """
    add_transfert_time
    Description:
        Ajoute 5 minutes au temps total, utilisé lorsqu'on charge ou décharge.
    paramètre:
    """
    def add_transfert_time(self):
        self._temp_totalTime += 5

    """
    save_solution
    Description:
        Ecrase les actions, temps et parcours précédent pour les remplacer par une meilleure solution
    paramètre:
        - total_time: le nouveau temp total optimal
        - parcours: le nouveau parcours optimal
    """
    def save_solution(self, total_time, parcours):
        self.totalTime = total_time
        self.parcours = self.copy_array(parcours)
        self.actions = self.copy_array(self._temp_actions)

    """
    compare_results
    Description:
        Compare les résultats précédents avec les nouveaux, si meilleur, on les sauvegardera
    paramètre:
        - total_time: le nouveau temp total optimal
        - parcours: le nouveau parcours optimal
    """
    def compare_results(self, total_time, parcours):
        if(self.totalTime == 0 or total_time < self.totalTime):
            self.save_solution(total_time, parcours)

    """
    is_all_delivered
    Description:
        Vérifie si tous les clients ont été livré
    paramètre:
        - parcours: le parcours actuel
    """
    def is_all_delivered(self, parcours):
        temp = True
        for i in range(self.n):
            if i not in parcours:
                temp = False
        return temp

    """
    add_time
    Description:
        Ajoute le temp nécessaire pour passer entre 2 lieu dans le temp total
    paramètre:
        - dest_from: le lieu de départ
        - dest_to: le lieu d'arrivée
    """
    def add_time(self, dest_from, dest_to):
        if dest_from != dest_to:
            time_to_add = self.get_time_between(dest_from, dest_to)
            self._temp_totalTime += time_to_add

    """
    already_pass
    Description:
        Vérifie si on est déja passé un nombre num de fois dans un lieu
    paramètre:
        - parcours: Le parcours actuel
        - position: le lieu en question
        - num: le nombre de fois qu'on veut vérifier si il est passé
    """
    def already_pass(self, parcours, position, num):
        cpt = 0
        for pos in parcours:
            if position == pos:
                cpt += 1
        return cpt >= num

    """
    is_client
    Description:
        Permet de savoir si un lieu est un client
    paramètre:
        - position: le lieu en question
    """
    def is_client(self, position):
        return position in [i for i in range(self.n)]

    """
    is_depot
    Description:
        Permet de savoir si un lieu est un depot
    paramètre:
        - position: le lieu en question
    """
    def is_depot(self, position):
        return position in [self.n + i for i in range(self.n)]

    """
    can_go
    Description:
        Permet de savoir si un lieu peut en rejoindre un autre en vérifiant:
        - Si il n'a pas déja atteint le nombre limite de passage
        - Si le client est atteignable (c-à-d si il été chargé en dernier pour ce client)
        - Si le temp pour atteindre le client n'est pas dépassé avec le temps de chargement et de chemin
    paramètre:
        - parcours: le parcours actuel
        - total_time: le temp total actuel
        - dest_from: le lieu de départ
        - dest_to: le lieu d'arrivée
    """
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

    """
    can_go_to_client
    Description:
        Permet de savoir si le lieu peut atteindre le client en vérifiant:
        - Si le lieu a déja été livré
        - si le dernier chargement est le bon
    paramètre:
        - dest_from: le lieu départ
        - dest_to: le client
    """
    def can_go_to_client(self, dest_from, dest_to):
        if(len(self._temp_parcours) == 0):
            return False
        if self.client_already_delivered(self.get_depot_for(dest_to), self._temp_parcours):
            return True
        depot_target = self.get_depot_for(dest_to)
        return self.get_last_loaded() == depot_target

    """
    get_last_loaded
    Description:
        Retourne le dernier dépot à avoir été chargé dans le camion
    paramètre:
    """
    def get_last_loaded(self):
        max = None
        depot = None
        for key in self._depot_loaded.keys():
            if max == None or max < self._depot_loaded[key][1]:
                if not self._depot_loaded[key][2]:
                    max = self._depot_loaded[key][1]
                    depot = key

        return depot

    """
    is_loaded
    Description:
        Permet de savoir si le depot en question a déja été chargé ou pas
    paramètre:
        - position: le dépot en question
    """
    def is_loaded(self, position):
        value = None
        try:
            value = self._depot_loaded[position]
        except:
            pass
        return value != None #Si il est dans la liste, c'est qu'il a été loadé

    """
    copy_array
    Description:
        Méthode permettant de recopier un tableau dans un autre
    paramètre:
        - array_from: le tableau de départ
    """
    def copy_array(self, array_from):
        temp = []
        for elm in array_from:
            temp.append(elm)

        return temp

    """
    depot_already_delivered
    Description:
        Méthode permettant de vérifier si un dépot a déja déchargé sa marchandise chez son client
    paramètre:
        - depot: le dépot en question
        - parcours: le parcours actuel
    """
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

    """
    get_time_expected
    Description:
        Méthode permettant de récupérer le temp maximum pour un client pour être chargé
    paramètre:
        - position: le client en question
    """
    def get_time_expected(self, position):
        if position in [i for i in range(self.n)]:
            return self.deliveryTime[position]
        else:
            return None

    """
    time_expired
    Description:
        Méthode permettant de savoir si il est possible d'atteindre le client dans le temps imparti
        - Si apres chargement et le trajet, le temps est dépassé, retourne vrai
    paramètre:
        - total_time: le temp maximale actuel
        - dest_from: le lieu de départ
        - dest_to: le client
        - time_to_add: le temp a ajouter pour effectuer le trajet entre le lieu et le client
    """
    def time_expired(self, total_time, dest_from, dest_to, time_to_add):
        if self.is_client(dest_to):
            if not self.client_already_delivered(self.get_depot_for(dest_to), self._temp_parcours):
                time_to_add += 5
            time_expected = self.get_time_expected(dest_to)
            if time_expected == None:
                return False
            return time_expected >= total_time + time_to_add
        return False

    """
    client_already_delivered
    Description:
        Méthode permettant de savoir si un client a déja été livré
    paramètre:
        - position: le lieu en question
        - parcours: le parcours actuel
    """
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

    """
    printRes
    Description:
        Méthode permettant d'afficher les actions de la solution optimale
    paramètre:
    """
    def printRes(self):
        if self.totalTime == 0:
            print("Trajet impossible dans le temps imparti")
        else:
            for line in self.actions:
                print(line)
            print("Temps total : {}".format(self.totalTime))
            print("Nombre d'itérations : {}".format(self.count))

    """
    add_action
    Description:
        Méthode permettant de rajouter l'action effectué dans la liste des actions
        - Si c'est un dépot, vérifie si il doit être chargé ou pas
        - Si c'est un client, vérifie si il n'a pas déja été livré
    paramètre:
        - parcours: le parcours actuel
        - dest_from: le lieu de départ
        - position: le lieu à atteindre
        - to_load: si il faut charger le camion ou pas
    """
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

    """
    remove_last_action
    Description:
        Méthode permettant de supprimer la derniere entrée dans la liste d'actions
    paramètre:
    """
    def remove_last_action(self):
        del self._temp_actions[-1]

    """
    solve
    Description:
        La méthode principale, solve, reprenant l'algorithme de résolution du projet
    paramètre:
        - position: Le lieu de départ
        - strategy: la stratégie de chargement du camion
    """
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
            self.compare_results(self._temp_totalTime, self._temp_parcours)
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

    """
    iteration_limit
    Description:
        Méthode permettant de savoir si on a dépassé ou non la limite d'itération
    paramètre:
    """
    def iteration_limit(self):
        return self.count >= self._limit

    """
    time_passed_better
    Description:
        Méthode permettant de savoir si on a dépassé ou non le temps optimal
    paramètre:
    """
    def time_passed_better(self):
        if self.totalTime != 0:
            return self._temp_totalTime > self.totalTime
        else:
            return False

    """
    time_passed_better
    Description:
        Méthode permettant de savoir si on a assez de temps pour atteindre les dépots et clients restant
        en supposant que tous les chemins soient à 1.
        Si il reste 2 client et 1 dépots à atteindre, ça fera minimum 15 minutes de chargement,
        et supposons qu'on soit à 1 lieu du dépot et que les 2 clients se suivent,
        on peut assumer rajouter au minimum 3 minutes
        Et donc si aucuns des deliveryTime restant ne dépasse le le temp total actuel plus ces minutes
        supplémentaire, on peut dire que c'est une solution érronée et arreter là cette itération.
    paramètre:
    """
    def enough_time_remaining(self):
        clients = self.clients_remaining()
        depots = self.depots_remaining()
        total = clients + depots
        if total == 0:
            return True
        time = (total * 5) + total

        flag = False
        cpt = 0
        for delivery in self.deliveryTime:
            if not self.client_already_delivered((cpt + self.n), self._temp_parcours):
                if delivery >= self._temp_totalTime + time:
                    flag = True
            cpt += 1

        return flag

    """
    clients_remaining
    Description:
        Retourne le nombre de client non livrés
    paramètre:
    """
    def clients_remaining(self):
        cpt = 0
        cpt += self.n - len(self._depot_loaded)
        if cpt != self.n:
            for key in self._depot_loaded.keys():
                if self._depot_loaded[key][2] == False:
                    cpt += 1

        return cpt

    """
    depots_remaining
    Description:
        Retourne le nombre de dépot non visité
    paramètre:
    """
    def depots_remaining(self):
        return self.n - len(self._depot_loaded)

    """
    remove_last_position
    Description:
        Supprime le dernier lieu visité dans parcours et soustrait la durée adéquate dans le temp total
        - Vérifie si c'est un dépot et qu'il y a eu chargement ou pas
        - Vérifie si c'est un client et qu'il y a eu livraison ou pas
        - Vérifie si c'est un client qui a déja été livré
        - Vérifie si c'est un dépot qui a déja été chargé
    paramètre:
    """
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

    """
    remove_time
    Description:
        Retire une durée dans le temp total actuel
    paramètre:
        - time: la durée à retirer
    """
    def remove_time(self, time):
        self._temp_totalTime -= time

    """
    generate_load_or_not
    Description:
        Génère les stratégies de chargement du camion en générant les différentes possibilité
        binaire en fonction de n:
        - [0, 0, 0]
        - [0, 0, 1]
        - [0, 1, 0]
        - [0, 1, 1]
        - etc.
        où 0 veut dire de ne pas charger le camion au premier passage et 1, dit qu'on le charge au premier passage
        ici, les indices du tableau correspondent au dépot
        [dépot 1, dépot 2, dépot 3]

        Par soucis d'optimisation, on a supprimé ceux dont on a plus qu'un 0 dans le tableau, en effet, on peut
        facilement observer que si on passe au minimum plus d'une fois dans les différents entrepots sans
        charger le camion la perte de temps est significative, donc dans l'exemple ci-dessus,
        les 2 premiers tableau sont exclus des stratégies.
    paramètre:
    """
    def generate_load_or_not(self):
        temp = [list(i) for i in itertools.product([0, 1], repeat=self.n)]
        for elm in temp:
            count = elm.count(0)
            if count <= 1:
                self._load_possibilities.append(elm)

    """
    should_load
    Description:
        Méthode permettant de savoir si le au passage actuel du camion dans le dépot, si il doit charger
        la marchandise ou non en fonction de la stratégie en cours.
        Si la stratégie est [1, 0, 1], que c'est notre premier passage dans le second dépot, alors comme c'est 0
        on lui dit de ne pas charger le camion cette fois-ci et d'attendre le second passage.
    paramètre:
    """
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
