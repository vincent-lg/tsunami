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


"""Fichier contenant l'action ordonner."""

from primaires.format.fonctions import supprimer_accents
from primaires.scripting.action import Action
from primaires.scripting.instruction import ErreurExecution
from secondaires.navigation.equipage.volonte import volontes

class ClasseAction(Action):

    """Donne un ordre à l'équipage d'un navire."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.ordonner, "Salle", "str")

    @staticmethod
    def ordonner(salle, ordre):
        """Donne un ordre à l'équipage.

        Paramètres à renseigner :

          * salle : la salle de navire contenue dans le navire
          * ordre : la chaîne contenant l'ordre et ses paramètres.

        Exemple d'utilisation :

          ordonner salle "plier 3 voiles"

        Vous pouvez aussi utiliser les ordres suivants:

          "suivre cap CLEDUCAP"

        Exemple :

          ordonner salle "suivre cap cilude_38"

        """
        if not hasattr(salle, "navire"):
            raise ErreurExecution("La salle {} n'est pas une salle " \
                    "de navire".format(salle))

        message = supprimer_accents(ordre).lower()
        navire = salle.navire
        equipage = salle.navire.equipage
        commandants = equipage.get_matelots_au_poste("commandant", False)
        commandant = None
        if commandants:
            commandant = commandants[0].personnage

        # Cas particuliers
        if message.startswith("suivre cap "):
            cap = message[11:]
            if cap not in importeur.navigation.trajets:
                raise ErreurExecution("Cap {} inconnu.".format(
                        repr(cap)))
            trajet = importeur.navigation.trajets[cap]
            equipage.ajouter_trajet(trajet)
            return

        # Cas classiques
        for volonte in volontes.values():
            if volonte.ordre_court is None:
                continue

            groupes = volonte.tester(message)
            if isinstance(groupes, tuple):
                try:
                    arguments = volonte.extraire_arguments(navire, *groupes)
                except ValueError as err:
                    raise ErreurExecution(str(err))
                    return

                volonte = volonte(navire, *arguments)
                if commandant:
                    volonte.initiateur = commandant
                    volonte.crier_ordres(commandant)
                equipage.executer_volonte(volonte)
                return

        raise ErreurExecution("Ordre précisé {} invalide.".format(
                repr(message)))
