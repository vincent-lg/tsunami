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


"""Fichier contenant la classe Atelier, détaillée plus bas."""

from abstraits.obase import BaseObj
from secondaires.crafting.exception import ExceptionCrafting

class Atelier(BaseObj):

    """Classe représentant un atelier spécifique à une guilde."""

    def __init__(self, guilde, cle):
        """Constructeur du talent."""
        BaseObj.__init__(self)
        self.guilde = guilde
        self.cle = cle
        self.nom = "un atelier"
        self.matieres = {}
        self._construire()

    def __getnewargs__(self):
        return (None, "")

    def __repr__(self):
        return "<Atelier {} de la guilde {}>".format(repr(self.cle),
                str(self.guilde))

    def __str__(self):
        return "atelier {} de la guilde {}".format(self.cle, str(self.guilde))

    @property
    def cle_complete(self):
        """Retourne une clé plus agréable à la lecture."""
        return self.cle + " : " + self.nom

    def ajouter_matiere(self, cle, quantite=1):
        """Ajoute un prototype de type matière dans l'atelier."""
        if cle not in importeur.objet.prototypes:
            raise MatiereInconnue("Le prototype d'objet {} est " \
                    "inconnu".format(repr(cle)))

        prototype = importeur.objet.prototypes[cle]
        if not prototype.est_de_type("matériau"):
            raise MatiereInconnue("Le prototype d'objet {} n'est " \
                    "pas un matériau".format(repr(cle)))

        if cle not in self.matieres:
            self.matieres[cle] = 0

        self.matieres[cle] += quantite

    def retirer_matiere(self, cle, quantite=1):
        """Retire la matière dans la quantité indiquée."""
        if cle not in self.matieres:
            raise ValueError("Le matériau {} n'est pas présent dans " \
                    "l'atelier".format(repr(cle)))

        self.matieres[cle] -= quantite
        if self.matieres[cle] <= 0:
            del self.matieres[cle]


class MatiereInconnue(ExceptionCrafting):

    """Exception levée si la matière est introuvable."""

    pass
