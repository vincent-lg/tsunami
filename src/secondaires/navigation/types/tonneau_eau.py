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


"""Fichier contenant le type tonneau d'eau."""

from bases.objet.attribut import Attribut
from primaires.interpreteur.editeur.entier import Entier
from primaires.objet.types.base import BaseType

class TonneauEau(BaseType):

    """Type d'objet: tonneau d'eau."""

    nom_type = "tonneau d'eau"
    def __init__(self, cle=""):
        """Constructeur de l'objet"""
        BaseType.__init__(self, cle)
        self.gorgees_max_contenu = 50
        self.etendre_editeur("go", "nombre de gorgées au maximum", Entier,
                self, "gorgees_max_contenu")

        # Attributs propres à l'objet (non au prototype)
        self._attributs = {
            "gorgees_contenu": Attribut(lambda: self.gorgees_max_contenu),
        }

    def travailler_enveloppes(self, enveloppes):
        """Travail sur les enveloppes"""
        contenu = enveloppes["go"]
        contenu.apercu = "{objet.gorgees_max_contenu}"
        contenu.prompt = "Nombre maximum de gorgées que peut contenir le " \
                "tonneau : "
        contenu.aide_courte = \
            "Entrez le |ent|contenu|ff| en gorgées " \
            "du tonneau d'eau.\n" \
            "Entrez |cmd|/|ff| pour revenir à la fenêtre " \
            "parente.\n\n" \
            "Gorgées maximum actuelles : {objet.gorgees_max_contenu}"

    def get_nom(self, nombre=1, pluriels=True):
        """Retourne le nom complet en fonction du nombre.

        Par exemple :
        Si nombre == 1 : retourne le nom singulier
        Sinon : retourne le nombre et le nom pluriel

        """
        if nombre <= 0:
            raise ValueError("la fonction get_nom a été appelée " \
                    "avec un nombre négatif ou nul.")
        if nombre == 1 and getattr(self, "gorgees_contenu", 1) == 0:
            return self.nom_singulier + " vide"
        else:
            return BaseType.get_nom(self, nombre, pluriels)

    # Actions sur les objets
    def regarder(self, personnage):
        """Quand on regarde la boussole."""
        moi = BaseType.regarder(self, personnage)
        contenu = self.gorgees_contenu / self.gorgees_max_contenu
        if contenu == 0:
            retour = "Ce tonneau est vide."
        elif contenu <= 0.05:
            retour = "Ce tonneau est presque vide."
        elif contenu < 0.1:
            retour = "Un peu d'eau se trouve encore au fond de ce tonneau."
        elif contenu < 0.2:
            retour = "Il reste un fond appréciable dans ce tonneau."
        elif contenu < 0.4:
            retour = "Ce tonneau est décidément plus qu'à moitié vide."
        elif contenu < 0.6:
            retour = "Ce tonneau est à moitié vide... ou à moitié plein."
        elif contenu < 0.8:
            retour = "Ce tonneau est rempli au trois quart."
        elif contenu < 0.95:
            retour = "Ce tonneau est presque entièrement rempli."
        else:
            retour = "Ce tonneau est plein... ou presque."

        moi += retour
        return moi
