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


"""Fichier contenant la fonction objet."""

from primaires.scripting.fonction import Fonction
from primaires.objet.conteneur import SurPoids

class ClasseFonction(Fonction):
    
    """Recherche et retourne un objet."""
    
    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.objet_salle, "Salle", "str")
        cls.ajouter_types(cls.objet_perso, "Personnage", "str")
    
    @staticmethod
    def objet_salle(salle, cle_prototype):
        """Retourne, si trouvé, l'objet indiqué posé dans la salle.
        
        Vous devez préciser en paramètre la salle et la clé du prototype
        de l'objet. L'objet retourné est cherché parmi les objets posés
        au sol de la salle. Si aucun n'est trouvé, retourne une valeur
        nulle.
        
        """
        for objet in salle.objets_sol._objets:
            if objet.cle == cle_prototype:
                return objet
        
        return None
    
    @staticmethod
    def objet_perso(personnage, cle_prototype):
        """Retourne, si trouvé, l'objet indiqué possédé par le personnage.
        
        La recherche se fait dans l'inventaire étendu (comprenant
        donc l'équipement) du personnage. Vous pouvez par exemple
        chercher le premier objet de clé "sac_toile" possédé par
        le personnage. Si il en possède effectivement un (ou plusieurs),
        le premier trouvé est retourné. Sinon, une valeur nulle est
        retournée.
        
        """
        # on teste l'inventaire
        for o in personnage.equipement.inventaire:
            if o.cle == cle_prototype:
                return o
        
        return None
