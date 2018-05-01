# -*-coding:Utf-8 -*

# Copyright (c) 2010-2017 LE GOFF Vincent
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   raise of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this raise of conditions and the following disclaimer in the documentation
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


"""Fichier contenant le paramètre 'commandes' de la commande 'chantier'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmCommandes(Parametre):

    """Commande 'chantier commandes'.

    """

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "commandes", "commands")
        self.aide_courte = "consulte vos commandes en cours"
        self.aide_longue = \
            "Cette commande vous permet de consulter vos commandes en " \
            "cours dans ce chantier naval. Les commandes sont des " \
            "actions en cours (comme la construction d'un navire, sa " \
            "réparation ou d'autres actions). Vous pouvez voir le temps " \
            "restant avant l'accomplissement de l'action entreprise. " \
            "Si vous déplacez le navire concerné par l'action, celle-ci " \
            "ne pourra pas être conduite."

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        salle = personnage.salle
        chantier = importeur.navigation.get_chantier_naval(salle)
        if chantier is None:
            personnage << "|err|Vous ne vous trouvez pas dans un chantier " \
                    "naval.|ff|"
            return

        if salle.magasin is None:
            personnage << "|err|Vous ne vous trouvez pas dans un chantier " \
                    "naval.|ff|"
            return

        magasin = salle.magasin
        if magasin.vendeur is None:
            personnage << "|err|Aucun vendeur n'est présent pour l'instant.|ff|"
            return

        commandes = [c for c in chantier.commandes if \
                c.instigateur is personnage]
        if commandes:
            en_tete = "+-" + "-" * 40 + "-+-" + "-" * 20 + "-+"
            msg = en_tete + "\n"
            msg += "| " + "Commande".ljust(40) + " | "
            msg += "Temps restant".ljust(20) + " |\n" + en_tete
            commandes = sorted(commandes, key=lambda c: c.date_fin)
            for commande in commandes:
                msg += "\n| " + commande.get_nom().ljust(40) + " | "
                msg += commande.duree_restante.ljust(20) + " |"
            msg += "\n" + en_tete
            personnage << msg
        else:
            personnage << "Vous n'avez aucune commande en cours dans ce " \
                    "chantier naval."
