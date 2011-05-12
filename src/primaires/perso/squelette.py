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


"""Fichier contenant la classe Squelette, détaillée plus bas."""

from collections import OrderedDict

from abstraits.id import ObjetID
from primaires.format.description import Description
from primaires.format.fonctions import supprimer_accents
from .membre import Membre

class Squelette(ObjetID):
    
    """Classe représentant un squelette.
    Un squelette est un ensemble de membres.
    Plusieurs personnages peuvent posséder un même squelette. Par exemple,
    deux NPCs humains auront tous deux le squelette d'un humain.
    Les membres, cependant, seront bel et bien distincts d'un personnage
    à un autre. Cela inclut donc que, si vous modifiez un squelette déjà
    utilisé, vous pouvez ajouter des membres ou en retirer, mais que vous
    pouvez difficilement modifier un membre (dire, après coup, que tel
    membre aura tel flag par exemple).
    
    En bref, si votre squelett'e est utilisé par une race, évitez de trop
    la modifier après coup. Les joueurs de cette race pourront avoir des
    membres différents avant et après la modification.
    
    """
    
    groupe = "squelettes"
    sous_rep = "squelettes"
    def __init__(self, cle):
        """Constructeur du squelette"""
        ObjetID.__init__(self)
        self.cle = cle
        self.nom = "un squelette"
        self.description = Description(parent=self)
        self.__membres = OrderedDict()
    
    def __getinitargs__(self):
        return ("", )
    
    def __getitem__(self, item):
        item = supprimer_accents(item).lower()
        return self.__membres[item]
    
    def __setitem__(self, item, valeur):
        raise TypeError("vous ne pouvez ajouter ainsi {} au squelette " \
                "{}. Utilisez la méthode ajouter_membre".format(item,
                self.cle))
    
    def __str__(self):
        return self.cle
    
    @property
    def membres(self):
        """Retourne une copie du dicitonnaire des membres"""
        return OrderedDict(self.__membres)
    
    @property
    def presentation_indentee(self):
        """Retourne une présentation indentée des membres"""
        membres = [membre.nom for membre in self.__membres.values()]
        if not membres:
            membres = ["Aucun"]
        
        return "\n  " + "\n  ".join(membres)
    
    def ajouter_membre(self, nom, *args, **kwargs):
        """Construit le membre via son nom et l'ajoute au dictionnaire.
        Les paramètres *args et **kwargs sont transmis au constructeur de
        Membre.
        
        """
        membre = Membre(nom, *args, parent=self, **kwargs)
        nom = supprimer_accents(nom).lower()
        self.__membres[nom] = membre
        self.enregistrer()
        return membre
    
    def supprimer_membre(self, nom):
        """Supprime le membre du dictionnaire."""
        nom = supprimer_accents(nom).lower()
        if nom not in self.__membres.keys():
            raise KeyError("Le membre {} n'existe pas dans ce " \
                    "squelette".format(nom))
        
        del self.__membres[nom]
        self.enregistrer()

ObjetID.ajouter_groupe(Squelette)
