# -*-coding:Utf-8 -*

# Copyright (c) 2015 LE GOFF Vincent
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


"""Fichier contenant le paramètre 'commenter' de la commande 'rapport'."""

import argparse
import shlex

from primaires.interpreteur.masque.parametre import Parametre

# Constantes
AIDE = """
Cette commande permet de commenter un rapport.
Elle commande prend deux arguments obligatoires :
le numéro du rapport suivi du commentaire. Par exemple
%rapport% %rapport:commenter%|cmd| 12 Bonne suggestion|ff|.
""".strip()

class PrmCommenter(Parametre):

    """Commande 'rapport commenter'."""

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "commenter", "comment")
        self.tronquer = True
        self.schema = "<nombre> <texte_libre>"
        self.aide_courte = "commente un rapport"
        self.aide_longue = AIDE

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        def n_exit(code, msg):
            """Ne quitte pas Python."""
            raise ValueError(msg)

        id = dic_masques["nombre"].nombre
        texte = dic_masques["texte_libre"].texte

        try:
            rapport = importeur.rapport.rapports[id]
        except KeyError:
            personnage << "|err|Ce rapport n'existe pas.|ff|"
            return

        args = {
                "fermer": False,
        }

        if personnage.est_immortel():
            parser = argparse.ArgumentParser(conflict_handler='resolve')
            parser.exit = n_exit

            # Ajout des options
            parser.add_argument("defaut", nargs='*')
            parser.add_argument("-f", "--fermer", action="store_true")

            try:
                args = parser.parse_args(shlex.split(texte))
            except ValueError as err:
                personnage << "|err|Les options n'ont pas été interprétées " \
                        "correctement : {}.|ff|".format(err)
                return

            texte = " ".join(args.defaut)
        elif rapport.createur is not personnage and not rapport.public:
            personnage << "|err|Vous n'avez pas le droit de commenter " \
                    "ce rapport.|ff|"
            return
        else:
            commentaire = texte

        commentaire = rapport.commenter(personnage, texte)
        personnage << "|att|Le rapport #{} a bien été commenté.|ff|".format(
                rapport.id)

        if args.fermer:
            personnage << "Fermeture du rapport."
            rapport.statut = "fermé"

        commentaire.notifier()
