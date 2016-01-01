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


"""Fichier contenant le contexte "personnage:creation:nouveau_nom"""

import re

from primaires.interpreteur.contexte import Contexte
from primaires.format.fonctions import supprimer_accents
from primaires.joueur.joueur import Joueur

## Constantes
# Regex
RE_NOM_VALIDE = re.compile(r"^[A-Za-z]*$")

class NouveauNom(Contexte):
    """Contexte demandant au client d'entrer le nom de son nouveau personnage.

    La validité du nom est établie par la regex 'RE_NOM_VALIDE' et par
    des données de configuration
    précisant la taille minimum du nom, et sa taille maximum.
    On ne peut évidemment n'avoir qu'un seul joueur du même nom.

    Si le nom est valide, on passe au contexte de création suivant.

    """

    nom = "personnage:creation:nouveau_nom"

    def __init__(self, pere):
        """Constructeur du contexte"""
        Contexte.__init__(self, pere)
        self.opts.rci_ctx_prec = "connex:connexion:choix_personnages"

    def sortir(self):
        """En sortant du contexte :

        -   on vérifie que la salle du joueur est valide

        """
        if self.pere.joueur and self.pere.joueur.salle is None:
            # On recherche la salle
            cle = type(self).importeur.salle.salle_arrivee
            salle = type(self).importeur.salle[cle]
            # On ne l'écrit pas dans salle mais _salle pour que le joueur
            # ne soit pas ajouté dans les personnages de la salle
            self.pere.joueur._salle = salle

    def accueil(self):
        """Message d'accueil du contexte"""
        return \
            "\n|tit|----= Choix de votre nom =----|ff|\n" \
            "Entrez un |ent|nom|ff| pour votre nouveau personnage|ff|.\n" \
            "Ce nom peut être identique à votre nom de compte ; " \
            "il vous identifiera\n" \
            "auprès des autres joueurs, une fois entré dans notre monde.\n" \
            "|att|ATTENTION|ff| : Vancia est soumis aux règles du " \
            "RP, votre nom doit être :\n-   Prononçable sans " \
            "difficulté\n-   Cohérent (un parent peut-il nommer un " \
            "enfant comme cela ?)\nÉvitez les noms :\n-   Typiquement " \
            "anglophones\n-   D'un personnage d'une autre fiction\n" \
            "-   D'un pseudonyme de forum"

    def get_prompt(self):
        """Message de prompt"""
        return "Votre nom : "

    def interpreter(self, msg):
        """méthode d'interprétation"""
        cfg_joueur = type(self).importeur.anaconf.get_config("joueur")
        t_min = cfg_joueur.taille_min
        t_max = cfg_joueur.taille_max
        msg = msg.capitalize()
        if len(msg) < t_min or len(msg) > t_max:
            self.pere.envoyer("|err|Le nom de votre joueur doit faire entre " \
                    "{0} et {1} caractères.|ff|".format(t_min, t_max))
        elif importeur.joueur.joueur_existe(msg):
            self.pere.envoyer("|err|Ce nom de personnage est déjà utilisé. " \
                    "Choisissez-en un autre.|ff|")
        elif RE_NOM_VALIDE.search(supprimer_accents(msg).lower()):
            self.pere.joueur.nom = msg
            importeur.joueur.migrer_ctx_creation(self)
        else:
            self.pere.envoyer("|err|Ce nom est invalide. Veuillez " \
                    "réessayer.|ff|")
