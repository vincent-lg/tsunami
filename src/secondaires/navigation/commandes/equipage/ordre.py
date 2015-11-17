# -*-coding:Utf-8 -*

# Copyright (c) 2013 LE GOFF Vincent
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
# ARE DISCLAIMED. IN NO Eéquipage SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""Fichier contenant le paramètre 'ordre' de la commande 'équipage'."""

from primaires.format.fonctions import supprimer_accents
from primaires.interpreteur.masque.parametre import Parametre
from secondaires.navigation.equipage.volonte import volontes

class PrmOrdre(Parametre):

    """Commande 'équipage ordre'.

    """

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "ordre", "order")
        self.schema = "<message>"
        self.aide_courte = "donne un ordre à votre équipage"
        self.aide_longue = \
            "Cette commande permet de donner un ordre à votre équipage. " \
            "L'ordre doit être donné sous la forme d'une notation " \
            "précise. Pour chaque ordre il existe deux notations : " \
            "une notation longue (qui est la plus compréhensible) et " \
            "une notation courte qui s'écrit plus rapidement, n'étant " \
            "composée que de quelques lettres et chiffres."

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        message = supprimer_accents(dic_masques["message"].message)

        salle = personnage.salle
        if not hasattr(salle, "navire"):
            personnage << "|err|Vous n'êtes pas sur un navire.|ff|"
            return

        navire = salle.navire
        if not navire.a_le_droit(personnage, "officier"):
            personnage << "|err|Vous ne pouvez donner d'ordre sur ce " \
                    "navire.|ff|"
            return

        equipage = salle.navire.equipage
        for volonte in volontes.values():
            if volonte.ordre_court is None:
                continue

            groupes = volonte.tester(message)
            if isinstance(groupes, tuple):
                try:
                    arguments = volonte.extraire_arguments(navire, *groupes)
                except ValueError as err:
                    personnage << "|err|" + str(err) + "|ff|"
                    return

                volonte = volonte(navire, *arguments)
                volonte.initiateur = personnage
                volonte.crier_ordres(personnage)
                yield 0.3
                return equipage.executer_volonte(volonte)

        personnage << "|err|Ordre précisé {} invalide.|ff|".format(
                repr(message))
