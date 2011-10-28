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


"""Fichier contenant le contexte éditeur EdtGenres"""

from primaires.interpreteur.editeur.uniligne import Uniligne
from primaires.format.fonctions import supprimer_accents

class EdtGenres(Uniligne):
    
    """Classe définissant le contexte éditeur 'genres'.
    Ce contexte permet d'éditer les genres d'une race.
    
    """
    
    def __init__(self, pere, objet=None, attribut=None):
        """Constructeur de l'éditeur"""
        Uniligne.__init__(self, pere, objet, attribut)
        self.ajouter_option("a", self.changer_distinction)
    
    def changer_distinction(self, arguments):
        """Change la distinction anonyme.
        
        Syntaxe : /a <genre> <distinction>
        
        """
        if len(arguments.split(" ")) < 2:
            self.pere << "|err|Syntaxe : <genre> <distinction anonyme>|ff|"
            return
        
        nom_genre = supprimer_accents(arguments.split(" ")[0]).lower()
        distinction = " ".join(arguments.split(" ")[1:])
        distinction = distinction[0].upper() + distinction[1:]
        try:
            self.objet.changer_distinction(nom_genre, distinction)
        except KeyError:
            self.pere << "|err|Ce genre est inconnu.|ff|"
        else:
            self.actualiser()
    
    def interpreter(self, msg):
        """Interprétation du message"""
        msg = supprimer_accents(msg.lower())
        genres = self.objet
        genre_entre = msg.split(" ")[0]
        corresp = ""
        if genre_entre in genres:
            del genres[genre_entre]
        else:
            if genre_entre != "masculin" and genre_entre != "feminin":
                try:
                    corresp = msg.split(" ")[1]
                except IndexError:
                    self.pere << "|err|Vous devez préciser une " \
                            "correspondance grammaticale.|ff|"
                    return
            if corresp == "feminin":
                corresp = "féminin"
            genres.ajouter_genre(genre_entre, corresp)
        self.actualiser()
