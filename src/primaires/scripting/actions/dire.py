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


"""Fichier contenant l'action dire."""

from primaires.scripting.action import Action
from primaires.scripting.utile.fonctions import get_variables

class ClasseAction(Action):

    """Dit quelque chose.

    C'est l'action standard pour envoyer un message dans l'univers.

    """

    entrer_variables = True

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.dire_personnage, "Personnage", "str")
        cls.ajouter_types(cls.dire_personnage, "Personnage", "str", "str")
        cls.ajouter_types(cls.dire_salle, "Salle", "str")
        cls.ajouter_types(cls.dire_salle, "Salle", "str", "str")
        cls.ajouter_types(cls.dire_joueur, "str", "str")

    @staticmethod
    def dire_personnage(personnage, message, flags="", variables=None):
        """Envoie un message au personnage.

        Paramètres à préciser :

          * personnage : le personnage à qui envoyer le message
          * message : le message à envoyer (une chaîne)
          * flags (optionnel) : un ou plusieurs flags, séparés par un espace

        Flags disponibles :

          * "sp" : envoie sans prompt

        """
        flags = flags.lower()
        for flag in flags.split(" "):
            if flag == "sp":
                personnage.sans_prompt()

        message = message.replace("_b_nl_b_", "\n")
        personnage.envoyer(message, **variables)

    @staticmethod
    def dire_salle(salle, message, flags="", variables=None):
        """Envoie un message aux personnages présents dans la salle.

        Paramètres à préciser :

          * salle : la salle à laquelle envoyer le message
          * message : le message à envoyer (une chaîne)
          * flags (optionnel) : un ou plusieurs flags, séparés par un espace

        Flags disponibles :

          * "sp" : envoie sans prompt

        À noter que tous les personnages contenus dans des variables de
        ce script, s'il y en a, sont exclus de la liste et ne reçoivent
        donc pas ce message.

        """
        flags = flags.lower()
        message = message.replace("_b_nl_b_", "\n")
        f_variables = get_variables(variables, message)
        f_variables["lisser"] = True
        for flag in flags.split(" "):
            if flag == "sp":
                f_variables["prompt"] = False

        salle.envoyer(message, **f_variables)

    @staticmethod
    def dire_joueur(nom_joueur, message, variables):
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
