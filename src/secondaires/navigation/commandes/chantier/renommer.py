# -*-coding:Utf-8 -*

# Copyright (c) 2013 LE GOFF Vincent
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


"""Fichier contenant le paramètre 'renommer' de la commande 'chantier'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmRenommer(Parametre):

    """Commande 'chantier renommer'.

    """

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "renommer", "rename")
        self.schema = "<nombre> <message>"
        self.aide_courte = "renomme un navire"
        self.aide_longue = \
            "Cette commande vous permet de changer le nom d'un navire. " \
            "Celui-ci doit être dans le chantier naval où vous vous " \
            "trouvez. Vous devez préciser en premier paramètre le " \
            "numéro du navire (tel que la commande %chantier% " \
            "%chantier:liste% l'affiche) et en second paramètre le " \
            "nouveau nom du navire. Cette action n'est pas instantanée " \
            ": le navire doit rester dans le chantier naval quelques " \
            "minutes le temps que les ouvriers repeignent son nom sur " \
            "la coque. Vous pouvez voir le temps restant pour cette " \
            "opération en entrant %chantier% %chantier:commandes%."

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        nombre = dic_masques["nombre"].nombre
        nom = dic_masques["message"].message
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
        if magasin.vendeur is None:
            personnage << "|err|Aucun vendeur n'est présent pour l'instant.|ff|"
            return

        navires = chantier.get_navires_possedes(personnage)
        try:
            navire = navires[nombre - 1]
        except IndexError:
            personnage << "|err|Numéro de navire introuvable.|ff|"
            return

        chantier.ajouter_commande(personnage, navire, "renommer", 11, nom)
        personnage << "Votre requête a été envoyé au chantier naval."
