# -*-coding:Utf-8 -*

# Copyright (c) 2013 LE GOFF Vincent
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
# ARE DISCLAIMED. IN NO Ematelot SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""Fichier contenant le paramètre 'promouvoir' de la commande 'matelot'."""

from corps.fonctions import lisser
from primaires.format.fonctions import supprimer_accents
from primaires.interpreteur.masque.parametre import Parametre
from secondaires.navigation.equipage.postes.hierarchie import ORDRE

class PrmPromouvoir(Parametre):

    """Commande 'matelot promouvoir'."""

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "promouvoir", "promote")
        self.schema = "<nom_joueur> <message>"
        self.tronquer = True
        self.aide_courte = "promeut un joueur dans votre équipage"
        self.aide_longue = \
            "Cette commande est assez identique à %matelot% " \
            "%matelot:poste% sauf qu'elle permet de changer le poste " \
            "d'un joueur. Les joueurs sont libres de leurs actions " \
            ": ils entendent les ordres et, certaines fois, ils " \
            "peuvent les accomplir, mais ils n'y sont pas forcés. " \
            "L'avantage de cette commande est surtout d'indiquer " \
            "d'autres officiers : les postes |ent|officier|ff|, " \
            "|ent|maître d'équipage|ff|, |ent|second|ff| et " \
            "|ent|capitaine|ff| ont des privilèges particuliers, " \
            "comme celui de pouvoir donner des ordres sur le navire. " \
            "En outre, seuls le capitaine et son second (il peut y " \
            "avoir plusieurs capitaines ou seconds) ont le droit " \
            "d'ordonner de larguer les amarres ou de lever l'ancre. " \
            "Enfin, si un équipage est placé pour réceptionner un " \
            "abordage, les matelots ayant pour tâche de protéger le " \
            "navire attaqueront les membres d'un équipage adverse : " \
            "ils ne s'attaqueront pas entre eux, faisant parti du " \
            "même équipage, et ils n'attaqueront pas les joueurs " \
            "définis dans le même équipage, mais tous les autres " \
            "(PNJ ou joueurs) seront pris pour cible. Si vous oubliez " \
            "d'inclure un joueur dans votre équipage à ce moment, il " \
            "sera considéré comme un ennemi. Pour manipuler cette " \
            "commande, entrez en premier paramètre le nom du joueur " \
            "(celui visible dans la commande %qui%, pas sa " \
            "distinction anonyme) et en second paramètre le poste " \
            "auquel vous voulez l'assigner, ou |ent|aucun|ff| si " \
            "vous voulez retirer ce joueur de votre équipage. Les postes " \
            "disponibles sont : " + ", ".join(ORDRE) + "."

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        salle = personnage.salle
        if getattr(salle, "navire", None) is None:
            personnage << "|err|Vous n'êtes pas sur un navire.|ff|"
            return

        navire = salle.navire
        joueur = dic_masques["nom_joueur"].joueur
        nom_poste = dic_masques["message"].message.lower()
        equipage = navire.equipage

        if not navire.a_le_droit(personnage, "maître d'équipage"):
            personnage << "|err|Vous ne pouvez donner d'ordre sur ce " \
                    "navire.|ff|"
            return

        if nom_poste == "aucun":
            if joueur in equipage.joueurs:
                del equipage.joueurs[joueur]
                personnage << "{} a bien été retiré de votre " \
                        "équipage.".format(joueur.nom)
            else:
                personnage << "|err|Le joueur {} n'est pas dans " \
                        "votre équipage.|ff|".format(joueur.nom)
            return

        # On essaye de trouver le nom du poste (sans accents ni majuscules)
        nom = None
        for t_nom in ORDRE:
            if supprimer_accents(t_nom).lower() == supprimer_accents(
                    nom_poste):
                nom = t_nom
                break

        if nom is None:
            personnage << "|err|Impossible de trouver le nom du poste : " \
                    "{}.|ff|".format(nom_poste)
        else:
            equipage.changer_poste(joueur, nom)
            personnage << lisser("{} a bien été mis au poste de {}.".format(
                    joueur.nom, nom))
