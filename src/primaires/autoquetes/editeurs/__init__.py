# -*-coding:Utf-8 -*

# Copyright (c) 2010-2017 LE GOFF Vincent
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

"""Package définissant les différents éditeurs propres à AutoQuete."""

from primaires.interpreteur.contexte import MetaContexte
from primaires.interpreteur.editeur.entier import Entier
from primaires.interpreteur.editeur.flag import Flag
from primaires.interpreteur.editeur.flottant import Flottant

# Types d'éditeurs
editeurs = {
    "entier": Entier,
    "flag": Flag,
    "flottant": Flottant,
}

class MetaEditeur(MetaContexte):
    
    """Métaclasse des éditeurs pour les autoquetes.
    
    Note : ce module peut utiliser des éditeurs qui ne sont
    pas définis (ou redéfinis) ici sans inconvénient,
    mais ils devront être ajoutés à la main dans le dictionnaire editeurs.
    
    """
    
    def __init__(cls, nom, bases, contenu):
        """Constructeur de la métaclasse"""
        MetaContexte.__init__(cls, nom, bases, contenu)
        if not cls.nom:
            raise ValueError("la classe " + str(cls) + " ne défini " \
                    "aucun nom")
        
        if cls.nom in editeurs:
            raise ValueError("la classe " + cls.nom + " a déjà " \
                    "été définie")
        
        editeurs[cls.nom] = cls
