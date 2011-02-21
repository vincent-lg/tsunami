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


"""Fichier contenant la classe Personnage, détaillée plus bas."""

from abstraits.id import ObjetID
from primaires.interpreteur.file import FileContexte

class Personnage(ObjetID):
    """Classe représentant un personnage.
    C'est une classe abstraite. Elle doit être héritée pour faire des joueurs
    et NPCs. Ces autres classes peuvent être également héritées, à leur tour.
    
    Note: on précise bel et bien un nom de groupe, mais on ne l'ajoute pas à
    ObjetID puisqu'il s'agit d'une classe abstraite.
    
    """
    groupe = "personnages"
    sous_rep = "personnages"
    
    def __init__(self):
        """Constructeur d'un personnage"""
        ObjetID.__init__(self)
        self.nom = ""
        self.groupe = "npc"
        self.contextes = FileContexte() # file d'attente des contexte
        self.langue_cmd = "francais"
        self.salle = None
    
    def __getinitargs__(self):
        """Retourne les arguments à passer au constructeur"""
        return ()
    
    def __lshift__(self, msg):
        """Redirige vers 'envoyer'"""
        self.envoyer(msg)
        return self
    
    def _get_contexte_actuel(self):
        """Retourne le contexte actuel, c'est-à-dire le premier de la file"""
        if len(self.contextes) > 0:
            contexte = self.contextes[0]
        else:
            contexte = None
        
        return contexte
    
    def _set_contexte_actuel(self, nouveau_contexte):
        """Ajoute le nouveau contexte à la file des contextes.
        Note : la file peut très bien être manipulée par un contexte qui
        utilisera dans ce cas les méthodes 'ajouter' et 'retirer' de la file
        des contextes.
        
        """
        self.contextes.ajouter(nouveau_contexte)
    
    contexte_actuel = property(_get_contexte_actuel, _set_contexte_actuel)
    
    def envoyer(self, msg):
        """Méthode envoyer"""
        raise NotImplementedError
    
    def regarder(self):
        """Retourne ce qu'il y a autour du personnage"""
        return self.salle.regarder(self)
    
    def deplacer_vers(self, sortie):
        """Déplacement vers la sortie 'sortie'"""
        salle = self.salle
        salle_dest = salle.sorties[sortie].salle_dest
        self.salle = salle_dest
        self.envoyer(self.regarder())
    
    def __setstate__(self, state):
        print("rec", state["salle"])
        ObjetID.__setstate__(self, state)
