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
from primaires.format.fonctions import supprimer_accents

class Genres(BaseObj):
    
    """Conteneur de genres.
    Elle contient les genres disponibles pour une race, ainsi que leur
    correspondance grammaticale (masculin ou féminin).
    
    """
    
    def __init__(self, parent=None):
        """Constructeur du conteneur"""
        BaseObj.__init__(self)
        self.parent = parent
        self._genres = { # par défaut
            "masculin": "masculin",
            "féminin": "féminin",
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
        for genre in self._genres.keys():
            if nom == supprimer_accents(genre.lower()):
                return True
        return False
    
    def __len__(self):
        """Retourne le nombre de genres existants"""
        return len(self._genres)
    
    def __getitem__(self, nom):
        """Retourne le genre correspondant"""
        for genre in self._genres.keys():
            if nom == supprimer_accents(genre.lower()):
                return self._genres[genre]
        raise KeyError(nom)
    
    def __delitem__(self, nom):
        """Supprime le genre"""
        for genre in self._genres.keys():
            if nom == supprimer_accents(genre.lower()):
                nom = genre
                break
        del self._genres[nom]
        for d in self._distinctions.keys():
            if nom == supprimer_accents(d.lower()):
                nom = d
                break
        del self._distinctions[nom]
    
    def ajouter_genre(self, nom, corresp=""):
        """Ajoute un genre"""
        self._genres[nom] = corresp if corresp != "" else nom
        # définition des distinctions par défaut
        if self._genres[nom] == "masculin":
            self._distinctions[nom] = "un jeune homme"
        else:
            self._distinctions[nom] = "une jeune femme"
    
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
        sep = ("+" + 16 * "-") * 2 + "+" + 26 * "-" + "+"
        debut = sep + "\n| |tit|" + "Genre".ljust(15)
        debut += "|ff|| |tit|Correspondance|ff| | |tit|"
        debut += "Distinction par défaut".ljust(25) + "|ff||\n"
        for genre, corresp in self._genres.items():
            ligne = "| |grf|" + genre.ljust(15) + "|ff|| " + corresp.ljust(15)
            ligne += "| |vr|" + self._distinctions[genre].ljust(25) + "|ff||"
            lignes.append(ligne)
        ret = debut + sep + "\n" + "\n".join(lignes) + "\n" + sep
        return ret if lignes else "|att|Aucun genre défini.|ff|"
    
    def get_distinction(self, genre):
        """Retourne la distinction correspondant au genre."""
        distinctions = {}
        for nom, val in self._distinctions.items():
            distinctions[supprimer_accents(nom.lower())] = val
        return distinctions[genre]
    
    def changer_distinction(self, nom, distinction):
        """Change la distinction par défaut du genre."""
        if nom not in [supprimer_accents(g.lower()) for g in self._genres.keys()]:
            raise KeyError(nom)
        for d in self._distinctions.keys():
            if nom == supprimer_accents(d.lower()):
                self._distinctions[d] = distinction
                break
