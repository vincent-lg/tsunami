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


"""Fichier contenant l'action equiper."""

from primaires.scripting.action import Action
from primaires.scripting.instruction import ErreurExecution

class ClasseAction(Action):

    """Fait équiper un personnage."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.equiper_prototype, "Personnage", "str")

    @staticmethod
    def equiper_prototype(personnage, cle_prototype):
        """Fait équiper un objet à un personnage.

        Paramètres à préciser :

          * personnage : le personnage qui doit s'équiper
          * cle_prototype : la clé du prototype d'objet à équiper

        Exemple d'utilisation :

          equiper personnage "sabre_bois"

        Le personnage n'a pas besoin d'avoir l'objet indiqué dans
        son inventaire : il sera dans tous les cas créé. En outre,
        cette action ne vérifie pas que le joueur peut s'équiper
        à cet emplacement (utilisez la fonction 'peut_equiper' pour
        vérifier cela).

        """
        if not cle_prototype in importeur.objet.prototypes:
            raise ErreurExecution("prototype d'objet {} introuvable".format(
                    repr(cle_prototype)))

        prototype = importeur.objet.prototypes[cle_prototype]
        objet = importeur.objet.creer_objet(prototype)
        for membre in personnage.equipement.membres:
            if membre.peut_equiper(objet):
                membre.equiper(objet)
                return

        raise ErreurExecution("le personnage {} ne peut équiper {}".format(
                repr(personnage), repr(objet.cle)))
