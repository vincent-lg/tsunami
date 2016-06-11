# -*-coding:Utf-8 -*

# Copyright (c) 2010-2016 LE GOFF Vincent
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


"""Fichier définissant la classe Piece, détaillée plus bas."""

from abstraits.obase import BaseObj

class Piece(BaseObj):
    
    """Classe représentant une pièce du poquiir."""
    
    def __init__(self, nom, couleur, points, fem=True):
        """Constructeur du pion."""
        BaseObj.__init__(self)
        self.nom = nom
        self._couleur = couleur
        self.points = points
        self.fem = fem
        self._construire()
    
    def __getnewargs__(self):
        return ("", "", 0)
    
    def __repr__(self):
        return self.nom_complet_indefini
    
    @property
    def couleur(self):
        return self._couleur.format(e="e" if self.fem else "")
    
    @property
    def article_indefini(self):
        return "une" if self.fem else "un"
    
    @property
    def article_defini(self):
        if self.nom.startswith("aeiouyh"):
            return "l'"
        
        return "la" if self.fem else "le"
    
    @property
    def nom_complet_defini(self):
        nom = self.article_defini
        if not nom.endswith("'"):
            nom += " "
        nom += self.nom
        nom += " " + self.couleur
        nom += " (" + str(self.points) + ")"
        return nom
    
    @property
    def nom_complet_indefini(self):
        nom = self.article_indefini + " "
        nom += self.nom
        nom += " " + self.couleur
        nom += " (" + str(self.points) + ")"
        return nom
