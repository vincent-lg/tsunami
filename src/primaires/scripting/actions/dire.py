# -*-coding:Utf-8 -*

# Copyright (c) 2010 LE GOFF Vincent
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


"""Fichier contenant l'action dire."""

from primaires.scripting.action import Action
from primaires.scripting.utile.fonctions import get_variables

class ClasseAction(Action):

    """Dit quelque chose.

    C'est l'action standard pour envoyer un message dans l'univers."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.dire_personnage, "Personnage", "str")
        cls.ajouter_types(cls.dire_salle, "Salle", "str")
        cls.ajouter_types(cls.dire_joueur, "str", "str")

    @staticmethod
    def dire_personnage(personnage, message):
        """Envoie un message au personnage."""
        variables = importeur.scripting.execute_test[-1].evenement.espaces. \
                variables
        personnage.envoyer(message, **variables)

    @staticmethod
    def dire_salle(salle, message):
        """Envoie un message aux personnages présents dans la salle.
        A noter que tous les personnages contenus dans des variables de
        ce script, s'il y en a, sont exclus de la liste et ne reçoivent
        donc pas ce message.

        """
        variables = importeur.scripting.execute_test[-1].evenement.espaces. \
                variables
        f_variables = get_variables(variables, message)
        salle.envoyer(message, **f_variables)

    @staticmethod
    def dire_joueur(nom_joueur, message):
        """Envoie un message ou un mudmail au joueur.

        Si le joueur est déconnecté, le message est envoyé en mudmail
        par l'intermédiaire du joueur système. Si le joueur est connecté,
        il le reçoit directement.

        Paramètres à préciser :

          * nom_joueur : le nom du joueur (exemple "kredh")
          * message : le message à envoyer

        Le message peut éventuellement contenir des variables, comme
        toute chaîne de caractères. Exemple :
            dire "kredh" "Le joueur ${personnage} fait une action."

        """
        variables = importeur.scripting.execute_test[-1].evenement.espaces. \
                variables
        nom_joueur = nom_joueur.capitalize()
        try:
            joueur = importeur.joueur.joueurs[nom_joueur]
        except KeyError:
            raise ErreurExecution("le joueur {} est introuvable".format(repr(
                    nom_joueur)))

        message = message.format(**variables)
        if joueur.est_connecte():
            joueur.envoyer(message)
        else:
            joueur_systeme = importeur.joueur.joueur_systeme
            mail = importeur.communication.mails.creer_mail(
                    joueur_systeme)
            mail.liste_dest.append(joueur)
            mail.sujet = "Message automatique"
            mail.contenu.paragraphes.append(message)
            mail.envoyer()
