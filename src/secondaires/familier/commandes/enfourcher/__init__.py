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
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""Package contenant la commande 'enfourcher'."""

from primaires.interpreteur.commande.commande import Commande

class CmdEnfourcher(Commande):

    """Commande 'enfourcher'"""

    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "enfourcher", "ride")
        self.nom_categorie = "familier"
        self.schema = "(<personnage_present>)"
        self.aide_courte = "enfourche une monture"
        self.aide_longue = \
            "Cette commande permet d'enfourcher une monture qui se trouve " \
            "dans la même salle. Vous devez préciser son nom, celui " \
            "que vous utilisez pour donner des ordres à cette monture. " \
            "Une fois à dos de monture, vous pouvez utiliser les " \
            "commandes de déplacement standard : les montures ne peuvent " \
            "pas aller dans tous les endroits auquel vous pouvez " \
            "normalement accéder, mais si elles le peuvent, elles " \
            "consommeront l'endurance à votre place. Pour redescendre " \
            "sur terre, utilisez la commande %enfourcher% de nouveau, " \
            "sans paramètre."

    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        salle = personnage.salle
        familier = None

        if dic_masques["personnage_present"]:
            pnj = dic_masques["personnage_present"].personnage
            identifiant = getattr(pnj, "identifiant", "")
            try:
                familier = importeur.familier.familiers[identifiant]
            except KeyError:
                personnage.envoyer("|err|Vous ne pouvez enfourcher {}.|ff|",
                        pnj)
                return

        if "chevauche" in personnage.etats:
            familier = personnage.etats.get("chevauche").monture
            pnj = familier.pnj
            personnage.etats.retirer("chevauche")
            familier.chevauche_par = None
            personnage.envoyer_lisser("Vous descendez du dos de {}.", pnj)
            personnage.salle.envoyer("{} descend du dos de {}.", personnage,
                    pnj)
            return

        if familier is None:
            personnage << "|err|Vous devez préciser le nom d'une monture.|ff|"
            return

        if familier.maitre is not personnage:
            personnage.envoyer("|err|{} ne vous appartient pas.|ff|", pnj)
            return

        if not familier.fiche.monture:
            personnage.envoyer("|err|{} n'est pas une monture.|ff|", pnj)
            return

        if familier.chevauche_par:
            personnage << "|err|Il y a déjà quelqu'un en croupe.|ff|"
            return

        if any(aff.affection.a_flag("ne peut chevaucher") for aff in \
                personnage.affections.values()):
            personnage << "|err|Vous ne pouvez faire cela.|ff|"
            return

        personnage.etats.ajouter("chevauche", familier)
        familier.chevauche_par = personnage
        personnage.envoyer("Vous enfourchez {}.", pnj)
        personnage.salle.envoyer("{} enfourche {}.", personnage, pnj)
