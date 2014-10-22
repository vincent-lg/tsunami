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


"""Fichier contenant l'action renommer_familier."""

from primaires.scripting.action import Action
from primaires.scripting.instruction import ErreurExecution

class ClasseAction(Action):

    """Renomme un familier."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.renommer_familier, "Personnage", "str")

    @staticmethod
    def renommer_familier(pnj, nom_ou_noms):
        """Renomme un familier.

        Paramètres à préciser :

          * pnj : le PNJ à renommer (doit être un familier)
          * nom_ou_noms : le ou les noms précisés.

        Vous pouvez préciser plusieurs noms séparés par une barre
        verticale (|). Dans ce cas-là, un nom aléatoire sera choisi.
        Notez que cette action essaye de respecter le caractère
        unique d'un nom de familier : si un autre familier du même
        maître possède le même nom, ce nom ne sera pas choisi.
        Vérifiez donc si possible avant de faire apparaître un PNJ
        par scripting que le nombre détenu par le personnage n'est
        pas trop élevé (5 familiers par personnage semble suffisant)
        et précisez cinq alternatives pour les renommer.

        Exemple d'utilisation :

          si nb_familiers(personnage) < 5:
              pnj = creer_familier("cle_du_prototype", personnage)
              renommer_familier(pnj, "Paris|Londres|Boston|Madrid|Dublin")

        """
        identifiant = getattr(pnj, "identifiant", None)
        if identifiant not in importeur.familier.familiers:
            raise ErreurExecution("le personnage {} n'est pas un " \
                    "familier".format(repr(pnj)))

        noms = nom_ou_noms.split("_b_")
        noms = [n.capitalize() for n in noms]
        familier = importeur.familier.familiers[identifiant]
        familier.trouver_nom(noms)
