from random import random

class SortedList:

    """
    Classe représentant une liste triee sous forme de skip list.
    Les noeuds utilises contiennent une liste Python de references
    vers d'autres endroits dans la skip list.
    """

    PROMOTION_THRESHOLD = 0.5

    def __init__(self):
        self.head = Node("H", None)

    def top_level(self):
        """
        Renvoie le niveau maximal dans la liste.
        Permet de savoir a quel niveau commencer la recherche.
        """
        return self.head.height() - 1

    def insert(self, value):
        """
        Insere un noeud dans la skip list en appliquant l'algorithme
        probabiliste de promotion.       
        """
        to_insert = Node(value, [None])   

        previous = self.previous_at_level(value)
        to_insert.set_next(previous.next())
        previous.set_next(to_insert)      

        level = 1
        while random() < SortedList.PROMOTION_THRESHOLD:
            to_insert.promote()
            if level > (self.top_level()):
                self.head.promote()
            previous = self.previous_at_level(value, level)
            to_insert.set_next(previous.next(level), level)
            previous.set_next(to_insert, level)
            level += 1
                 
    
    def remove(self, value):
        """
        Enleve un noeud de la skip list en le retirant successivement de chaque niveau.
        """
        node = self.search(value)
        if node is None:
            return False
        
        for level in range(node.height()):
            previous = self.previous_at_level(value, level)
            previous.set_next(node.next(level), level)
    
        del node
        return True
        

    def previous_at_level(self, value, level=0):
        """
        Retourne le noeud de la skip list dont la valeur est juste avant à la valeur demandée
        """
        #On positionne d'abord notre curseur en tête de liste
        current = self.head
        #On récupère la hauteur de la liste
        current_level = self.top_level()
        #On boucle tant que:
        # - On a pas dépassé le niveau demandé
        # - On a pas atteint le bout de liste
        # - La valeur vaut H
        # - La valeur est plus grande que celle demandée
        # Donc on boucle tant qu'on a pas trouvé le premier element plus grand que celle demandée
        # et lorsqu'on a trouvé cette valeur, on descend d'un niveau et on continue.
        while(current_level >= level and current != None and (current.get_value() == "H" or current.get_value() < value)):
            temp = current
            next = current.next(current_level)
            #Donc si on est en bout de liste à ce niveau là ou si la valeur est plus grande que celle demandée
            if(next == None or next.get_value() >= value):
                #On descend d'un niveau
                current_level -= 1
            else:
                #Sinon on récupère la valeur suivante au même niveau
                current = current.next(current_level)
        return temp

        
    def search(self, value):
        """
        Retourne le noeud de la skip list dont la valeur est la valeur recherchée
        """
        #On positionne d'abord notre curseur en tête de liste
        current = self.head
        #On récupère la hauteur de la liste
        current_level = self.top_level()
        #On initialise notre boolean servant à signifier qu'on a trouver notre valeur, à faux.
        found = False

        #On boucle tant que:
        # - On a pas trouvé notre valeur
        # - On a pas parcouru tous les niveaux de la liste
        # - On a pas atteint la fin de la liste
        # Donc on boucle tant qu'on a pas parcouru tous les niveaux et qu'on a pas trouvé notre élement.
        while(not found and current_level >= 0 and current != None):
            #Si la valeur actuelle est celle qu'on recherche
            if(current.get_value() == value):
                #On met la boolean à vrai
                found = True
            else:
                #Sinon on récupère l'element suivant sur le même niveau
                next = current.next(current_level)
                #Si l'element suivant n'existe pas ou si la valeur suivante est plus grande
                if(next == None or next.get_value() > value):
                    #On descend d'un niveau
                    current_level -= 1
                else:
                    #Sinon on récupère l'element suivant sur le même niveau
                    current = current.next(current_level)
        return current
        
        
    def __iter__(self):
        """
        Permet la conversion en liste Python grace a la fonction list().
        """
        current = self.head.next()
        while current is not None:
            yield current.get_value()
            current = current.next()


    def __str__(self):
        """
        Pretty print pour la liste. Utile pour debugger.
        """
        str_buffer = [str(i-1)+" " if i>0 else "  " for i in range(self.top_level() + 2)]
        current = self.head
        while current is not None:
            temp = "   " if len(str(current.get_value())) == 2 else "    "
            str_buffer[0] += str(current.get_value()) + temp
            for level in range(self.top_level()+1):
                if level < current.height():   
                    if current == self.head:
                        str_buffer[level+1] += "##"
                    else:             
                        str_buffer[level+1] += "-->##"
                else:
                    str_buffer[level+1] += "-----"
            current = current.next()
        return "-->\n".join(str_buffer[:0:-1])+"-->\n" + str_buffer[0]+"END"


class Node:
    """
    Classe noeud utilisee pour implementer une skip list.
    
    Attributs:
      - _value: contient une valeur arbitraire mais requiert une relation d'ordre
      - _next: liste Python contenant les references vers d'autres noeuds. L'indice
               dans la liste represente le niveau. Le noeud suivant de la skip list
               sur le niveau n est donne par self._next[n]
    """

    def __init__(self, value, next):
        """
        Initialise le noeud avec une valeur et un noeud suivant au niveau 0.
        """
        self._value = value
        self._next = [next]

    def next(self, level=0):
        """
        Renvoie l'element suivant sur le niveau passe en parametre (niveau le plus bas par defaut).
        """   
        return self._next[level]

    def set_next(self, new_next, level=0):
        """
        Permet de modifier la reference vers l'element suivant pour un niveau donne.
        """
        self._next[level] = new_next 

    def get_value(self):
        return self._value
       
    def promote(self):
        """
        Ajoute un niveau au noeud (utilise lors de l'insertion).
        """
        self._next.append(None)

    def height(self):
        """
        Renvoie le nombre de references du noeud.
        """
        return len(self._next)

    def __str__(self):
        res = "Node@" + str(id(self)) +"V" +str(self._value)+"\n"
        for n in self._next:
            res += str(id(n)) + "\n"
        return res


   
    
    
