# -*-coding:Utf-8 -*

# Copyright (c) 2010-2017 LE GOFF Vincent
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
# ARE DISCLAIMED. IN NO Eéquipage SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""Fichier contenant le paramètre 'annuler' de la commande 'équipage'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmAnnuler(Parametre):

    """Commande 'équipage annuler'."""

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "annuler", "cancel")
        self.nom_groupe = "administrateur"
        self.schema = "(<cle_navire>)"
        self.aide_courte = "efface les ordres d'un équipage"
        self.aide_longue = \
            "Cette commande permet de supprimer tous les ordres en " \
            "cours d'un équipage. Elle doit être utilisée si un équipage " \
            "se voit donner beaucoup trop d'ordres qu'il ne peut " \
            "accomplir, ce qui peut se produire dans le cas d'un bug " \
            "(même les ordres inopérants ou inefficaces doivent être " \
            "normalement gérés par le système). Précisez en paramètre " \
            "la clé du navire. Si vous ne précisez aucun paramètre, " \
            "la commande opère sur le navire où vous vous trouvez " \
            "actuellement. Les volontés sont également retirées de " \
            "l'équipage. Les contrôles ne sont cependant pas retirés."

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        navire = dic_masques["cle_navire"]
        if navire is None:
            salle = personnage.salle
            if not hasattr(salle, "navire") or salle.navire is None:
                personnage << "|err|Vous n'êtes pas sur un navire.|ff|"
                return

            navire = salle.navire
        else:
            navire = navire.navire

        if navire.equipage is None:
            personnage << "|err|Ce navire n'a pas d'équipage actif.|ff|"
            return

        for matelot in navire.equipage.matelots.values():
            matelot.ordres[:] = []

        navire.equipage.volontes[:] = []
        personnage << "L'équipage du navire {} a bien été " \
                "réinitialisé.".format(navire.cle)
