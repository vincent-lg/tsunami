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


"""Package contenant le paramètre 'valeur' de la commande 'louer'."""

from primaires.interpreteur.masque.parametre import Parametre
from secondaires.auberge.chambre import MAX_NB_JOURS

class PrmValeur(Parametre):

    """Commande 'louer valeur'"""

    def __init__(self):
        """Constructeur du paramètre."""
        Parametre.__init__(self, "valeur", "value")
        self.tronquer = True
        self.schema = "<chambre_auberge> <nombre>"
        self.aide_courte = "affiche le prix de location"
        self.aide_longue = \
            "Cette commande affiche le prix de location d'une chambre " \
            "d'auberge pour une durée précise. Pour l'utiliser, vous " \
            "devez vous trouver auprès d'un aubergiste. Le premier " \
            "paramètre est le numéro de la chambre, tel que vous le voyez " \
            "dans %louer% %louer:liste% ou %louer% %louer:actuelles%. " \
            "Le second paramètre est la durée en jour réels. Par " \
            "exemple : %louer% %louer:valeur%|ent| suite 5|ff| pour " \
            "obtenir le prix de la location de la suite pour cinq " \
            "jours."

    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        chambre = dic_masques["chambre_auberge"].chambre
        nombre = dic_masques["nombre"].nombre
        if nombre <= 0:
            personnage << "|err|Le nombre de jour précisé est négatif " \
                    "ou nul.|ff|"
            return

        if nombre > 30:
            personnage << "|err|Vous ne pouvez réserver autant de jours.|ff|"
            return
        elif personnage not in importeur.auberge.vacances:
            pass
        elif nombre > MAX_NB_JOURS:
            personnage << "|err|Vous ne pouvez réserver autant de jours.|ff|"
            return

        valeur = chambre.prix(nombre)
        s = "s" if valeur > 1 else ""
        personnage << "Il vous en coûtera {} pièce{s} de bronze.".format(
                valeur, s=s)
