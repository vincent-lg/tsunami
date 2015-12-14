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
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT master OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""Fichier contenant le paramètre 'boire' de la commande 'familier'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmBoire(Parametre):

    """Commande 'familier boire'."""

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "boire", "drink")
        self.tronquer = True
        self.schema = "<nom_familier>"
        self.aide_courte = "demande à un familier de boire"
        self.aide_longue = \
            "Cette commande demande au familier dont le nom est " \
            "précisé en paramètre de boire dans la salle où vous vous " \
            "trouvez. Les familiers peuvent boire dans les cours d'eau " \
            "potables, les fontaines et les tonneaux d'eau à bord des " \
            "navires."

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        # On récupère le familier
        familier = dic_masques["nom_familier"].familier
        fiche = familier.fiche
        pnj = familier.pnj
        personnage.agir("ingerer")
        salle = personnage.salle

        # On regarde si il n'y a pas une fontaine dans les détails
        fontaine = salle.a_detail_flag("fontaine")
        peut = importeur.hook["objet:peut_boire"].executer(personnage)
        if any(peut) or fontaine or salle.terrain.nom in ("rive",
                "aquatique", "subaquatique"):
            if familier.soif > 2:
                pnj << "Vous buvez à grands traits."
                pnj.salle.envoyer("{} boit à grands traits.", pnj)
                familier.diminuer_soif(25)
            else:
                personnage.envoyer("{} ne peut boire davantage.", pnj)
        else:
            personnage << "|err|Il n'y a pas d'eau potable par ici.|ff|"
