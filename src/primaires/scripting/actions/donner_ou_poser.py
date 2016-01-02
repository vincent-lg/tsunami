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


"""Fichier contenant l'action donner_ou_poser."""

from primaires.scripting.action import Action

class ClasseAction(Action):

    """Donne quelque chose à un personnage ou le pose.

    Cette fonction doit donner l'objet au personnage si il peut le prendre
    ou bien le poser sur le sol. Dans ce dernier cas, le personnage sera
    notifié que l'objet est au sol (il est donc bon d'envoyer un message
    informant le joueur qu'il reçoit l'objet avant d'appeler cette
    action).

    """

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.donner_objet, "Personnage", "Objet")
        cls.ajouter_types(cls.donner_prototype_nb, "Personnage", "str",
                "Fraction")

    @staticmethod
    def donner_objet(personnage, objet):
        """Donne un objet au personnage (variable de type Objet)."""
        if not objet.peut_prendre:
            raise ErreurExecution("{} ne peut pas être manipulé".format(
                    objet.get_nom()))

        if objet.contenu:
            try:
                objet.contenu.retirer(objet)
            except ValueError:
                pass

        personnage.ramasser_ou_poser(objet)

    @staticmethod
    def donner_prototype_nb(personnage, prototype, nb):
        """Donne au personnage nb objets modelés sur le prototype précisé."""
        nb = int(nb)
        if not prototype in importeur.objet.prototypes:
            raise ErreurExecution("prototype {} introuvable".format(prototype))

        prototype = importeur.objet.prototypes[prototype]
        for i in range(nb):
            objet = importeur.objet.creer_objet(prototype)
            if not objet.peut_prendre:
                raise ErreurExecution("{} ne peut pas être manipulé".format(
                        objet.get_nom()))

            personnage.ramasser_ou_poser(objet)
