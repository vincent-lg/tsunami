# -*-coding:Utf-8 -*

# Copyright (c) 2010 LE GOFF Vincent
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# * Neither the name of the copyright holder nor the names of its contributors
#   may be used to endorse or promote products derived from this software
#   without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""Ce fichier contient la classe Quetes, détaillée plus bas."""

from collections import OrderedDict

from abstraits.obase import *
from .quete import Quete

class Quetes(BaseObj):
    
    """Conteneur de quêtes d'un personnage.
    
    Ce conteneur représente l'avancement d'un personnage dans les quêtes
    de l'univers. Il se présente sous la forme d'un dictionnaire :
    * En clé, le nom des quêtes
    * En valeur, les objets quete associés
    
    On doit utiliser les méthodes de manipulation de ce conteneur pour modifier
    ou consulter la valeur des quêtes d'un joueur. Ainsi, l'objet Quete
    lui-même, conçu pour conserver le niveau d'un personnage dans une quête, ne
    doit pas être manipulable directement sauf pour des opérations de lecture
    ou de consultation. Par exemple, pour savoir si un joueur a le droit
    de faire une quête.
    
    Méthodes disponibles :
        __getitem__ Retourne une Quete déréférencée
        __setitem__ Modifie le niveau d'une quête, prend un tuple en paramètre
    
    Même en récupérant une quête en entrant son nom
    (personnage.quetes["cle_quete"]), on récupère un objet Quete déréférencé.
    Cela veut dire qu'il peut servir pour les opérations de lecture et de
    comparaison, mais qu'écrire dedans ne modifiera pas l'objet Quete du
    personnage. Pour le modifier, il faut utiliser la méthode __setitem__
    (personnage.quetes["nom_quete"] = (1, 2)) qui prend un tuple en paramètre.
    C'est la suite des niveaux. Le premier élément représente le niveau dans
    la quête, le second si présent représente le niveau dans la sous-quête,
    etc.
    
    L'objet Quete que l'on peut obtenir via __getitem__ possède des méthodes
    utiles pour comparer l'objet.
    Si aucune quête n'est définie dans le dictionnaire, retourne un tuple
    contenant 0.
    
    Exemple de manipulation :
    >>> quetes = personnage.quetes # conteneur
    >>> quetes["berger_picte"]
    "0"
    
    Pour plus d'informations, consultez l'aide des méthodes __getitem__ et
    __setitem__ ou, plus spécifiquement, l'aide de l'objet Quete.
    
    """
    
    def __init__(self, parent):
        """Constructeur du conteneur."""
        BaseObj.__init__(self)
        self.__quetes = {}
        self.parent = parent
    
    def __getnewargs__(self):
        return (None, )
    
    def __getitem__(self, cle_quete):
        """Retourne l'objet Quete déréférencé associé au niveau enregistré.
        
        Si aucun objet n'est encore enregistré, retourne (0, ).
        Ce tuple représente "aucun avancement dans la quête".
        
        """
        if cle_quete in self.__quetes.keys():
            return Quete(cle_quete, self.__quetes[cle_quete])
        else:
            return Quete(cle_quete, (0, ))
    
    def __setitem__(self, cle_quete, valeur):
        """Affecte la valeur valeur comme niveau de la quête cle_quete.
        
        La valeur peut être de différents types :
            un tuple, chaque élément étant un entier
            un entier représentant le premier niveau de la quête
            une chaîne, convertit en tuple en utilisant le "." comme séparateur
        
        Par exemple :
            1 est convertit en tuple (1, )
            "1.2" est converti en tuple (1, 2)
        
        Les éléments du tuple caractérisent les niveaux dans une quête. Le tuple
        (1, 2, 1) signifie le niveau 1 dans la quête, sous-niveau 2, sous-
        sous-niveau 1.
        
        """
        if isinstance(valeur, tuple):
            pass
        elif isinstance(valeur, int):
            valeur = tuple(valeur)
        elif isinstance(valeur, str):
            valeur = tuple(int(v) for v in valeur.split("."))
        else:
            raise TypeError("le type {} n'est pas un type valide pour un " \
                    "niveau de quête".format(type(valeur)))
        
        if cle_quete in self.__quetes.keys():
            self.__quetes[cle_quete].mettre_a_jour(valeur)
        else:   
            self.__quetes[cle_quete] = Quete(cle_quete, valeur, self.parent)
    
    def __iter__(self):
        """On itère sur les quêtes."""
        return iter(self.__quetes.copy())
    
    def __repr__(self):
        return "<quetes " + repr(self.__quetes) + ">"
    
    def __str__(self):
        return str(self.__quetes)
    
    @property
    def quetes(self):
        return dict(self.__quetes)
    
    @property
    def etapes_accomplies(self):
        etapes = OrderedDict()
        res_etapes = [q.etapes_accomplies for q in self.__quetes.values()]
        for t_etapes in res_etapes:
            for quete, etape in t_etapes.items():
                if quete.type == "etape" and not quete.parent.ordonnee:
                    liste = etapes.get(quete.parent, [])
                    liste.append(etape)
                    etapes[quete.parent] = liste
                else:
                    etapes[quete] = [etape]
        
        return etapes
    
    @property
    def etapes_a_faire(self):
        etapes = OrderedDict()
        res_etapes = [q.etapes_a_faire for q in self.__quetes.values()]
        for t_etapes in res_etapes:
            for quete, etape in t_etapes.items():
                if quete.type == "etape" and not quete.parent.ordonnee:
                    liste = etapes.get(quete.parent, [])
                    liste.append(etape)
                    etapes[quete.parent] = liste
                else:
                    etapes[quete] = [etape]
        
        return etapes
    
    def valider(self, quete, niveau):
        """Valide la quête."""
        self[quete.cle] = niveau
        self.__quetes[quete.cle].valider(quete, niveau)
    
    def vider(self, cle_quete):
        """Remet à zéro la quête spécifiée."""
        if cle_quete in self.__quetes.keys():
            self.__quetes[cle_quete].detruire()
            del self.__quetes[cle_quete]
        else:
            raise KeyError("la quête {} n'a pu être trouvée".format(cle_quete))
    
    def get_quete(self, cle):
        """Retourne la quête en la créant si n'existe pas."""
        if cle not in self.__quetes:
            self.__quetes[cle] = Quete(cle, (), self.parent)
        return self.__quetes[cle]
