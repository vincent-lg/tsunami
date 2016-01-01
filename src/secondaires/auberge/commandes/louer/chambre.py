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


"""Package contenant le paramètre 'chambre' de la commande 'louer'."""

from datetime import datetime, timedelta

from primaires.commerce.transaction import *
from primaires.interpreteur.masque.parametre import Parametre
from secondaires.auberge.chambre import MAX_NB_JOURS

class PrmChambre(Parametre):

    """Commande 'louer chambre'"""

    def __init__(self):
        """Constructeur du paramètre."""
        Parametre.__init__(self, "chambre", "room")
        self.tronquer = True
        self.schema = "<chambre_auberge> <nombre>"
        self.aide_courte = "loue une chambre"
        self.aide_longue = \
            "Cette commande vous permet de louer une chambre. Vous " \
            "devez vous trouver auprès d'un aubergiste pour ce faire. " \
            "Le premier paramètre à préciser est le numéro de la chambre " \
            "à louer (vous pouvez obtenir cette information à l'aide " \
            "de la commande %louer% %louer:liste%). Le second paramètre " \
            "est le nombre de jours (réels) pour lesquels vous voulez " \
            "louer cette chambre. Vous pouvez louer une chambre pour " \
            "un jour minimum et dix jours au maximum : vous avez " \
            "cependant la possibilité de renouveler une location qui " \
            "n'a pas encore expirée à l'aide de la commande %louer% " \
            "%louer:renouveler%."

    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        chambre = dic_masques["chambre_auberge"].chambre
        auberge = chambre.auberge
        nombre = dic_masques["nombre"].nombre
        if auberge.aubergiste is None:
            personnage << "|err|Aucun aubergiste n'est présent pour " \
                    "s'en charger.|ff|"
            return

        if chambre.proprietaire is personnage:
            personnage << "|err|Vous louez déjà cette chambre.|ff|"
            return

        if chambre.proprietaire is not None:
            personnage << "|err|Cette chambre est déjà louée.|ff|"
            return

        if nombre > MAX_NB_JOURS:
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

        # On rend le personnage propriétaire
        chambre.proprietaire = personnage
        duree = timedelta(days=nombre)
        chambre.expire_a = datetime.now() + duree
        s = "s" if nombre > 1 else ""
        personnage << "Vous louez la chambre '{}' pour {} jour{s}.".format(
                chambre.numero, nombre, s=s)
