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


"""Ce package définit la classe abstraite ObjetEnr, squelette
des objets à enregistrer. Voir l'aide de la classe pour plus d'informations.
Il propose également des fonctions propres à la manipulation de tels objets.

"""

import os
import pickle

from abstraits.objet_id import *

class ObjetEnr:
    """Cette classe doit être héritée par TOUS les objets s'enregistrant dans
    le projet. Elle propose quelques méthodes permettant la sérialisation de
    l'instance concernée, grâce au module pickle. En outre, avant
    l'enregistrement, les objets dérivés de ObjetID sont remplacés par l'ID
    correspondante.
    
    En revanche, la récupération des instances correspondant aux ID
    sauvegardées ne se fait pas dans cette classe. Elle n'a aucun moyen
    de connaître la correspondance entre ID et instance.
    Cette tâche est laissée à la classe *** qui, après récupération
    des objets sérialisés, s'occupe de convertir les IDs contenues dans chaque
    objet en instance.
    
    Cette classe permet surtout, grâce à certains dictionnaires
    déclarés lors de l'initialisation, d'enregistrer automatiquement
    l'objet dès qu'il est modifié.
    
    """
    def __init__(self, base_rep, cle_id, dct_base):
        """base_rep est le répertoire dans lequel enregistrer l'objet.
        cle_id est l'identifiant de l'objet. Ce peut être l'ID de l'objet,
        ou un autre identifiant, str ou int. On le convertit de toute façon en
        chaîne, étant donné qu'il servira de base à l'enregistrement de l'objet en
        mémoire (ce sera le nom du fichier).
        
        Les autres attributs à préciser sont :
        -   dct_base : le dictionnaire de base contenant en clé les attributs
            et en valeur les valeurs correspondantes. Si l'attribut existe,
            on ne le change pas. Sinon, on lui donne la valeur par défaut
            précisée. On appelle la méthode 'update' de la classe
            car cette mise à jour pourra s'effectuer après initialisation
        
        """
        self._init = True
        self.base_rep = base_rep
        self.cle_id = str(cle_id)
        self.dct_base = dct_base
        self._init = False
        self.update()
    
    def update(self, dct_base = None):
        """Cette méthode permet de mettre à jour les attributs de l'instance
        grâce au dictionnaire dct_base. Si ce paramètre est laissé à None,
        on se base sur self.dct_base. Dans le cas contraire, on change
        la valeur de self.dct_base.
        
        Note: ce mécanisme simplifie grandement la manipulation d'objets
        sérialisés. On distingue deux cas principaux :
        
        1)  A la création de l'objet : on lui passe un dictionnaire contenant
            le nom des attributs de l'instance, et les valeurs par défaut
            liées à chaque attribut. Vu qu'il s'agit de l'initialisation,
            tous les attributs seront écrits

        2)  A la récupération de l'objet sérialisé : dans ce second cas,
            l'objet possède déjà un certain nombre d'attributs. Il n'est
            ni nécessaire, ni souhaitable de réécrire tous les attributs
            avec leur valeur par défaut dans l'instance, car on écraserait
            les anciens attributs de l'objet. Aussi, on ne donne
            une nouvelle valeur qu'aux attributs qui n'existent pas
            dans l'objet. On appellera dans ce second cas la méthode 'update'
            en lui passant en paramètre le dictionnaire des attributs et
            valeurs correspondant à l'objet
        
        """
        if dct_base is None:
            dct_base = self.dct_base
        else:
            self.dct_base = dct_base
        
        # Mise à jour des attributs
        dct_base.update(self.__dict__)
        self.__dict__ = dct_base
    
    def __setattr__(self, nom_attr, val_attr):
        """Redéfinition de __setattr__. Elle permet d'automatiser
        l'enregistrement d'un objet dès qu'un attribut est modifié.
        
        Note: les attributs commençant par _ n'entraînent pas
        d'enregistrement de l'objet quand ils sont modifiés
        
        """
        object.__setattr__(self, nom_attr, val_attr)
        if not nom_attr.startswith("_") and not self._init:
            self.enregistrer()
    
    def enregistrer(self):
        """Méthode appelée pour enregistrer l'objet en mémoire.
        On se base sur self.cle_id pour trouver le nom du fichier à
        enregistrer.
        
        Note: cette méthode n'est pas sécurisée. On s'assure simplement
        que si une exception est levée lors de l'enregistrement du fichier,
        le fichier soit bien fermé malgré tout. Mais si une exception est
        levée, elle ne sera pas interceptée par cette méthode.
        
        """
        nom_fichier = self.base_rep + os.sep + self.cle_id
        with open(nom_fichier, 'wb') as fichier:
            pic = pickle.Pickler(fichier)
            pic.dump(self)
            fichier.close()
