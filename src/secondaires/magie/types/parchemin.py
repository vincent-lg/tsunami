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


"""Fichier contenant le type Parchemin."""

from primaires.interpreteur.editeur.uniligne import Uniligne
from bases.objet.attribut import Attribut
from primaires.objet.types.base import BaseType

class Parchemin(BaseType):

    """Type d'objet: parchemin.

    """

    nom_type = "parchemin"

    def __init__(self, cle=""):
        """Constructeur de l'objet"""
        BaseType.__init__(self, cle)
        self._cle_sort = ""
        self.charges = 1
        self.etendre_editeur("s", "sort", Uniligne, self, "cle_sort")
        self.etendre_editeur("c", "charges", Uniligne, self, "charges")

    def _get_cle_sort(self):
        return self._cle_sort
    def _set_cle_sort(self, sort):
        sorts = [sort.cle for sort in type(self).importeur.magie.sorts.values()]
        if sort in sorts:
            self._cle_sort = sort
    cle_sort = property(_get_cle_sort, _set_cle_sort)

    @property
    def sort(self):
        """Renvoie le sort de ce parchemin."""
        if self.cle_sort:
            return type(self).importeur.magie.sorts[self.cle_sort]
        else:
            return None

    def travailler_enveloppes(self, enveloppes):
        """Travail sur les enveloppes"""
        sort = enveloppes["s"]
        sort.apercu = "{objet.cle_sort}"
        sort.prompt = "Clé du sort : "
        sort.aide_courte = \
            "Entrez la |ent|clé|ff| du sort contenu dans ce parchemin. Il " \
            "va sans dire que le sort\nen question doit être déjà créé. " \
            "Entrez |cmd|/|ff| pour revenir à la fenêtre parente.\n\n" \
            "Sort actuel : {objet.cle_sort}"
        sort.type = str

        charges = enveloppes["c"]
        charges.apercu = "{objet.charges}"
        charges.prompt = "Nombre de charges : "
        charges.aide_courte = \
            "Entrez le |ent|nombre|ff| de charges du parchemin ; ce nombre " \
            "correspond à la quantité\nde sorts que l'on peut lancer avant " \
            "que le parchemin soit inutilisable.\n" \
            "Entrez |cmd|/|ff| pour revenir à la fenêtre parente.\n\n" \
            "Charges actuelles : {objet.charges}"
        charges.type = int

    @staticmethod
    def regarder(objet, personnage):
        """Le personnage regarde l'objet."""
        msg = BaseType.regarder(objet, personnage)
        if getattr(objet, "sort", False):
            de = "de"
            if objet.sort.nom[0] in ["a", "e", "i", "o", "u", "y"]:
                de = "d'"
            if objet.charges > 0:
                s = "s" if objet.charges > 1 else ""
                msg += "\nCe parchemin contient " + str(objet.charges)
                msg += " charge" + s + " du sort " + de + " " + objet.sort.nom
                msg += "."
            else:
                msg += "\nCe parchemin ne contient plus aucune charge."

        return msg
