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


"""Fichier contenant le contexte 'personnage:creation:choix_genre'"""

from primaires.interpreteur.contexte import Contexte
from primaires.format.fonctions import *

class ChoixGenre(Contexte):

    """Contexte demandant au client de choisir le genre de son personnage.

    """

    nom = "personnage:creation:choix_genre"
    def __init__(self, pere):
        """Constructeur du contexte"""
        Contexte.__init__(self, pere)
        self.opts.rci_ctx_prec = "personnage:creation:choix_race"

    def accueil(self):
        """Message d'accueil du contexte"""
        genres = self.pere.joueur.race.genres
        noms_genres = genres.liste_genres
        return \
            "\n|tit|---------= Choix du genre =--------|ff|\n" \
            "Choisissez le |ent|genre|ff| de votre personnage.\n\n" \
            "Genres disponibles :\n\n" \
            "  " + "\n  ".join(noms_genres)

    def get_prompt(self):
        """Message de prompt"""
        return "Entrez un genre : "

    def interpreter(self, msg):
        """Méthode d'interprétation"""
        genre = supprimer_accents(msg).lower()

        genres = self.pere.joueur.race.genres
        genres = [supprimer_accents(g.lower()) for g in genres.liste_genres]

        if not genre in genres:
            self.pere << "|err|Ce genre n'est pas disponible.|ff|"
        else:
            self.pere.joueur.genre = genre

            if self.pere.joueur not in self.pere.compte.joueurs:
                self.pere.compte.ajouter_joueur(self.pere.joueur)
            self.pere.joueur.contextes.vider()
            self.pere.joueur.pre_connecter()
