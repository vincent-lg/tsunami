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


"""Package contenant le paramètre 'renouveler' de la commande 'louer'."""

from datetime import datetime, timedelta

from primaires.commerce.transaction import *
from primaires.interpreteur.masque.parametre import Parametre
from secondaires.auberge.chambre import MAX_NB_JOURS

class PrmRenouveler(Parametre):

    """Commande 'louer renouveler'"""

    def __init__(self):
        """Constructeur du paramètre."""
        Parametre.__init__(self, "renouveler", "renew")
        self.tronquer = True
        self.schema = "<chambre_auberge> <nombre>"
        self.aide_courte = "renouvelle une location"
        self.aide_longue = \
            "Cette commande vous permet de renouveler le loyer d'une " \
            "chambre que vous louez déjà. Si vous arrivez à la fin de " \
            "la période d'expiration de la location, vous pouvez " \
            "utiliser cette commande pour conserver la chambre plus " \
            "longtemps. Vous ne pouvez utiliser cette commande pour " \
            "dépasser le nombre de jours maximum (fixée à dix jours). " \
            "La syntaxe de cette commande est la même que %louer% " \
            "%louer:chambre%, vous devez préciser le numéro de la " \
            "chambre en premier paramètre et la durée (en jours réels) " \
            "de location souhaitée. La nouvelle durée sera ajoutée à " \
            "celle restante et le prix que vous devrez payer sera le " \
            "même que si vous vouliez louer cette chambre sans l'avoir " \
            "déjà louée auparavant. Vous pouvez donc utiliser la " \
            "commande %louer% %louer:valeur% pour estimer le prix " \
            "nécessaire à un prolongement de la durée de location."

    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        chambre = dic_masques["chambre_auberge"].chambre
        auberge = chambre.auberge
        nombre = dic_masques["nombre"].nombre
        if auberge.aubergiste is None:
            personnage << "|err|Aucun aubergiste n'est présent pour " \
                    "s'en charger.|ff|"
            return

        if chambre.proprietaire is not personnage or chambre.expire_a is None:
            personnage << "|err|Vous ne louez pas cette chambre.|ff|"
            return

        delta = chambre.expire_a - datetime.now()
        n_delta = delta + timedelta(days=nombre)
        if n_delta.days > 30:
            personnage << "|err|Vous ne pouvez réserver autant de jours.|ff|"
            return
        elif personnage not in importeur.auberge.vacances:
            pass
        elif n_delta.days > MAX_NB_JOURS:
            personnage << "|err|Vous ne pouvez réserver autant de jours.|ff|"
            return

        valeur = chambre.prix(nombre)

        # On crée la transaction associée
        try:
            transaction = Transaction.initier(personnage, auberge, valeur)
        except FondsInsuffisants:
            personnage << "|err|Vous n'avez pas assez d'argent.|ff|"
            return

        # On prélève l'argent
        transaction.payer()

        if nombre > MAX_NB_JOURS:
            auberge.vacances.append(personnage)

        # On rend le personnage propriétaire
        chambre.expire_a = datetime.now() + n_delta
        s = "s" if nombre > 1 else ""
        personnage << "Vous prolongez la location de la chambre '{}' " \
                "pour {} jour{s}.".format(chambre.numero, nombre, s=s)
