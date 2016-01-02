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


"""Fichier contenant l'action creer_perturbation."""

from primaires.scripting.action import Action
from primaires.scripting.instruction import ErreurExecution

class ClasseAction(Action):

    """Crée une perturbation dans la salle spécifiée."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.creer_perturbation, "Salle", "str")

    @staticmethod
    def creer_perturbation(salle, nom_perturbation):
        """Crée une perturbation dans la salle indiquée.

        Le nom de la perturbation doit être son nom système ("pluie", "orage",
        ...).

        Si une perturbation existe déjà au-dessus de cette salle, l'ancienne
        sera effacée et la perturbation spécifiée la remplacera. Elle aura
        exactement le même rayon que l'ancienne perturbation, ce qui
        garantie aucun recouvrement.

        Si aucune perturbation n'existe au-dessus de cette salle, cependant,
        le rayon sera laissé par défaut sauf si un recouvrement est détecté
        à la création. Dans ce cas, le rayon sera réduit jusqu'à éviter le
        recouvrement. Ainsi, si aucune perturbation n'existe sur la salle
        indiquée, le rayon de la nouvelle perturbation pourra être au minimum
        de 1.

        Notez également que la perturbation créée sera statique, c'est-à-dire
        qu'elle ne se déplacera pas. Elle vivra sa vie ordinaire sans se
        déplacer et disparaîtra à la fin de sa durée de vie, aléatoire en
        fonction de la perturbation choisie.

        """
        # On parcourt les perturbations existantes
        a_remplacer = None
        rayon = None
        for perturbation in importeur.meteo.perturbations_actuelles:
            distance = perturbation.distance_au_centre(salle) - \
                    perturbation.rayon
            if distance <= 0: # la salle est sous la perturbation
                a_remplacer = perturbation
                rayon = perturbation.rayon
                break

            if rayon is None or rayon > distance:
                rayon = distance

        # On recherche la perturbation à créer
        a_creer = None
        for perturbation in importeur.meteo.perturbations:
            if perturbation.nom_pertu == nom_perturbation:
                a_creer = perturbation
                break

        if a_creer is None:
            raise ErreurExecution("impossible de trouver la perturbation " \
                    "{}".format(nom_perturbation))

        if a_remplacer:
            a_remplacer.detruire()
            importeur.meteo.perturbations_actuelles.remove(a_remplacer)

        n_pertu = a_creer(salle.coords.get_copie())
        n_pertu.rayon = rayon
        n_pertu.statique = True
        importeur.meteo.perturbations_actuelles.append(n_pertu)
