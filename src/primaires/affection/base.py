# -*-coding:Utf-8 -*

# Copyright (c) 2012 LE GOFF Vincent
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


"""Ce module contient la classe AffectionAbstraite, détaillée plus bas."""

from abstraits.obase import BaseObj
from corps.fonctions import valider_cle
from .affection import Affection

class AffectionAbstraite(BaseObj):
    
    """Affection abstraite, propre à toutes les affections."""
    
    nom_type = "non renseigné"
    def __init__(self, cle):
        valider_cle(cle)
        BaseObj.__init__(self)
        self.cle = cle
        self.force_max = 50
        self.duree_max = -1
    
    def __getnewargs__(self):
        return ("inconnue", )
    
    def __repr__(self):
        return "<affection de {} {}>".format(self.nom_type, self.cle)
    
    def equilibrer_force(self, force):
        """Équilibre la force et retourne la force_max si besoin."""
        if force > self.force_max:
            force = self.force_max
        
        return force
    
    def equilibrer_duree(self, duree):
        """Équilibre la durée et retourne la duree_max si besoin."""
        if self.duree_max > 0 and duree > self.duree_max:
            duree = self.duree_max
        
        return duree
