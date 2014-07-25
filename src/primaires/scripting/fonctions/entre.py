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


"""Fichier contenant la fonction entre."""

from primaires.scripting.fonction import Fonction
from primaires.scripting.instruction import ErreurExecution

class ClasseFonction(Fonction):

    """Retourne les salles entre deux autres salles."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.entre_salle, "Salle", "Salle")

    @staticmethod
    def entre_salle(origine, destination):
        """Retourne toutes les salles entre origine et destination.

        Cette fonction est très utile pour retourner un chemin DROIT entre
        deux salles. Notez cependant qu'elle ne peut pas être utilisée
        dans tous les cas : origine et destination doivent avoir des
        coordonnées valides et il doit exister un chemin droit et
        continu entre origine et destination. Cela signifie que vous
        ne pourrez probablement pas utiliser cette fonction pour trouver
        les salles intermédiaires entre deux salles inconnues mais que
        vous devrez l'utiliser sur des salles dont vous êtes sûr des
        coordonnées.

        Par exemple, cette fonction peut être utilisée pour parcourir
        toutes les salles entre l'origine d'une rue et la fin d'une
        rue, tant que la rue est droite.

        Paramètres à préciser :

          * origine : la salle d'origine
          * destination : la salle de destination

        Notez que la salle d'origine et de destination ne sont pas inclus
        dans la liste retournée.

        """
        if origine is destination:
            raise ErreurExecution("{} est identique à {}".format(
                    origine, destination))

        if not origine.coords.valide:
            raise ErreurExecution("{} n'a pas de coordonnées valides".format(
                    origine))

        if not destination.coords.valide:
            raise ErreurExecution("{} n'a pas de coordonnées valides".format(
                    destination))

        chemin = origine.trouver_chemin(destination)
        if chemin is None or not chemin.droit:
            raise ErreurExecution("Chemin entre {} et {} introuvable ou " \
                    "non droit".format(origine, destination))

        intermediaires = []
        for sortie in chemin:
            intermediaires.append(sortie.salle_dest)

        intermediaires.remove(destination)
        return intermediaires
