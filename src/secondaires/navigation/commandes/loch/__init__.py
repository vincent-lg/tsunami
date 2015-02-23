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


"""Package contenant la commande 'loch'."""

from primaires.interpreteur.commande.commande import Commande

class CmdLoch(Commande):

    """Commande 'loch'"""

    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "loch", "log")
        self.nom_categorie = "navire"
        self.aide_courte = "manipule le loch"
        self.aide_longue = \
            "Cette commande permet d'utiliser le loch présent dans la " \
            "salle pour estimer la vitesse du navire."

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        personnage.agir("utiliser_loch")
        salle = personnage.salle
        if not hasattr(salle, "navire") or salle.navire is None or \
                salle.navire.etendue is None:
            personnage << "|err|Vous n'êtes pas sur un navire.|ff|"
            return

        navire = salle.navire
        loch = salle.loch
        if not loch:
            personnage << "|err|Il n'y a pas de loch ici.|ff|"
            return

        personnage << "Vous jetez la corde lestée à la mer."
        personnage.salle.envoyer("{} jète le loch.", personnage)
        vitesse_1 = salle.navire.vitesse_noeuds
        personnage.etats.ajouter("utiliser_loch")
        yield 6
        if "utiliser_loch" not in personnage.etats:
            return

        personnage.etats.retirer("utiliser_loch")
        vitesse_2 = salle.navire.vitesse_noeuds
        vitesse = (vitesse_2 + vitesse_1) / 2
        vitesse = round(vitesse, 1)
        vitesse = str(vitesse).replace(".", ",")
        navire.donnees["vitesse"] = vitesse
        personnage << "Le loch vous donne une vitesse approximative de " \
                "{} noeuds.".format(vitesse)
