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


"""Fichier contenant le type Grimoire."""

from bases.objet.attribut import Attribut
from primaires.interpreteur.editeur.uniligne import Uniligne
from primaires.objet.types.base import BaseType

class Grimoire(BaseType):

    """Type d'objet : grimoire.

    Ce type d'objet permet d'apprendre un sort, en l'étudiant, si on
    est du bon élément. Sinon il se détruit et les points de tribut
    du sort sont ajoutés dans les points du lecteur.

    """

    nom_type = "grimoire"

    def __init__(self, cle=""):
        """Constructeur de l'objet"""
        BaseType.__init__(self, cle)
        self._cle_sort = ""
        self.etendre_editeur("s", "sort", Uniligne, self, "cle_sort")

        # Attributs propres à l'objet (non au prototype)
        self._attributs = {
            "proprietaire": Attribut(None),
        }

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
            return importeur.magie.sorts[self.cle_sort]
        else:
            return None

    def travailler_enveloppes(self, enveloppes):
        """Travail sur les enveloppes"""
        sort = enveloppes["s"]
        sort.apercu = "{objet.cle_sort}"
        sort.prompt = "Clé du sort : "
        sort.aide_courte = \
            "Entrez la |ent|clé|ff| du sort appris par ce grimoire. Il " \
            "va sans dire que le sort\nen question doit être déjà créé. " \
            "Entrez |cmd|/|ff| pour revenir à la fenêtre parente.\n\n" \
            "Sort actuel : {objet.cle_sort}"

    def acheter(self, quantite, magasin, transaction):
        """Achète le grimoire."""
        objets = BaseType.acheter(self, quantite, magasin, transaction)
        acheteur = transaction.initiateur

        for objet in objets:
            objet.proprietaire = acheteur

        acheteur.envoyer_tip("Vous êtes propriétaire de ce grimoire. " \
                "Utilisez la commande %étudier% pour l'étudier.")

    def regarder(self, personnage):
        """Le personnage regarde l'objet."""
        sort = self.sort
        if sort:
            if sort.elements[0] != personnage.element:
                return "L'ancre ondule étrangement devant vos yeux... " \
                        "vous ne pouvez lire ce parchemin."

            msg = BaseType.regarder(self, personnage)
            points = sort.points_tribut
            s = "s" if points > 1 else ""
            phrase = "Il vous faut {} point{s} de tribut pour apprendre ce " \
                    "sort.".format(points, s=s)

            msg += "\n\n" + phrase

        return msg
