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


"""Fichier contenant la classe Membre, détaillée plus bas.
Dans ce contexte, un membre est une partie du corps, comme un bras ou une
jambe.

"""

from abstraits.obase import BaseObj

# Flags
AUCUN_FLAG = 0
AFFICHABLE = 1
PEUT_TENIR = 2

FLAGS = {
    "affichable": AFFICHABLE,
    "peut tenir": PEUT_TENIR,
}

STATUTS = ("entier", "brisé")

class Membre(BaseObj):
    
    """Classe définissant un membre, une partie du corps d'un personnage.
    Chaque personnage possède un squelette, qui peut être propre à sa race
    ou à une personnalisation propre. Certains NPCs, par exemple, auront
    des squelettes hors de la définition de toute race;
    
    """
    
    def __init__(self, nom, modele=None, parent=None):
        """Constructeur d'un membre"""
        BaseObj.__init__(self)
        self.nom = nom
        self.flags = AUCUN_FLAG
        self.statut = "entier"
        
        # Copie du modèle si existe
        if modele:
            self.nom = modele.nom
            self.flag = modele.flag
        
        self.parent = parent
    
    def __getinitargs__(self):
        return ("", )
    
    def __setattr__(self, nom_attr, val_attr):
        if not nom_attr.startswith("_") and hasattr(self, "parent") and \
                self.parent:
            self.parent.enregistrer()
    
    def _get_statut(self):
        return self._statut_m
    def _set_statut(self, statut):
        if statut not in STATUTS:
            raise ValueError("Le statut {} n'existe pas pour " \
                    "un membre".format(statut))
        
        self._statut_m = statut
        
        if hasattr(self, "parent") and self.parent:
            self.parent.enregistrer()
    
    statut = property(_get_statut, _set_statut)
