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
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""Package contenant le paramètre 'actuelles' de la commande 'louer'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmActuelles(Parametre):

    """Commande 'louer actuelles'"""

    def __init__(self):
        """Constructeur du paramètre."""
        Parametre.__init__(self, "actuelles", "current")
        self.tronquer = True
        self.aide_courte = "affiche vos locations"
        self.aide_longue = \
            "Cette commande vous permet de consulter la liste des " \
            "chambres que vous louez actuellement ainsi que la durée " \
            "restante avant l'expiration de la location, pour chacune. " \
            "Notez que le temps restant est spécifié en temps réel " \
            "(pas en temps Vancéen)."

    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        chambres = []
        for auberge in sorted(importeur.auberge.auberges.values(),
                key=lambda a: a.titre):
            for chambre in sorted(auberge.chambres.values(),
                    key=lambda c: c.numero):
                if not chambre.expiree and chambre.proprietaire is personnage:
                    chambres.append(chambre)

        if not chambres:
            personnage << "Vous ne louez aucune chambre pour l'instant."
            return

        en_tete = "+-" + "-" * 22 + "-+-" + "-" * 6 + "-+-" + "-" * 10 + "-+"
        msg = en_tete + "\n"
        msg += "| Auberge                | Numéro | Temps      |\n"
        msg += en_tete
        for chambre in chambres:
            msg += "\n| " + chambre.auberge.titre.ljust(22)
            msg += " | " + chambre.numero.ljust(6) + " | "
            msg += chambre.aff_temps.ljust(10) + " |"

        msg += "\n" + en_tete
        personnage << msg
