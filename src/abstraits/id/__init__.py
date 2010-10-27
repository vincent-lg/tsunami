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


"""Ce package définit les objets et fonctions nécessaires à la manipulation
d'objets identifiées par des ID. La classe ObjetID, détaillée plus bas,
donne plus d'informations sur ces objets.
Ces objets sont aussi destinés à être enregistrés dans des fichiers grâce au
module Pickle.

[1] Les objets issus des sous-classes d'ObjetID sont destinés à être
    enregistré dans des fichiers. Leur récupération est également automatisée :
    Au chargement du module 'supenr', les différents groupes sont
    récupérés et les objets chargés pour chaque groupe se retrouvent dans une
    liste en attribut de la sous-classe (sous_classe.objets').

"""

import os
import pickle

from abstraits.id.id import ID

class StatutObjet:
    """Classe définissant, sous la forme d'attributs de classe, les différents
    statuts d'un objet.
    
    """
    EN_CONSTRUCTION = 0
    INITIALISE = 1
    DETRUIT = 2

class ObjetID:
    """Cette classe abstraite peut être héritée des objets qui souhaitent
    obtenir un identifiant unique, propre à chaque objet créé.

    Celui-ci se base sur deux données :
    -   une chaîne de caractère identifiant le groupe d'objets. Ce préfixe
        est nécessaire quand on souhaite grouper plusieurs objets dans
        une structure, un dictionnaire par exemple. Le module primaire parid
        associe un dictionnaire par groupe d'objet et cela permet de retrouver
        la classe concernée par le préfixe. Quand on souhaite créer
        un nouveau groupe, on doit hériter cette classe en lui donnant
        un nom de groupe qui sera utilisé pour chaque objet créé
    -   un entier identifiant clairement le numéro de l'objet. Cet entier
        s'incrémente à chaque fois que l'on créée un objet du groupe
    
    Exemple : 'salles:45' fait référence à un objet du groupe 'salles'
    (probablement une salle) dont le numéro identifiant est 45. Ainsi, on ne
    risque pas de le confondre avec 'joueurs:45'.
    
    Les objets instanciés depuis cette classe sont également conçus pour être
    enregistrés dans des fichiers par sérialisation. Ainsi, chaque
    objet destiné à être directement enregistré dans un fichier devra
    posséder un identifiant, et donc hériter de cette classe. En revanche,
    il n'est pas nécessaire que chaque attribut enregistré dans l'objet soit
    identifié (voir selon les besoins, au cas par cas);
        
    Note: un mécanisme est mis en place pour que, si un objet possède en
    attribut une référence vers un autre objet, la référence soit conservée.
    Cela signifie que si deux objets possèdent un attribut pointant
    vers le même objet, ce sera toujours vrai après la récupération
    des objets enregistrés. Voir 'enregistrer' pour plus d'informations.
    
    Mode d'emplois :
        Si vous souhaitez définir un nouveau groupe identifiant,
        vous devez hériter de cette classe et redéfinir, dans la sous-classe,
        l'attribut de classe 'groupe' en lui donnant le nom de votre nouveau
        groupe sous la forme d'une chaîne.
        Par exemple :
        >>> # création du groupe destiné à enregistrer des salles
        >>> class Salle(ObjetID):
        ...     '''Si l'on veut créer une nouvelle salle, on passe par cette
        ...     classe.
        ...     
        ...     '''
        ...     groupe = "salles"
        Quand vous créerez votre première salle, elle aura pour ID 'salles:1'
        la seconde aura pour ID 'salles:2' et ainsi de suite.
        Vous pouvez également redéfinir l'attribut de classe 'sous_rep'
        qui contient le chemin relatif menant à vos données enregistrées
        (ce chemin sera naturellement différent pour chaque groupe).
        NE REDEFINISSEZ PAS LES AUTRES ATTRIBUTS DE CLASSE.
    
    """
    id_actuel = 1 # on compte à partir de 1
    groupe = "" # la chaîne contenant le nom du groupe préfixant l'ID
    _supenr = None # superviseur d'enregistrement
    sous_rep = "" # sous répertoire menant de _chemin_enr aux données du groupe
    groupes = {} # dictionnaire des groupes créés ({nom_groupe:classe})
    objets = [] # Voir la note [1]
    
    # Méthodes de classe
    def ajouter_groupe(groupe):
        """Méthode appelée lors de la construction de groupes d'ID.
        Après la définition de la sous-classe héritée d'ObjetID,
        cette méthode doit e^tre appelée (on lui passe en paramètre la
        sous-classe). Cette méthode permet de garder une trace des groupes
        créés et de leur ID actuelle.
        
        """
        ObjetID.groupes[groupe.groupe] = groupe
        groupe.id_actuel = 1
        groupe.objets = []
    
    # Méthodes d'instance
    def __init__(self):
        """Constructeur de la classe. On incrémente l'id_actuel du groupe.
        Dans le même temps, on crée un attribut nommé id dans l'objet
        manipulé. On associe à cet attribut un ID contenant le nom du groupe
        et l'identifiant entier le caractérisant.
        
        """
        self._statut = StatutObjet.EN_CONSTRUCTION
        self.id = ID(type(self).groupe, type(self).id_actuel)
        type(self).id_actuel += 1
        # On laisse aux sous-classes redéfinissant le constructeur
        # la tâche de changer le statut de EN_CONSTRUCTION à INITIALISE
        # à la fin de l'appel au constructeur
    
    def __setstate__(self, dico_attrs):
        """Méthode appelée lors de la sérialisation d'un objet hérité
        d'ObjetID.
        
        """
        self.__dict__.update(dico_attrs)
        if self.id.id >= type(self).id_actuel:
            type(self).id_actuel = self.id.id + 1
    
    def __setattr__(self, nom_attr, val_attr):
        """Méthode appelée lorsqu'on cherche à modifier un attribut
        de l'objet. Si l'objet est initialisé, on le place dans l'ensemble
        des objets à enregistrer. On ne l'enregistre pas immédiatement
        mais bien plus tôt à chaque tour de boucle synchro. Cela limite
        les accès disque et oppose une légère résistance en cas de corruption
        de données.
        
        """
        object.__setattr__(self, nom_attr, val_attr)
        if self._statut == StatutObjet.INITIALISE and ObjetID._supenr:
            ObjetID._supenr.fil_attente.add(self)
    
    def enregistrer(self):
        """Enregistre l'objet dans un fichier.
        Le superviseur (attribut de classe _supenr) doit être défini.
        Le chemin d'enregistrement est déterminé par l'attribut 'racine_enr'
        du superviseur 'supenr', suivi du chemin définit pour le groupe
        (attribut de classe '_sous_rep'). Le nom du fichier est l'identifiant
        de l'objet avec l'extension '.sav'.
        
        Note: l'objet doit être initialisé.
        
        """
        if ObjetID._supenr:
            supenr = ObjetID._supenr
            supenr.enregistrer(self)
        else:
            raise RuntimeError("impossible d'enregistrer {0} : le " \
                    "superviseur 'supenr' n'a pas été trouvé".format(self))
    
    def detruire(self):
        """Méthode appelée pour détruire l'objet.
        Elle change son statut en StatutObjet.DETRUIT.
        Elle va également demander au superviseur de détruire le fichier
        contenant l'objet.
        
        """
        self._statut = StatutObjet.DETRUIT
        if ObjetID._supenr:
            supenr = ObjetID._supenr
            supenr.detruire_fichier(self)
        else:
            raise RuntimeError("impossible de supprimer {0} : le " \
                    "superviseur 'supenr' n'a pas été trouvé".format(self))

# Fonctions liées à la manipulation de ces objets

def est_objet_id(objet):
    """Cette fonction renvoie True si l'objet manipulé est un ObjetID ou
    dérivé, False sinon.
    
    """
    return isinstance(objet, ObjetID)

def existe(objet):
    """Retourne True si l'objet existe c'est-à-dire :
    -   si il n'est pas None
    -   si il n'est pas ObjetID et détruit
    
    """
    return objet is None or (est_objet_id(objet) and objet._statut != \
            StatutObjet.DETRUIT)
