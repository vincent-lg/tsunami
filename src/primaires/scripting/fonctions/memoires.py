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


"""Fichier contenant la fonction memoires."""

import re

from primaires.format.fonctions import supprimer_accents
from primaires.scripting.fonction import Fonction

class ClasseFonction(Fonction):

    """Renvoie les noms des mémoires de script."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.memoires_salle, "Salle")
        cls.ajouter_types(cls.memoires_salle, "Salle", "str")
        cls.ajouter_types(cls.memoires_perso, "Personnage")
        cls.ajouter_types(cls.memoires_perso, "Personnage", "str")
        cls.ajouter_types(cls.memoires_objet, "Objet")
        cls.ajouter_types(cls.memoires_objet, "Objet", "str")

    @staticmethod
    def memoires_salle(salle, expression=""):
        """Renvoie les mémoires contenues dans la salle précisée.

        Paramètres à entrer :

          * salle : la salle dans laquelle on va chercher les mémoires
          * expression (optionnel) : l'expression qui correspond aux mémoires

        Si une expression est précisée, ne renvoie que les mémoires
        qui correspondent à cette expression. L'expression doit être
        sous la forme d'une expression régulière. Voici un exemple :

            memoires = memoires(salle, "^[a-z]+$")

        """
        if salle in importeur.scripting.memoires:
            return ClasseFonction.filtrer(
                    importeur.scripting.memoires[salle], expression)
        else:
            return []

    @staticmethod
    def memoires_perso(personnage, expression=""):
        """Renvoie les mémoires contenues dans le personnage précisé.

        Paramètres à entrer :

          * personnage : le personnage dans lequel on va chercher les mémoires
          * expression (optionnel) : l'expression qui correspond aux mémoires

        Si une expression est précisée, ne renvoie que les mémoires
        qui correspondent à cette expression. L'expression doit
        être sous la forme d'une expression régulière. Voici un exemple :

            memoires = memoires(personnage, "^[a-z]+$")

        """
        personnage = hasattr(personnage, "prototype") and \
                personnage.prototype or personnage
        if personnage in importeur.scripting.memoires:
            return ClasseFonction.filtrer(
                    importeur.scripting.memoires[personnage], expression)
        else:
            return []

    @staticmethod
    def memoires_objet(objet, expression=""):
        """Renvoie les mémoires contenues dans l'objet précisé.

        Paramètres à entrer :

          * objet : l'objet dans lequel on va chercher les mémoires
          * expression (optionnel) : l'expression qui correspond aux mémoires

        Si une expression est précisée, ne renvoie que les mémoires
        qui correspondent à cette expression. L'expression doit
        être sous la forme d'une expression régulière. Voici un exemple :

            memoires = memoires(objet, "^[a-z]+$")

        """
        if objet in importeur.scripting.memoires:
            return ClasseFonction.filtrer(
                    importeur.scripting.memoires[objet], expression)
        else:
            return []

    @staticmethod
    def filtrer(noms, expression):
        """Filtre les noms de mémoires."""
        noms = list(noms)
        expression = re.compile(expression, re.I)
        for nom in list(noms):
            t_nom = supprimer_accents(nom)
            if expression.search(t_nom) is None:
                noms.remove(nom)

        return noms
