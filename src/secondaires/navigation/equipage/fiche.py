# -*-coding:Utf-8 -*

# Copyright (c) 2013 LE GOFF Vincent
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


"""Fichier contenant la classe FicheMatelot, détaillée plus bas."""

from abstraits.obase import BaseObj
from secondaires.navigation.equipage.constantes import *

class FicheMatelot(BaseObj):

    """Fiche d'un matelot à créer.

    La fiche comprend des informations sur les aptitudes et postes
    spécifiques d'un matelot au niveau prototype. Une fiche pourrait, par
    exemple, dire que le prototype 'marin_ctn' a comme poste par défaut
    'charpentier' et la compétence 'calfeutrage' à 'bon' (ce qui se
    traduit, pour le PNJ créé depuis cette fiche, en l'obtension du
    talent 'calfeutrage' à quelque chose comme 30%).

    """

    enregistrer = True
    def __init__(self, prototype):
        """Constructeur du matelot."""
        BaseObj.__init__(self)
        self.prototype = prototype
        self.poste_defaut = "matelot"
        self.aptitudes = {}

    def __getnewargs__(self):
        return (None, )

    def __repr__(self):
        return "<FicheMâtelot {}>".format(repr(self.cle))

    @property
    def cle(self):
        return self.prototype and self.prototype.cle or "aucune"

    def creer_aptitude(self, nom_aptitude, nom_niveau):
        """Ajoute une aptitude."""
        nom_aptitude = supprimer_accents(nom_aptitude).lower()
        nom_niveau = supprimer_accents(nom_niveau).lower()
        aptitude = CLES_APTITUDES.get(nom_aptitude)
        if aptitude is None:
            raise KeyError("Aptitude inconnue {}".format(repr(nom_aptitude)))

        niveau = VALEURS_NIVEAUX.get(nom_niveau)
        if niveau is None:
            raise KeyError("Niveau inconnu {}".format(repr(nom_niveau)))

        self.aptitudes[aptitude] = niveau

    def creer_PNJ(self, salle=None):
        """Crée le PNJ sur la fiche."""
        if self.prototype is None:
            raise ValueError("Le prototype de cette fiche est inconnu")

        pnj = importeur.pnj.creer_PNJ(self.prototype, salle)

        # Modifie les aptitudes
        for aptitude, niveau in self.aptitudes.items():
            talents = TALENTS.get(aptitude, [])
            connaissance = CONNAISSANCES[niveau]
            for talent in talents:
                pnj.talents[talent] = connaissance
                print("SetTalent", talent, connaissance)

        return pnj
