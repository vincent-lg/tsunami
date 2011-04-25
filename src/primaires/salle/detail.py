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


"""Ce fichier contient la classe Detail, détaillée plus bas."""

from abstraits.obase import *
from primaires.format.description import Description

class Detail(BaseObj):
    
    """Cette classe représente un détail observable dans une salle.
    Elle permet d'ajouter à la description d'une salle des détails invisibles
    au premier abord, mais discernable avec la commande look.
    
    """
    
    def __init__(self, nom, synonymes=[], parent=None, modele=None):
        """Constructeur de la classe"""
        BaseObj.__init__(self)
        self.nom = nom
        self.synonymes = list(synonymes)
        self.description = Description()
        self.titre = "un certain détail"
        self.parent = parent
        if modele is not None:
            self.synonymes = modele.synonymes
            self.titre = modele.titre
            self.description = modele.description
        # On passe le statut en CONSTRUIT
        self._statut = CONSTRUIT
    
    def __getinitargs__(self):
        return ("", "")
    
    def __str__(self):
        return self.nom
    
    def __setattr__(self, nom_attr, valeur):
        """Enregisre le parent si il est précisé"""
        construit = self.construit
        BaseObj.__setattr__(self, nom_attr, valeur)
        if construit and self.parent:
            self.parent.enregistrer()
    
    def enregistrer(self):
        """Enregistre le détail dans son parent"""
        construit = self.construit
        if construit and self.parent:
            self.parent.enregistrer()
    
    def regarder(self, personnage):
        """Le personnage regarde le détail"""
        moi = "Vous examinez {} :".format(self.titre)
        description = str(self.description)
        if not description:
            description = "Il n'y a rien de bien intéressant à voir."
        
        moi += "\n\n" + description
        return moi
