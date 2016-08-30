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


"""Fichier contenant l'action desequiper."""

from primaires.scripting.action import Action
from primaires.scripting.instruction import ErreurExecution
from primaires.objet.conteneur import SurPoids

class ClasseAction(Action):

    """Fait déséquiper un personnage."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.desequiper_objet, "Personnage", "Objet")

    @staticmethod
    def desequiper_objet(personnage, objet):
        """Force un personnage à déséquiper l'objet précisé.

        Cette syntaxe de l'action se rapproche davantage de la commande
        **retirer/remove**. Elle demande à un personnage de déséquiper un
        objet qu'il équipe. L'objet est ensuite placé dans l'inventaire
        du personnage, ou sur le sol si ce n'est pas possible.

        Paramètres à préciser :

          * personnage : le personnage que l'on souhaite déséquiper
          * objet : l'objet que l'on souhaite déséquiper.

        Exemple d'utilisation :

          sabre = equipe(personnage, "sabre_bois")
          desequiper personnage sabre

        """
        if objet.contenu is not personnage.equipement.equipes:
            raise ErreurExecution("{} n'équipe pas {}".format(
                    personnage.nom_unique, objet.identifiant))

        # Essaye de déséquiper l'objet
        try:
            personnage.equipement.equipes.retirer(objet)
        except ValueError:
            raise ErreurExecution("{} ne peut retirer {}".format(
                personnage.nom_unique, objet.identifiant))
        else:
            try:
                personnage.ramasser(objet=objet)
            except SurPoids:
                personnage.equipement.tenir_objet(objet=objet)

            objet.script["retire"].executer(objet=objet,
                    personnage=personnage)
