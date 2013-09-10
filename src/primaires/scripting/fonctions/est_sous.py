# -*-coding:Utf-8 -*

# Copyright (c) 2012 LE GOFF Vincent
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

"""Fichier contenant la fonction est_sous."""

from primaires.format.fonctions import supprimer_accents
from primaires.scripting.fonction import Fonction

class ClasseFonction(Fonction):

    """Retourne vrai si la salle est sous la perturbation indiquée."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.est_sous_quelle, "Salle")
        cls.ajouter_types(cls.est_sous, "Salle", "str")

    @staticmethod
    def est_sous_quelle(salle):
        """Retourne la clé de la perturbation sous laquelle la salle se trouve.

        Si la salle n'est sous aucune perturbation (il fait grand beau),
        alors retour une chaîne vide.

        Paramètres à entrer :

          * salle - la salle à tester

        Exemple d'usages :

          si est_sous(salle) = "orage:

        Ou :

          perturbation = est_sous(salle)
          si expression(perturbation, "orage|pluie"):

        """
        # Retrouve la perturbation sous laquelle se trouve salle
        perturbation = None
        if salle.interieur:
            return ""

        for p in importeur.meteo.perturbations_actuelles:
            if p.est_sur(salle):
                perturbation = p
                break

        if perturbation is None:
            return ""

        return perturbation.nom_pertu

    @staticmethod
    def est_sous(salle, noms_perturbations):
        """Retourne vrai si la salle est sous l'une des perturbations.

        Le nom des perturbations doit être indiqué (par exemple,
        "pluie"). Plusieurs perturbations peuvent être indiquées,
        séparées par le pipe (|). Par exemple "pluie|orage".

        """
        # Retrouve la perturbation sous laquelle se trouve salle
        perturbation = None
        if salle.interieur:
            return False

        for p in importeur.meteo.perturbations_actuelles:
            if p.est_sur(salle):
                perturbation = p
                break

        if perturbation is None:
            return False

        expressions = supprimer_accents(noms_perturbations.lower())
        for exp in expressions.split("_b_"):
            if perturbation.nom_pertu == exp:
                return True

        return False
