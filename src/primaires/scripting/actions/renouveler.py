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
# LIABLE FOR ANY renouveler_inventaireCT, INrenouveler_inventaireCT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""Fichier contenant l'action renouveler."""

from primaires.scripting.action import Action
from primaires.scripting.instruction import ErreurExecution

class ClasseAction(Action):

    """Renouvelle l'inventaire du magasin précisé."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.renouveler_inventaire_salle, "Salle")
        cls.ajouter_types(cls.renouveler_inventaire_salle, "Salle", "str")

    @staticmethod
    def renouveler_inventaire_salle(salle, flags=""):
        """Renouvelle l'inventaire d'un magasin dans la salle précisée.

        Paramètres à préciser :

          * salle : la salle à renouveler (type salle)
          * flags (optionnel) : une liste de flags

        Flags disponibles :

          * "vider" : vide l'inventaire du magasin avant de renouveler

        La salle précisée doit contenir un magasin. Renouveler
        l'inventaire d'un magasin permet de transférer le stock dans
        l'inventaire : ce qui doit être vendu tel que précisé
        dans le magasin devient en vente. Renouveler l'inventaire
        d'un magasin se fait généralement automatiquement à l'ouverture
        et/ou à la fermeture du magasin en question, mais cette action
        permet d'en renouveler l'inventaire à d'autres moments.

        Exemple d'utilisation :

          salle = salle("zone:mnemo")
          renouveler salle
          #Vide l'inventaire avant de renouveler le stock
          renouveler salle "vider"

        """
        if salle.magasin is None:
            raise ErreurExecution("La salle {} n'est pas un " \
                    "magasin".format(repr(salle.ident)))

        flags = flags.lower().split(" ")
        variables = {}
        if "vider" in flags:
            variables["vider"] = True

        salle.magasin.renouveler(**variables)
