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


"""Fichier contenant la fonction creer_familier."""

from primaires.scripting.fonction import Fonction
from primaires.scripting.instruction import ErreurExecution

class ClasseFonction(Fonction):

    """Crée un PNJ à partir du prototype précisé."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.creer_familier, "str", "Personnage")
        cls.ajouter_types(cls.creer_familier_PNJ, "Personnage", "Personnage")

    @staticmethod
    def creer_familier(prototype, maitre):
        """Crée un familier sur le prototype précisé.

        Paramètres à préciser :

          * prototype : la clé du prototype (celle de la fiche de familier)
          * maitre : le personnage qui deviendra le maître du familier

        Cette fonction retourne le PNJ créé, comme 'creer_PNJ'.
        Prenez garde de toujours stocker les PNJs créés dans des variables
        afin de ne pas créer de PNJs fantômes.

        """
        if not prototype in importeur.pnj.prototypes:
            raise ErreurExecution("prototype {} introuvable".format(prototype))
        if not prototype in importeur.familier.fiches:
            raise ErreurExecution("fiche de familier {} introuvable".format(
                    prototype))
        prototype = importeur.pnj.prototypes[prototype]
        if prototype.squelette is None:
            raise ErreurExecution("prototype {} sans squelette".format(
                    prototype))
        pnj = importeur.pnj.creer_PNJ(prototype)
        familier = importeur.familier.creer_familier(pnj)
        familier.maitre = maitre
        familier.trouver_nom()
        return pnj

    @staticmethod
    def creer_familier_PNJ(pnj, maitre):
        """Crée un familier sur le PNJ existant.

        Paramètres à préciser :

          * pnj : le PNJ existant
          * maitre : le personnage qui deviendra le maître du familier

        Cette fonction travaille sur un PNJ déjà existant. Le
        PNJ doit avoir une fiche de familier valide (et ne pas
        déjà être un familier). Le PNJ est retourné.

        """
        cle = getattr(pnj, "cle", None)
        identifiant = getattr(pnj, "identifiant", None)
        if cle not in importeur.familier.fiches:
            raise ErreurExecution("aucune fiche de famillier associée " \
                    "au personnage {}".format(repr(pnj)))

        if identifiant in importeur.familier.familiers:
            raise ErreurExecution("le PNJ {} est déjà un familier".format(
                    repr(pnj)))

        familier = importeur.familier.creer_familier(pnj)
        familier.maitre = maitre
        familier.trouver_nom()
        return pnj
