# -*-coding:Utf-8 -*

# Copyright (c) 2014 LE GOFF Vincent
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


"""Fichier contenant le paramètre 'vendre' de la commande 'chantier'."""

from primaires.commerce.transaction import *
from primaires.interpreteur.masque.parametre import Parametre
from secondaires.navigation.constantes import *

class PrmVendre(Parametre):

    """Commande 'chantier vendre'.

    """

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "vendre", "sell")
        self.schema = "<nombre>"
        self.aide_courte = "vend un navire"
        self.aide_longue = \
            "Cette commande vous permet de vendre un navire à un " \
            "chantier navale. Vous devez préciser le numéro du navire " \
            "à vendre tel qu'indiqué dans %chantier% %chantier:liste%. " \
            "Le navire doit être vidé (et réparé). Si il reste des " \
            "matelots présents, la transaction sera annulée. Si il " \
            "reste des choses en cale elles seront tout simplement perdues."

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        nombre = dic_masques["nombre"].nombre
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
        vendeur = magasin.vendeur
        if vendeur is None:
            personnage << "|err|Aucun vendeur n'est présent pour l'instant.|ff|"
            return

        navires = chantier.get_navires_possedes(personnage)
        try:
            navire = navires[nombre - 1]
        except IndexError:
            personnage << "|err|Numéro de navire introuvable.|ff|"
            return

        prix = 0
        for n_salle in navire.salles.values():
            if n_salle.noyable and n_salle.voie_eau != COQUE_INTACTE:
                if n_salle.voie_eau == COQUE_COLMATEE:
                    prix += 25
                else:
                    prix += 40

        if len(navire.personnages) > 0:
            personnage << "|err|l y a toujours des matelots à bord.|ff|"
            return

        prix = int(navire.modele.m_valeur / 2) - prix
        if prix <= 0:
            personnage << "|err|En l'état, ce navire ne vaut rien.|ff|"
            return

        # Essaye de payer
        personnage << "{} vous dit : je payerai {} pièces de " \
                "bronze.".format(vendeur.nom_singulier.capitalize(), prix)

        transaction = Transaction.initier(personnage, magasin, -prix)

        personnage << "Vous vendez {}.".format(navire.desc_survol)
        importeur.navigation.supprimer_navire(navire.cle)

        # On prélève l'argent
        transaction.payer()
