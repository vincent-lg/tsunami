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


from fractions import Fraction

from .instruction import Instruction
from .parser import expressions

"""Fichier contenant la classe Action, détaillée plus bas."""

actions = {} # dictionnaire des actions répertoriées

class Action(Instruction):
    
    """Classe définissant une action.
    
    Une action est une instruction effectuant une action précise (dire
    à un joueur, faire apparaître un objet, créer une tempête...).
    
    Chaque action peut avoir un comportement différent en fonction du type
    des paramètres qu'on lui transmet.
    
    Chaque action doit hériter de cette classe et être définie dans 
    le sous-package actions. Un module portant le nom de l'action doit
    y être créé. Ce module doit contenir une classe appelée ClasseAction.
    Si ces règles sont suivis, l'action sera automatiquement chargée
    au lancement du module scripting.
    
    Chaque ClasseAction doit redéfinir :
        La méthode init_types -- généralement, dans cette méthode,
                on fait appel à ajouter_types (voir plus bas)
        Plusieurs méthodes statiques représentant les différentes actions
        en fonction des types
    
    Exemple du code de la classe dire.
    Il se trouve dans le sous-package actions, fichier dire.py :
    >>> from primaires.scripting.action import Action
    ... class ClasseAction(Action):
    ...     @classmethod
    ...     def init_types(cls):
    ...         cls.ajouter_types(cls.dire_personnage, "Personnage", "str")
    ...         cls.ajouter_types(cls.dire_salle, "Salle", "str")
    ... @staticmethod
    ... def dire_personnage(personnage, message):
    ...         personnage.envoyer(message)
    ... @staticmethod
    ... def dire_salle(salle, message):
    ...         salle.envoyer(message)
    ...
    
    """
    
    _parametres_possibles = None
    
    @classmethod
    def init_types(cls):
        """Initialise les types à passer à l'action.
        
        Cette méthode est à redéfinir dans chaque sous-classe.
        
        """
        raise NotImplementedError
    
    def __init__(self):
        """Construction d'une action.
        
        """
        Instruction.__init__(self)
        self.parametres = ()
    
    def __str__(self):
        return self.nom + " " + " ".join(self.str_parametres)
    
    @classmethod
    def executer(cls, evenement, *parametres):
        """Exécute l'action selon l'évènement."""
        action = cls.quelle_action(parametres)
        return action(*parametres)
    
    @property
    def str_parametres(self):
        """Retourne les paramètres sous la forme d'une liste de chaînes."""
        parametres = []
        for p in self.parametres:
            parametres.append(str(p))
        
        return tuple(parametres)
    
    @classmethod
    def ajouter_types(cls, methode, *parametres):
        """Ajoute une interprétation possible de l'action.
        
        Les actions peuvent avoir plusieurs interprétations possibles
        en fonction du type de leur paramètre.
        
        Par exemple :
            dire peut prendre un simple message en paramètre
            dire peut aussi prendre un joueur et un message
            dire peut prendre une salle et un message
            ...
        
        Les paramètres suplémentaires sont les types.
        Ce doivent tous être des chaînes de caractères.
        
        """
        if tuple((p for p in parametres if not isinstance(p, str))):
            raise TypeError("les types doivent être des type 'str'")
        
        if parametres in cls._parametres_possibles:
            raise ValueError("les paramètres {} existent déjà pour " \
                    "cette action".format(parametres))
        
        cls._parametres_possibles[parametres] = methode
    
    @classmethod
    def quelle_action(cls, parametres):
        """Retourne l'action correspondant aux paramètres.
        
        Les paramètres se trouvent dans parametres.
        En fonction de leur type on doit savoir quelle action appeler.
        
        Si aucune interprétation des types n'est possible, on lève
        une exception ValueError.
        
        """
        ty_p = [type(p) for p in parametres]
        for types, methode in cls._parametres_possibles.items():
            if all(issubclass(p, t) for p, t in zip(ty_p, types)):
                return methode
        
        raise ValueError("aucune interprétation de la fonction {} " \
                "avec les paramètres {} n'est possible (types {})".format(
                cls.nom, parametres, ty_p))
    
    @classmethod
    def peut_interpreter(cls, chaine):
        """La chaîne peut-elle être interprétée par la classe Action ?"""
        return True
    
    @classmethod
    def construire(cls, chaine):
        """Construit l'instruction.
        
        L'instruction est sous la forme :
            action parametre1 parametre2 parametre3 ...
        
        Le premier mot est donc le nom de l'action.  Ceux suivant
        sont ses paramètres.
        
        """
        action = chaine
        if not chaine.strip():
            raise ValueError("Entrez au moins un nom d'action")
        
        chaine = chaine.split(" ")
        nom_action = chaine[0]
        chaine = " ".join(chaine[1:])
        parametres = []
        types = ("variable", "nombre", "chaine", "fonction")
        types = tuple([expressions[nom] for nom in types])
        while True:
            chaine = chaine.lstrip(" ")
            if not chaine:
                break
            
            types_app = [type for type in types if type.parsable(chaine)]
            if not types_app:
                raise ValueError("impossible de parser {}".format(action))
            elif len(types_app) > 1:
                raise ValueError("l'action {} peut être différemment " \
                        "interprétée".format(action))
            
            type = types_app[0]
            arg, chaine = type.parser(chaine)
            parametres.append(arg)
            
            chaine.lstrip(" ")
            if not chaine:
                break
        
        # On cherche l'action
        try:
            action = actions[nom_action]()
        except KeyError:
            raise ValueError("l'action {} n'existe pas".format(nom_action))
        
        action.parametres = parametres
        
        return action
    
    @classmethod
    def convertir_types(cls):
        """Convertit les types de _parametres_possibles.
        
        Ils sont à l'origine au format str, on va chercher à quel type
        ils correspondent.
        
        """
        for str_types, methode in tuple(cls._parametres_possibles.items()):
            types = __import__("primaires.scripting.types").scripting.types
            s_types = [types.get(t) for t in str_types]
            del cls._parametres_possibles[str_types]
            cls._parametres_possibles[tuple(s_types)] = methode
    
    @property
    def code_python(self):
        """Retourne le code Pytho associé à l'action."""
        py_code = "actions['" + self.nom + "']"
        py_args = ["evt"] + [a.code_python for a in self.parametres]
        py_code += ".executer(" + ", ".join(py_args) + ")"
        return py_code
