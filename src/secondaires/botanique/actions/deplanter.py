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


"""Fichier contenant l'action deplanter."""

from primaires.scripting.action import Action
from primaires.scripting.instruction import ErreurExecution

class ClasseAction(Action):

    """Plante un végétal dans une salle."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.deplanter, "Salle", "str")
        cls.ajouter_types(cls.deplanter, "Salle", "str", "Fraction")

    @staticmethod
    def deplanter(salle, cle_plante, nombre=None):
        """Retire un végétal de la salle.

        Paramètres à préciser :

          * salle : la salle dans laquelle déplanter
          * cle_plante : la clé du végétal à retirer
          * nombre (optionnel) : le nombre de plantes à retirer

        Si le nombre n'est pas précisé, retire tous les végétaux dont la
        clé est précisée dans la salle.

        Notez qu'aucune alerte ne sera créée si la suppression n'a pas pu se
        faire. Si, par exemple, vous essayez de retirer trois végétaux dans
        la salle indiquée alors qu'il n'y en a que 2, les 2 végétaux seront
        retirés et aucune alerte ne sera créée. Si le végétal n'est
        pas même présent dans la salle spécifiée, aucune alerte ne sera
        créée. Il peut être souhaitable d'utiliser cette action en
        conjonction avec la fonction 'nb_plantes'.

        Exemples d'utilisation :

          # Retire TOUS les pommiers sauvages de la salle
          deplanter salle "pommier_sauvage"
          # Retire 3 pommiers sauvages de la salle
          deplanter salle "pommier_sauvage" 3

        """
        prototype = importeur.botanique.prototypes.get(cle_plante.lower())
        if prototype is None:
            raise ErreurExecution("le végétal {} n'existe pas".format(
                    repr(cle_plante)))

        nombre = int(nombre) if nombre else None
        nb = 0
        for plante in list(importeur.botanique.salles.get(salle, [])):
            print("Nombre", nombre)
            if plante.cle == cle_plante.lower():
                if nombre is None or nb < nombre:
                    importeur.botanique.supprimer_plante(plante.identifiant)
                    nb += 1
