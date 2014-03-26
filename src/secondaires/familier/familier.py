# -*-coding:Utf-8 -*

# Copyright (c) 2014 LE GOFF Vincent
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


"""Fichier contenant la classe Familier, détaillée plus bas."""

from random import choice

from abstraits.obase import BaseObj
from secondaires.familier.constantes import NOMS

class Familier(BaseObj):

    """Classe représentant un familier.

    Un familier est une sur-couche d'un PNJ, définissant certains
    attributs propres à un familier mais n'intéressant pas le PNJ.
    Par exemple, un familier, contrairement à un PNJ, a un maître.
    Cependant, un familier est toujours modelé sur un PNJ.

    Supposons par exemple que vous avez défini le prototype de PNJ
    'cheval'. Vous créez une fiche de familier de même clé : côté
    du module 'pnj', rien ne se passe. Si vous faites apparaître un
    'cheval', le PNJ sera créé. Mais aucun familier ne sera créé.
    Pour cela, un joueur devra apprivoiser le 'cheval'. À partir du
    moment où il le fait, le PNJ ne s'altère pas mais un familier
    est créé sur ce PNJ. Si le PNJ est détruit (il meurt par exemple),
    le familier est détruit. Mais le familier peut être détruit sans
    que le PNJ soit affecté, si par exemple le maître actuel du
    familier libère le libère.

    """

    enregistrer = True

    def __init__(self, pnj):
        """Constructeur du navire."""
        BaseObj.__init__(self)
        self.pnj = pnj
        self.maitre = None
        self.faim = 0
        self.soif = 0
        self.nom = "Médor"
        self.chevauche_par = None

    def __getnewargs__(self):
        return ("", )

    def __repr__(self):
        return "<Familier {} appartenant à {}>".format(
                self.cle, self.maitre)

    def __str__(self):
        return self.cle

    @property
    def cle(self):
        """Retourne la clé du PNJ."""
        return self.pnj and self.pnj.cle or "aucune"

    @property
    def fiche(self):
        """Retourne la fiche du familier."""
        return importeur.familier.fiches[self.cle]

    @property
    def identifiant(self):
        return self.pnj and self.pnj.identifiant or "aucun"

    @property
    def nom_maitre(self):
        return self.maitre and self.maitre.nom or "aucun"

    @property
    def salle(self):
        return self.pnj and self.pnj.salle or "aucune"

    @property
    def titre_salle(self):
        return self.pnj and self.pnj.salle and self.pnj.salle.titre or \
                "inconnu"

    @property
    def str_faim(self):
        return self.aff_niveau(self.faim)

    @property
    def str_soif(self):
        return self.aff_niveau(self.soif)

    def trouver_nom(self):
        """Recherche un nom qui n'a pas été déjà pris par les familiers."""
        noms = []
        familiers = importeur.familier.familiers_de(self.maitre)
        noms_ex = [f.nom for f in familiers]
        for nom in NOMS:
            if nom not in noms_ex:
                noms.append(nom)

        self.nom = choice(noms)

    def diminuer_faim(self, modifieur):
        """Diminue la faim du familier."""
        self.faim = round(self.faim - modifieur, 2)

        if self.faim < 0:
            self.faim = 0

    def diminuer_soif(self, modifieur):
        """Diminue la soif du PNJ."""
        self.soif = round(self.soif - modifieur, 2)

        if self.soif < 0:
            self.soif = 0

    def augmenter_faim(self, modifieur):
        """Augmente la faim du PNJ."""
        self.faim = round(self.soif + modifieur, 2)

        if self.faim > 100:
            self.faim = 100

    def augmenter_soif(self, modifieur):
        """Augmente la soif du familier."""
        self.soif = round(self.soif + modifieur, 2)

        if self.soif > 100:
            self.soif = 100

    def peut_attaquer(self, personnage):
        """Retourne True si le familier pense pouvoir attaquer la cible."""
        pnj = self.pnj
        return personnage not in (self.maitre, pnj) and pnj.niveau > \
                personnage.niveau

    @staticmethod
    def aff_niveau(niveau):
        """Affiche la faim ou soif en fonction du niveau (entre 0 et 100)."""
        if niveau < 10:
            return "Pas du tout"
        elif niveau < 30:
            return "Un peu"
        elif niveau < 50:
            return "Moyennement"
        elif niveau < 70:
            return "Plutôt"
        elif niveau <= 90:
            return "Énormément"
        else:
            return "Sur le point de dépérir"
