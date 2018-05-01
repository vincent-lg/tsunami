# -*-coding:Utf-8 -*

# Copyright (c) 2010-2017 DAVY Guillaume
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
# pereIBILITY OF SUCH DAMAGE.


from primaires.interpreteur.contexte import Contexte

import re

## Constantes
# Regex
RE_MAIL_VALIDE = re.compile(r"^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$", re.I)

class EntrerEmail(Contexte):
    """Contexte du choix de l'adresse mail.
    On récupère l'adresse email pour envoyer un mail avec le code de
    validation qui sera récupéré par le contexte suivant
    Note: si le serveur mail n'est pas actif (option configurable), on valide
    automatiquement le compte.

    """
    nom = "connex:creation:entrer_email"

    def __init__(self, pere):
        """Constructeur du contexte"""
        Contexte.__init__(self, pere)

    def get_prompt(self):
        """Message de prompt"""
        return "Votre adresse mail : "

    def accueil(self):
        """Message d'accueil"""
        return \
            "\n|tit|----------= Adresse mail =----------|ff|\n" \
            "Entrez une |cmd|adresse mail|ff| de contact pour votre compte. " \
            "Un message sera envoyé\n" \
            "à cette adresse pour valider le compte ; elle sera " \
            "aussi utilisée si\n" \
            "vous perdez votre |cmd|mot de passe|ff|. Veillez donc à ce " \
            "qu'elle soit valide.\n|att|Les adresses jetables sont " \
            "interdites sur ce serveur.|ff|"

    def deconnecter(self):
        """En cas de déconexion du joueur, on supprime son compte"""
        type(self).importeur.connex.supprimer_compte(self.pere.compte)

    def interpreter(self, msg):
        """Méthode appelée quand un message est réceptionné"""
        cfg_email = type(self).importeur.anaconf.get_config("email")

        # On passe le message en minuscules
        msg = msg.lower()
        if msg in type(self).importeur.connex.email_comptes:
            self.pere.envoyer("|err|Cette adresse mail est déjà utilisée " \
                    "par un autre compte.|ff|")
        elif RE_MAIL_VALIDE.search(msg) is None:
            self.pere.envoyer("|err|L'adresse spécifiée n'est pas valide.|ff|")
        else:
            nom_domaine = msg[msg.find("@") + 1:].lower()
            if nom_domaine in importeur.email.noms_domaines_interdits:
                self.pere.envoyer("|err|Cette adresse e-mail est " \
                        "considérée comme une adresse jetable.|ff|")
                return

            self.pere.compte.adresse_email = msg
            if cfg_email.serveur_mail:
                self.migrer_contexte("connex:creation:validation")
            else:
                self.pere.compte.valide = True
                self.pere.envoyer( \
                    "\n|att|Félicitations, votre compte a bien été validé !" \
                    "|ff|\n\nVous pouvez maintenant commencer à créer un " \
                    "personnage...")
                self.migrer_contexte("connex:connexion:choix_personnages")

