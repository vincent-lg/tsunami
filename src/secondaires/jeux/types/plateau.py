# -*-coding:Utf-8 -*

# Copyright (c) 2010-2016 LE GOFF Vincent
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


"""Fichier contenant le type jeu."""

from bases.objet.attribut import Attribut
from primaires.interpreteur.editeur.choix import Choix
from primaires.objet.types.base import BaseType

class Plateau(BaseType):

    """Type d'objet: plateau de jeu.

    """

    nom_type = "plateau de jeu"
    nettoyer = False
    attributs = {
        "partie": Attribut(),
    }

    def __init__(self, cle=""):
        """Constructeur du type jeu"""
        BaseType.__init__(self, cle)
        self.peut_prendre = False
        plateaux = list(sorted(type(self).importeur.jeux.plateaux.keys()))
        self.plateau = ""
        self.etendre_editeur("l", "plateau", Choix, self, "plateau", plateaux)
    def travailler_enveloppes(self, enveloppes):
        """Travail sur les enveloppes.

        On récupère un dictionnaire représentant la présentation avec en
        clé les raccourcis et en valeur les enveloppes.

        Cela peut permettre de travailler sur les enveloppes ajoutées par
        'etendre_editeur'.

        """
        env = enveloppes["l"] # on récupère 'jeu'
        env.prompt = "Entrez un nom de plateau : "
        env.apercu = "{objet.plateau}"
        env.aide_courte = \
            "Entrez le |ent|nom du plateau|ff| ou |cmd|/|ff| pour revenir à " \
            "la fenêtre mère.\n\n" \
            "Plateaux existants : {liste}\n\n" + \
            "Plateau actuel : " + \
            "|bc|{objet.plateau} |ff|"

    # Actions sur les objets
    def regarder(self, personnage):
        """Quand on regarde le plateau."""
        moi = BaseType.regarder(self, personnage)
        partie = getattr(self, "partie", None)
        if partie:
            moi += "\n\n" + partie.afficher(personnage)

        return moi
