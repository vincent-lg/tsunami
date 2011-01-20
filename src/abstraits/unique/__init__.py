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
d'objets Unique. Ce sont des objets qui peuvent être directement enregistré
dans des fichiers. A la différence des ObjetID, ces objets ne sont pas censé
produire plusieurs objets différents identifiés par des ID, mais bien
un seul objet par classe dérivant de Unique.

Par exemple, si vous souhaitez sauvegarder les versions du programme, des
données statistiques ou autre, inutile de créer des ObjetID à chaque fois.
Il sera plus logique et facile de tout enregistrer dans un même fichier, dans
un conteneur héritant de Unique.

"""

import os
import pickle

from abstraits.obase import BaseObj

class Unique(BaseObj):
    """Cette classe définit un objet Unique à enregistrer.
    Tous les objets susceptibles d'être enregistré et ne proposant qu'un seul
    objet de cette classe (autrement dit des classes singleton, explicites ou
    implicites) devront hériter de Unique.
    
    L'objet possède lui-même ses informations d'enregistrement.
    Ainsi et sauf si ces informations sont modifiées, créer deux objets et les
    modifier entraînera l'écrasement sur le disque d'un des deux.
    
    """
    
    def __init__(self, sous_rep, nom_fichier, enregistrer=True):
        """Constructeur de la classe.
        -   sous_rep : le sous-répertoire d'enregistrement
        -   nom_fichier : le nom du fichier à enregistrer (dans sous_rep)
        -   enregistrer : un flag spécifiant si l'objet est à enregistrer
            ou non (True par défaut)
        
        """
        # Appel du constructeur de BaseObj
        BaseObj.__init__(self)
        # Attributs
        self._sous_rep = sous_rep
        self._nom_fichier = nom_fichier
        self._enregistrer = enregistrer
        self.enregistrer()
    
    def __setattr__(self, nom_attr, val_attr):
        """Méthode appelée lorsqu'on cherche à modifier un attribut
        de l'objet. On le place dans l'ensemble des objets à enregistrer.
        On ne l'enregistre pas immédiatement mais à chaque tour de boucle
        synchro. Cela limite les accès disque et oppose une légère résistance
        en cas de corruption de données.
        
        """
        BaseObj.__setattr__(self, nom_attr, val_attr)
        if not nom_attr.startswith("_"):
            self.enregistrer()
    
    def enregistrer(self):
        """Enregistre l'objet dans un fichier.
        
        """
        supenr = BaseObj.importeur.supenr
        if self._enregistrer:
            supenr.file_attente.add(self)
    
    def detruire(self):
        """Méthode appelée pour détruire l'objet.
        Elle va demander au superviseur de détruire le fichier
        contenant l'objet.
        
        """
        supenr = BaseObj.importeur.supenr
        supenr.detruire_fichier(self)


# Fonctions liées à la manipulation de ces objets

def est_unique(objet):
    """Cette fonction renvoie True si l'objet manipulé est un Unique ou
    dérivé, False sinon.
    
    """
    return isinstance(objet, Unique)
