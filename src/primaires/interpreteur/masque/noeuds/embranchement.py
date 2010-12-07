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


"""Fichier définissant la classe Embranchement détaillée plus bas."""

from primaires.interpreteur.masque.noeuds.base_noeud import BaseNoeud

class Embranchement(BaseNoeud):
    """Un noeud embranchement, constitué non pas d'un seul suivant mais de
    plusieurs, sous la forme d'une liste extensible.
    
    """
    
    def __init__(self):
        """Constructeur de l'embranchement"""
        BaseNoeud.__init__(self)
        self.suivant = {} # {noeud:commande}
    
    def _get_fils(self):
        """Retourne les noeuds fils, c'est-à-dire suivant qui est à passer sous
        la forme d'une liste.
        
        """
        return self.suivant.keys()
    
    fils = property(_get_fils)
    
    def ajouter_fils(self, noeud_fils, commande=None):
        """Ajoute un fils à l'embranchement"""
        self.suivant[noeud_fils] = commande
    
    def __str__(self):
        """Méthode d'affichage"""
        msg = "emb("
        msg += ", ".join( \
            [str(cmd) + "=" + str(noeud) for noeud, cmd in \
            self.suivant.items()])
        msg += ")"
        return msg
    
    def valider(self, personnage, dic_masques, commande):
        """Validation du noeud Embranchement.
        La commande entrée par le personnage peut avoir déjà été réduite par
        les noeuds précédents. Elle est sous la forme d'une liste de
        caractères.
        
        """
        valide = False
        for fils in self.fils:
            valide = fils.valider(personnage, dic_masques, commande)
            if valide:
                fils.commande.interpreter(personnage, dic_masques)
                break
        
        return valide
