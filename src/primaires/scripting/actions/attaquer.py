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


"""Fichier contenant l'action attaquer."""

from primaires.format.fonctions import supprimer_accents
from primaires.perso.exceptions.action import ExceptionAction
from primaires.scripting.action import Action

class ClasseAction(Action):

    """Attaque un personnage présent.

    Cette action demande à un premier personnage (de préférence un
    PNJ) d'attaquer un second personnage présent dans la salle.
    Les deux personnages doivent être précisés.

    """

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.attaquer_personnage, "Personnage", "Personnage")

    @staticmethod
    def attaquer_personnage(auteur, cible):
        """Demande au personnage auteur d'attaquer cible."""
        if cible.est_mort():
            return

        try:
            auteur.agir("tuer")
        except ExceptionAction:
            pass
        else:
            auteur.etats.ajouter("combat", vider=True)
            cible.etats;ajouter("combat", vider=True)
            importeur.combat.creer_combat(auteur.salle, auteur, cible)
            auteur.envoyer("Vous attaquez {}.", cible)
            cible.envoyer("{} vous attaque.", auteur)
