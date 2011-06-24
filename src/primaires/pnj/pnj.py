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


"""Fichier contenant la classe PNJ, détaillée plus bas."""

from abstraits.id import ObjetID
from primaires.perso.personnage import Personnage

class PNJ(Personnage):
    """Classe représentant un PNJ, c'est-à-dire un personnage virtuel.
    
    Ce personnage est géré par l'univers et n'est pas connecté, à
    la différence d'un joueur.
    
    """
    
    groupe = "pnjs"
    sous_rep = "pnj/pnj"
    
    def __init__(self, prototype):
        """Constructeur du PNJ"""
        Personnage.__init__(self)
        self.prototype = prototype
        if prototype:
            self.identifiant = prototype.cle + "_" + str(
                    prototype.no)
            prototype.no += 1
            prototype.pnj.append(self)
            
            # On copie les attributs propres à l'objet
            # Ils sont disponibles dans le prototype, dans la variable
            # _attributs
            # C'est un dictionnaire contenant en clé le nom de l'attribut
            # et en valeur le constructeur de l'objet
            for nom, val in prototype._attributs.items():
                setattr(self, nom, val.construire(self))
    
    def __getnewargs__(self):
        return (None, )
    
    def __getattr__(self, nom_attr):
        """Si le nom d'attribut n'est pas trouvé, le chercher
        dans le prototype
        
        """
        try:
            Personnage.__getattr__(self, nom_attr)
        except AttributeError:
            return getattr(self.prototype, nom_attr)
    
    def detruire(self):
        """Destruction du PNJ."""
        if self in self.prototype.pnj:
            self.prototype.pnj.remove(self)
        ObjetID.detruire(self)

ObjetID.ajouter_groupe(PNJ)
