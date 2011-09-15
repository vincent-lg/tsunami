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


"""Fichier contenant la classe SujetAide, détaillée plus bas."""

from abstraits.id import ObjetID
from primaires.format.description import Description
from bases.collections.liste_id import ListeID
from primaires.format.fonctions import supprimer_accents

class SujetAide(ObjetID):
    
    """Classe représentant un sujet d'aide.
    
    Un sujet d'aide est une aide disponible in-game sur un sujet précis. Il peut être consultable par un certain groupe de personnes (seulement les administrateurs du jeu, par exemple) et peut être lié à d'autres sujets.
    
    Ses attributs sont :
        titre -- le titre du sujet
        contenu -- le contenu du sujet d'aide
        sujets_lies -- les sujets liés (des objets SujetAide contenus dans une liste)
    
    """
    
    groupe = "aide"
    sous_rep = "aide/sujets"
    def __init__(self, titre):
        """Constructeur du sujet d'aide."""
        ObjetID.__init__(self)
        self.titre = titre
        self.contenu = Description(parent=self)
        self.__sujets_lies = ListeID(parent=self)
    
    def __getnewargs__(self):
        return ("", )
    
    @property
    def sujets_lies(self):
        """Retourne une liste déréférencée des sujets liés."""
        return [s for s in self.__sujets_lies if s is not None]

ObjetID.ajouter_groupe(SujetAide)
