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


"""Fichier contenant le type sextant."""

from primaires.interpreteur.editeur.uniligne import Uniligne
from bases.objet.attribut import Attribut
from primaires.objet.types.instrument import Instrument
from corps.fonctions import lisser
from primaires.vehicule.vecteur import Vecteur


class Sextant(Instrument):

    """Type d'objet: sextant.

    """

    nom_type = "sextant"

    def __init__(self, cle=""):
        """Constructeur de l'objet"""
        Instrument.__init__(self, cle)
        self.emplacement = "mains"
        self.positions = (1, 2)
        self.precision = 10
        self.calcul = 60
        self.etendre_editeur("r", "précision", Uniligne, self, "precision")
        self.etendre_editeur("ca", "temps de calcul", Uniligne, self, "calcul")

    def travailler_enveloppes(self, enveloppes):
        """Travail sur les enveloppes"""
        precision = enveloppes["r"]
        precision.apercu = "{objet.precision}"
        precision.prompt = "Précision (en minutes) du sextant : "
        precision.aide_courte = \
            "Entrez la |ent|précision|ff| du sextant, |cmd|1|ff| au " \
            "minimum.\n" \
            "Plus le chiffre est bas, plus le sextant est précis.\n" \
            "Notez que le sextant est toujours précis en degrés, la " \
            "précision\nest en minutes.\n" \
            "Entrez |cmd|/|ff| pour revenir à la fenêtre " \
            "parente.\n\n" \
            "Précision actuelle : {objet.precision}"
        precision.type = int

        # Temps de calcul
        calcul = enveloppes["ca"]
        calcul.apercu = "{objet.calcul} secondes"
        calcul.prompt = "Temps de calcul nécessaire (en secondes) : "
        calcul.aide_courte = \
            "Entrez le |ent|temps de calcul|ff| du sextant en secondes.\n" \
            "Entrez |cmd|/|ff| pour revenir à la fenêtre " \
            "parente.\n\n" \
            "Temps actuelle : {objet.calcul} secondes"
        calcul.type = int

    # Actions sur les objets
    def regarder(self, personnage):
        """Quand on regarde la sextant."""
        moi = Instrument.regarder(self, personnage)
        personnage.envoyer_tip("Entrez la commande %point% pour " \
                "faire le point.")

        return moi
