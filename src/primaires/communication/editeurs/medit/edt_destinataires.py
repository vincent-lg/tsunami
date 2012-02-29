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


"""Fichier contenant le contexte éditeur EdtDestinataires"""

from primaires.interpreteur.editeur.uniligne import Uniligne
from primaires.communication.aliases import aliases

class EdtDestinataires(Uniligne):
    
    """Classe définissant le contexte éditeur 'destinataires'.
    Ce contexte permet d'éditer les destinataires d'un message.
    
    """
    
    def __init__(self, pere, objet=None, attribut=None):
        """Constructeur de l'éditeur"""
        Uniligne.__init__(self, pere, objet, attribut)
    
    def interpreter(self, msg):
        """Interprétation du message"""
        entree = msg.split(" ")[0].lower()
        if entree.startswith("@"):
            if not entree[1:] in aliases:
                self.pere << "|err|Cet alias n'existe pas.|ff|"
            else:
                cls_alias = aliases[entree[1:]]
                if cls_alias in self.objet.aliases:
                    self.objet.aliases.remove(cls_alias)
                else:
                    self.objet.aliases.append(cls_alias)
                self.actualiser()
        else:
            joueur = None
            joueurs = type(self).importeur.connex.joueurs
            for t_joueur in joueurs:
                nom = t_joueur.nom.lower()
                if nom == entree:
                    joueur = t_joueur
                    break
            if joueur is None:
                self.pere << "|err|Ce joueur n'a pu être trouvé.|ff|"
            else:
                if joueur in self.objet.liste_dest:
                    self.objet.liste_dest.remove(joueur)
                else:
                    self.objet.liste_dest.append(joueur)
                self.actualiser()
