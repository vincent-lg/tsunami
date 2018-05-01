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


"""Fichier contenant la fonction salle."""

import re

from primaires.scripting.fonction import Fonction
from primaires.scripting.instruction import ErreurExecution

class ClasseFonction(Fonction):

    """Retourne la salle d'un personnage, d'un objet ou d'après une clé de salle."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.salle_personnage, "Personnage")
        cls.ajouter_types(cls.salle_chaine, "str")
        cls.ajouter_types(cls.salle_objet, "Objet")

    @staticmethod
    def salle_personnage(personnage):
        """Retourne la salle du personnage passé en paramètre"""
        return personnage.salle

    @staticmethod
    def salle_chaine(cle):
        """Retourne la salle correspondante à la clé entrée.

        Paramètres à préciser :

          * cle : la clé de la salle (ne chaîne).

        La clé doit être la zone de la salle et son mnémonique
        séparés par le signe deux points. Par exemple, "picte:1".

        Vous pouvez utiliser le signe '*' pour dire "n'importe quel
        groupe de caractère ici". Cela peut être utile si vous ne
        connaissez pas le nom ou le mnémonique complet. Noez
        cependant que cette fonction va alors devoir parcourir toutes
        les salles, ce qui peut être gourmand en ressources. Évitez
        d'utiliser cette fonction sur des scripts appelés fréquemment
        et automatiquement par le système.

        Exemple d'utilisation :

          # Retourne la première salle de zone commençant par 'pic'
          # Et de mnémonique '1' :
          salle = salle("pic*:1")

        Notez que si vous utilisez un signe '*' dans la recherche, la
        première salle correspondante (ou une valeur nulle) est retournée.

        """
        if "*" in cle:
            # On essaye d'optimiser les performances en compilant la regex
            exp = "^" + re.escape(cle).replace("\\*", ".*") + "$"
            print("Expression", repr(exp))
            ident = re.compile(exp, re.I)
            for t_ident, salle in importeur.salle.salles.items():
                if ident.search(t_ident):
                    return salle

            return None

        # Si il n'y a pas de signe '*'
        try:
            salle = importeur.salle[cle]
        except KeyError:
            raise ErreurExecution("salle inconnue : {}".format(cle))
        else:
            return salle

    @staticmethod
    def salle_objet(objet):
        """Retourne la salle dans laquelle se trouve l'objet.

        Paramètres à préciser :

          * objet : l'objet dont on veut retrouver la salle.

        Attention : un objet peut se trouver possédé par un personnage. Dans
        ce cas, la salle retournée est celle dans laquelle se trouve le
        personnage. Notez aussi que l'objet peut se trouver nullepart
        (cela arrive en cas d'erreur sur une fonction 'creer_objet' par
        exemple, mais aussi dans d'autres situations pour certains objets
        détruits). Vérifiez toujours que la valeur retournée par cette
        fonction existe bien :

          # Retourne toutes les pommes rouges, peu importe où elles sont
          pour chaque objet dans objets("pomme_rouge"):
              salle = salle(objet)
              si salle:
                  dire salle "Les pommes rouges se mettent à danser !"

        """
        parent = objet.grand_parent
        if hasattr(parent, "salle"):
            return parent.salle

        return parent
