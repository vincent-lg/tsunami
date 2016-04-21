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


"""Fichier contenant le paramètre 'liste' de la commande 'bannir'."""

from datetime import datetime

from primaires.interpreteur.masque.parametre import Parametre

class PrmListe(Parametre):

    """Commande 'bannir liste'.

    """

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "liste", "list")
        self.aide_courte = "liste les bannisements"
        self.aide_longue = \
            "Cette commande liste les bannissements actuels, " \
            "temporaires ou prolongés, de joueurs, comptes ou " \
            "adresses."

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        msg = "Bannissements actuels :\n"
        temporaires = []
        maintenant = datetime.now()
        for joueur, date in \
                importeur.connex.bannissements_temporaires.items():
            msg_temp = joueur.nom + " ("
            dans = (date - maintenant).total_seconds()
            mesure = "s"
            if maintenant > date or dans < 0:
                dans = 0
            elif dans >= 86400:
                dans //= 86400
                mesure = "j"
            elif dans >= 3600:
                dans //= 3600
                mesure = "h"
            elif dans >= 60:
                dans //= 60
                mesure = "m"

            msg_temp += str(int(dans)) + mesure + ")"
            temporaires.append(msg_temp)

        temporaires = ", ".join(temporaires)
        if not temporaires:
            temporaires = "|att|aucun|ff|"

        joueurs = ", ".join(j.nom for j in importeur.connex.joueurs_bannis)
        if not joueurs:
            joueurs = "|att|aucun|ff|"

        msg += "\n  Bannissements temporaires : " + temporaires
        msg += "\n  Bannissements de joueurs : " + joueurs
        personnage << msg
