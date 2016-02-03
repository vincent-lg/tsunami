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


"""Fichier contenant le masque <nom_sort>."""

from primaires.format.fonctions import contient
from primaires.interpreteur.masque.masque import Masque
from primaires.interpreteur.masque.fonctions import *
from primaires.interpreteur.masque.exceptions.erreur_validation \
        import ErreurValidation

class NomSort(Masque):

    """Masque <nom_sort>.

    On attend le nom d'un sort en paramètre.

    """

    nom = "nom_sort"
    nom_complet = "sort"

    def init(self):
        """Initialisation des attributs"""
        self.sort = None
        self.parchemin = None

    def repartir(self, personnage, masques, commande):
        """Répartition du masque.

        Le masque <nom_sort> prend tout le message.

        """
        nom_sort = liste_vers_chaine(commande).lstrip()
        self.a_interpreter = nom_sort
        commande[:] = []
        if not nom_sort:
            raise ErreurValidation(
                "Spécifiez le nom d'un sort.")

        masques.append(self)
        return True

    def valider(self, personnage, dic_masques):
        """Validation du masque"""
        Masque.valider(self, personnage, dic_masques)
        nom_sort = self.a_interpreter

        sorts = type(self).importeur.magie.sorts
        sorts_connus = [sorts.get(cle) for cle in personnage.sorts.keys() if \
                cle in sorts]
        for sort in sorts_connus:
            if contient(sort.nom, nom_sort):
                self.sort = sort
                return True

        for objet in personnage.equipement.inventaire:
            if objet.est_de_type("parchemin") and objet.sort and contient(
                    objet.sort.nom, nom_sort) and objet.charges > 0:
                self.sort = objet.sort
                self.parchemin = objet
                return True

        raise ErreurValidation(
            "|err|Vous ne connaissez pas ce sort ni ne possédez de " \
            "parchemin fonctionnel.|ff|")
