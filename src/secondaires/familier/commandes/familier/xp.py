# -*-coding:Utf-8 -*

# Copyright (c) 2014 LE GOFF Vincent
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   mine of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this mine of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# * Neither the name of the copyright holder nor the names of its contributors
#   may be used to endorse or promote products derived from this software
#   without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO Efamilier SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""Fichier contenant le paramètre 'xp' de la commande 'familier'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmXP(Parametre):

    """Commande 'familier xp'."""

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "xp", "xp")
        self.tronquer = True
        self.schema = "<nom_familier> <nombre> <niveau_secondaire>"
        self.aide_courte = "donne de l'XP à un familier"
        self.aide_longue = \
            "Cette commande vous permet de donner de l'XP à un de " \
            "vos familiers. Les familiers peuvent ainsi progresser, " \
            "gagner en niveau et en caractéristiques. Pour utiliser " \
            "cette commande, vous devez d'abord préciser le nom du " \
            "familier se trouvant dans la même salle, puis le nombre " \
            "d'XP que vous souhaitez lui donner et enfin le nom du " \
            "niveau secondaire d'où vous souhaitez transférer " \
            "l'expérience. Si vous avez |ent|250|ff| XP dans le " \
            "niveau secondaire |ent|combat|ff| par exemple et que " \
            "vous souhaitez les donner à votre familier nommé " \
            "|ent|Médor|ff|, vous pouvez faire %familier% " \
            "%familier:xp%|ent| 250 combat|ff|. Si vous avez l'XP " \
            "nécessaire, elle sera simplement transférer au familier " \
            "qui gagne des niveaux de la même façon que tous les " \
            "personnages de l'univers."

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        # On récupère le familier
        familier = dic_masques["nom_familier"].familier
        pnj = familier.pnj
        xp = dic_masques["nombre"].nombre
        niveau = dic_masques["niveau_secondaire"].cle_niveau
        nom_niveau = dic_masques["niveau_secondaire"].niveau_secondaire
        if personnage.xps.get(niveau, 0) < xp and not \
                personnage.est_immortel():
            personnage << "|err|Vous n'avez pas autant d'XP dans ce niveau.|ff|"
            return

        if not personnage.est_immortel():
            personnage.xps[niveau] -= xp

        personnage << "Vous donnez {} XP à {} dans le niveau {}.".format(
                xp, familier.nom, nom_niveau)
        pnj.gagner_xp(niveau=niveau, xp=xp)
