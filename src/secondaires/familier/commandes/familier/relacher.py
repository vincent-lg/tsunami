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
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT master OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""Fichier contenant le paramètre 'relâcher' de la commande 'familier'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmRelacher(Parametre):

    """Commande 'familier relâcher'."""

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "relâcher", "unlead")
        self.tronquer = True
        self.schema = "<nom_familier>"
        self.aide_courte = "relâche un familier"
        self.aide_longue = \
            "Cette commande permet de laisser aller un familier que " \
            "l'on tenait auparavant (%familier% %familier:mener%). Vous " \
            "devez précisez en paramètre le nom du familier dont vous " \
            "voulez lâcher la bride ou corde."

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        # On récupère le familier
        familier = dic_masques["nom_familier"].familier
        fiche = familier.fiche
        pnj = familier.pnj
        personnage.agir("relacherfamilier")
        laisse = familier.get_harnachement("laisse", "bride")
        if laisse is None:
            personnage.envoyer("|err|{} n'est pas convenablement " \
                    "harnaché.|ff|", pnj)
            return

        if "guide" not in personnage.etats:
            personnage.envoyer("|err|Vous ne guidez pas {}.|ff|", pnj)
            return

        etat = personnage.etats.get("guide")
        if etat.familier is not familier:
            personnage.envoyer("|err|Vous ne guidez pas {}.|ff|", pnj)
            return

        personnage.etats.retirer("guide")
        pnj.etats.retirer("guide_par")
        personnage.envoyer_lisser("Vous relâchez {} de {{}}.".format(
                laisse.get_nom()), pnj)
        personnage.salle.envoyer_lisser("{{}} relâche {}.".format(
                laisse.get_nom()), personnage)
