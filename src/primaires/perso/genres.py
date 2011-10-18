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


"""Fichier contenant la classe Sorties, détaillée plus bas;"""

from abstraits.obase import *

class Genres(BaseObj):
    
    """Conteneur des genres.
    Elle contient les genres disponibles pour un classe, ainsi que leur
    correspondance grammaticale (masculin ou féminin).
    
    """
    
    def __init__(self, parent=None):
        """Constructeur du conteneur"""
        BaseObj.__init__(self)
        self.parent = parent
        self._genres = { # par défaut
            "masculin": "masculin",
            "féminin": "féminin"
        }
        self._distinctions = {
            "masculin": "un jeune homme",
            "féminin": "une jeune femme",
        }
        
        # On passe le statut en CONSTRUIT
        self._statut = CONSTRUIT
    
    def __getnewargs__(self):
        return ()
    
    def __contains__(self, nom):
        """Retourne True si 'nom' existe, False sinon"""
        return nom in self._genres
    
    def __len__(self):
        """Retourne le nombre de genres existants"""
        return len(self._genres)
    
    def __getitem__(self, nom):
        """Retourne le genre correspondant"""
        return self._genres[nom]
    
    def __delitem__(self, nom):
        """Supprime le genre"""
        del self._genres[nom]
        if nom in self._distinctions:
            del self._distinctions[nom]
    
    def ajouter_genre(self, nom, corresp=""):
        """Ajoute un genre"""
        self._genres[nom] = corresp or nom
        if self._statut == CONSTRUIT:
            self.parent.enregistrer()
    
    @property
    def str_genres(self):
        """Retourne une chaîne des genres"""
        ret = []
        for genre, corresp in self._genres.items():
            ret.append(genre + \
                    (corresp != genre and " (" + corresp + ") " or ""))
        ret = ", ".join(ret)
        return ret or "aucun"
    
    @property
    def liste_genres(self):
        """Retourne une liste des genres"""
        return list(self._genres.keys())
    
    @property
    def tableau_genres(self):
        """Retourne une chaîne représentant un tableau des genres."""
        lignes = []
        for genre, corresp in self._genres.items():
            tup = (genre, corresp, genre in self._distinctions and \
                    self._distinctions[genre] or "|err|Inconnue|ff|")
            lignes.append("      {:>10}    {:>10}    {}".format(*tup))
        
        if not lignes:
            return "Aucun genre"
        else:
            return "\n".join(lignes)
    
    def changer_distinction(self, nom, distinction):
        """Change la distinction par défaut du genre."""
        if nom not in self._genres:
            raise KeyError(nom)
        
        self._distinctions[nom] = distinction
        self.parent.enregistrer()
