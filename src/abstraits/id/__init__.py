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
d'objets identifiés par des ID. La classe ObjetID, détaillée plus bas,
donne plus d'informations sur ces objets.
Ces objets sont aussi destinés à être enregistrés dans des fichiers grâce au
module pickle.

[1] Les objets issus des sous-classes d'ObjetID sont destinés à être
    enregistré dans des fichiers. Leur récupération est également automatisée :
    Au chargement du module 'supenr', les différents groupes sont
    récupérés. Si vous voulez récupérer les objets d'un groupe, appelez
    la méthode 'charger_groupe' de 'supenr' en lui passant en paramètre
    la sous-classe contenant le groupe.

"""

import os
import pickle

from abstraits.obase import BaseObj
from abstraits.id.id import ID, est_id

class StatutObjet:
    """Classe définissant, sous la forme d'attributs de classe, les différents
    statuts d'un objet.
    
    """
    EN_CONSTRUCTION = 0
    INITIALISE = 1
    DETRUIT = 2

class ObjetID(BaseObj):
    
    """Cette classe abstraite peut être héritée des objets qui souhaitent
    obtenir un identifiant unique, propre à chaque objet créé.

    Celui-ci se base sur deux données :
    -   une chaîne de caractères identifiant le groupe d'objets. Ce préfixe
        est nécessaire quand on souhaite grouper plusieurs objets dans
        une structure, un dictionnaire par exemple.
        Quand on souhaite créer un nouveau groupe, on doit hériter cette
        classe en lui donnant un nom de groupe qui sera utilisé pour chaque
        objet créé ;
    -   un entier identifiant clairement le numéro de l'objet. Cet entier
        s'incrémente à chaque fois que l'on crée un objet du groupe.
    
    Exemple : 'salles:45' fait référence à un objet du groupe 'salles'
    (probablement une salle) dont le numéro identifiant est 45. Ainsi, on ne
    risque pas de le confondre avec 'joueurs:45'.
    
    Les objets instanciés depuis cette classe sont également conçus pour être
    enregistrés dans des fichiers par sérialisation. Ainsi, chaque
    objet destiné à être directement enregistré dans un fichier devra
    posséder un identifiant, et donc hériter de cette classe. En revanche,
    il n'est pas nécessaire que chaque attribut enregistré dans l'objet soit
    identifié (voir selon les besoins, au cas par cas);
        
    Mode d'emploi :
    -   Si vous souhaitez définir un nouveau groupe identifiant,
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
        ...     sous_rep = "salles" # sous-répertoire d'enregistrement
        Quand vous créerez votre première salle, elle aura pour ID 'salles:1',
        la seconde aura pour ID 'salles:2' et ainsi de suite.
        Vous devez également redéfinir l'attribut de classe 'sous_rep' qui
        contient le chemin relatif menant aux données de votre groupe.
        NE REDEFINISSEZ PAS LES AUTRES ATTRIBUTS DE CLASSE DE 'ObjetID'
    -   Après avoir défini votre classe, vous devez l'ajouter en tant que
        groupe d'identification. Utilisez pour cela la méthode de classe
        'ajouter_groupe' de 'ObjetID' en lui passant en paramètre votre sous-
        classe nouvellement créée :
        >>> ObjetID.ajouter_groupe(Salle)
    -   Vous pouvez ensuite créer des salles. Elles seront automatiquement
        enregistrées dès leur création (voir l'aide du constructeur d'ObjetID)
        jusqu'à leur destruction. Elles seront également récupérées
        au lancement du MUD, automatiquement, grâce au module 'supenr'.
        Dans notre exemple, au lancement du MUD, une liste contenant les
        salles récupérées par désérialisation sera écrite dans l'attribut de
        classe 'objets' de votre groupe. 'Salle.objets' contiendra, après la
        récupération des données, la liste des salles récupérées
        automatiquement par 'supenr'.
    
    """
    # Attributs à redéfinir en sous-classe
    groupe = "" # la chaîne contenant le nom du groupe préfixant l'ID
    _id_actuel = 1 # on compte à partir de 1
    sous_rep = "" # sous-répertoire menant de _chemin_enr aux données du groupe
    
    # Attributs à ne pas redéfinir
    groupes = {} # dictionnaire des groupes créés ({nom_groupe:classe})
    
    # Méthodes de classe
    def ajouter_groupe(groupe):
        """Méthode appelée lors de la construction de groupes d'ID.
        Après la définition de la sous-classe héritée d'ObjetID,
        cette méthode doit être appelée (on lui passe en paramètre la
        sous-classe). Cette méthode permet de garder une trace des groupes
        créés et de leur ID actuel.
        
        """
        ObjetID.groupes[groupe.groupe] = groupe
        groupe._id_actuel = 1
        BaseObj.importeur.parid[groupe.groupe] = {}
    
    # Méthodes d'instance
    def __init__(self):
        """Constructeur de la classe. On incrémente l'id_actuel du groupe.
        Dans le même temps, on crée un attribut nommé id dans l'objet
        manipulé. On associe à cet attribut un ID contenant le nom du groupe
        et l'identifiant entier le caractérisant.
        Les objets créés sont conçus de telle sorte que si on modifie un de
        leurs attributs, ils soient sauvés dans un fichier. Toutefois,
        pour éviter de les enregistrer dès la création, on paramètre leur
        statut en tant qu'initialisé (voir plus haut la classe 'StatutObjet').
        Après avoir appelé le constructeur de BaseObj qui écrit les attributs
        par défaut de l'objet, on repasse ce statut en 'INITIALISE' et on
        enregistre l'objet.
        
        """
        self._statut = StatutObjet.EN_CONSTRUCTION
        if BaseObj.importeur.parid.construit and type(self).groupe:
            self.id = ID(type(self).groupe, self.id_actuel)
            self.id_actuel = self.id_actuel + 1
        # Appel du constructeur de BaseObj
        BaseObj.__init__(self)
        # On l'ajoute dans le parid
        if BaseObj.importeur.parid.construit and type(self).groupe:
            BaseObj.importeur.parid[self.id.groupe][self.id.id] = self
        # On change le statut et enregistre l'objet
        self._statut = StatutObjet.INITIALISE
        self.enregistrer()
    
    def __str__(self):
        """Affichage ou convertion en chaîne"""
        return str(self.id)
    
    def __setstate__(self, dico_attrs):
        """Méthode appelée lors de la désérialisation d'un objet hérité
        d'ObjetID.
        
        """
        self._statut = StatutObjet.EN_CONSTRUCTION
        self.__dict__.update(dico_attrs)
        BaseObj.__setstate__(self, dico_attrs)
        self._statut = StatutObjet.INITIALISE
        if self.id.id >= self.id_actuel:
            self.id_actuel = self.id.id + 1
        
        # On l'ajoute dans parid
        BaseObj.importeur.parid[self.id.groupe][self.id.id] = self
    
    def __setattr__(self, nom_attr, val_attr):
        """Méthode appelée lorsqu'on cherche à modifier un attribut
        de l'objet. Si l'objet est initialisé, on le place dans l'ensemble
        des objets à enregistrer. On ne l'enregistre pas immédiatement
        mais à chaque tour de boucle synchro. Cela limite
        les accès disque et oppose une légère résistance en cas de corruption
        de données.
        
        """
        BaseObj.__setattr__(self, nom_attr, val_attr)
        if not nom_attr.startswith("_"):
            self.enregistrer()
    
    def _get_id_actuel(self):
        """Retourne l'ID actuel.
        Pour le déduire, on parcourt type(self) puis ses parents.
        
        """
        classe = type(self)
        classe = classe._get_classe_ou_parente_contenant_id(classe)
        return classe._id_actuel
    
    def _get_classe_ou_parente_contenant_id(classe):
        attrs = classe.__dict__
        if "_id_actuel" in attrs.keys():
            return classe
        else:
            classe = classe.__base__
            return classe._get_classe_ou_parente_contenant_id(classe)
    
    def _set_id_actuel(self, id_actuel):
        classe = type(self)._get_classe_ou_parente_contenant_id(type(self))
        classe._id_actuel = id_actuel
    
    id_actuel = property(_get_id_actuel, _set_id_actuel)
    
    def est_initialise(self):
        """Return True si le statut de l'objet est initialisé"""
        return self._statut == StatutObjet.INITIALISE
    
    def enregistrer(self):
        """Enregistre l'objet dans un fichier.
        
        Note: l'objet doit être initialisé.
        
        """
        supenr = BaseObj.importeur.supenr
        if self._statut == StatutObjet.INITIALISE and type(self).groupe:
            supenr.file_attente.add(self)
    
    def detruire(self):
        """Méthode appelée pour détruire l'objet.
        Elle change son statut en StatutObjet.DETRUIT.
        Elle va également demander au superviseur de détruire le fichier
        contenant l'objet.
        
        """
        self._statut = StatutObjet.DETRUIT
        supenr = BaseObj.importeur.supenr
        supenr.detruire_fichier(self)


# Fonctions liées à la manipulation de ces objets

def est_objet_id(objet):
    """Cette fonction renvoie True si l'objet manipulé est un ObjetID ou
    dérivé, False sinon.
    
    """
    return isinstance(objet, ObjetID)

def existe(objet):
    """Retourne True si l'objet existe c'est-à-dire :
    -   s'il n'est pas None
    -   s'il n'est pas ObjetID et détruit
    
    """
    return objet is None or (est_objet_id(objet) and objet._statut != \
            StatutObjet.DETRUIT)

# Décorateurs

def propriete_id(methode):
    """Ce décorateur doit être appelé devant les propriétés utilisant dans
    leur paramètre est IDs.
    
    """
    def red_methode(*parametres):
        parametres = list(parametres)
        for i, parametre in enumerate(parametres):
            if est_id(parametre):
                parametres[i] = parametre.get_objet()
        return methode(*parametres)
    return red_methode
