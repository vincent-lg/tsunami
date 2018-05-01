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


"""Package contenant le paramètre 'marcher' de la commande 'route'."""

from textwrap import dedent

from primaires.interpreteur.masque.parametre import Parametre

class PrmMarcher(Parametre):

    """Commande 'route marcher'"""

    def __init__(self):
        """Constructeur du paramètre."""
        Parametre.__init__(self, "marcher", "walk")
        self.aide_courte = "dessine plusieurs routes d'un coup"
        self.aide_longue = \
            "Cette commande permet de tracer rapidement plusieurs " \
            "routes en marchant, d'où son nom. L'utiliser est plus " \
            "simple que de multiples appels à %route% %route:marquer%, " \
            "bien que le principe soit le même. Cette commande est " \
            "pratique car elle permet de dessiner un complexe de " \
            "routes très facilement. Il suffit de la lancer dans une " \
            "des salles de la carte que l'on souhaite créer et se " \
            "déplacer dans toutes les salles que l'on souhaite inclure. " \
            "Le système s'occupe de créer tout seul les routes, en " \
            "se basant sur le nombre de sorties possibles à une " \
            "salle. Le comportement de cette commande est de créer " \
            "autant de routes que possibles plutôt que des routes " \
            "comportant de nombreuses salles. Ce comportement est " \
            "logique d'un point de vue d'optimisation (il est plus " \
            "facile pour le système de gérer de nombreuses routes " \
            "que de longues routes). Entrez cette commande pour " \
            "commencer à marquer un ensemble de routes, puis entrez " \
            "la de nouveau quand vous avez parcouru toutes les salles " \
            "que vous souhaitez mettre dans le complexe de routes. " \
            "Le système créera automatiquement les routes pour se " \
            "rendre dans chaque salle que vous avez visité."

    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        if personnage in importeur.route.automatiques:
            importeur.route.automatiques.remove(personnage)
            personnage << "Le complexe de route est à présent terminé."
        else:
            importeur.route.automatiques.append(personnage)
            msg = dedent("""
                On commence à marquer le complexe de route.
                Déplacez-vous normalement dans toutes les salles que
                vous souhaitez marquer, puis entrez de nouveau la
                même commande une fois terminé.
            """.strip("\n"))
            personnage << msg
