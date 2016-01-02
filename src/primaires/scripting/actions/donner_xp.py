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


"""Fichier contenant l'action donner_xp."""

from primaires.scripting.action import Action
from primaires.format.fonctions import supprimer_accents
from primaires.scripting.instruction import ErreurExecution

class ClasseAction(Action):

    """Donne de l'XP absolue à un personnage."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.xp_principal, "Personnage", "Fraction")
        cls.ajouter_types(cls.xp_secondaire, "Personnage", "str", "Fraction")

    @staticmethod
    def xp_principal(personnage, xp):
        """Donne l'XP absolue au personnage dans le niveau principal."""
        personnage.gagner_xp(None, int(xp))

    @staticmethod
    def xp_secondaire(personnage, niveau_secondaire, xp):
        """Donne l'XP absolue au personnage dans le niveau secondaire.

        Le nom du niveau doit être donné en son entier.
        Une partie de l'XP est automatiquement transmise au niveau principal.

        """
        niveaux = [n for n in importeur.perso.niveaux.values() if \
                supprimer_accents(n.nom).lower() == supprimer_accents(
                niveau_secondaire)]
        if not niveaux:
            raise ErreurExecution("le niveau {} est introuvable".format(
                    niveau_secondaire))

        personnage.gagner_xp(niveaux[0].cle, int(xp))
