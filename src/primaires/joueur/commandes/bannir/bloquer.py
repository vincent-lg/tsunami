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


"""Fichier contenant le paramètre 'bloquer' de la commande 'bannir'."""

from datetime import datetime, timedelta

from primaires.interpreteur.masque.parametre import Parametre

class PrmBloquer(Parametre):

    """Commande 'bannir bloquer'.

    """

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "bloquer", "block")
        self.schema = "<nom_joueur> pour/for <duree>"
        self.aide_courte = "bloque temporérement un joueur"
        self.aide_longue = \
            "Cette commande permet de bannir temporairement un joueur. " \
            "La durée doit être précisée après le mot-clé |cmd|pour|ff| " \
            "en français ou |cmd|for|ff| en anglais. Elle est " \
            "constituée d'une partie entière et d'une unité : |cmd|m|ff| " \
            "pour minute, |cmd|h|ff| pour heure et |cmd|j|ff| pour " \
            "jour. Par exemple, |cmd|5j|ff| veut dire 5 jours."

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        joueur = dic_masques["nom_joueur"].joueur
        secondes = dic_masques["duree"].secondes
        temps = dic_masques["duree"].temps
        maintenant = datetime.now()
        difference = timedelta(seconds=secondes)

        if joueur.est_immortel():
            personnage << "|err|Vous ne pouvez bannir un administrateur.|ff|"
            return

        if joueur in importeur.connex.joueurs_bannis:
            del importeur.connex.joueurs_bannis

        if joueur.est_connecte():
            joueur.envoyer("|rg|VOUS ÊTES BANNI DU SERVEUR POUR {}." \
                    "|ff|".format(temps.upper()))
            joueur.instance_connexion.deconnecter("Bannissement temporaire")

        date = maintenant + difference
        importeur.connex.bannissements_temporaires[joueur] = date
        personnage << "|att|Vous bannissez {} pour {}.|ff|".format(
                joueur.nom, temps)
