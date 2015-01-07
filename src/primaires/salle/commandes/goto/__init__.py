# -*-coding:Utf-8 -*

# Copyright (c) 2010 LE GOFF Vincent
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


"""Package contenant la commande 'goto'."""

from primaires.interpreteur.commande.commande import Commande

class CmdGoto(Commande):

    """Commande 'goto'"""

    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "goto", "goto")
        self.groupe = "administrateur"
        self.schema = "<identifiant:ident_salle|nom_joueur>"
        self.nom_categorie = "bouger"
        self.aide_courte = "permet de se déplacer dans l'univers"
        self.aide_longue = \
            "Cette commande vous permet de vous déplacer rapidement dans " \
            "l'univers. Vous pouvez lui passer en paramètre l'identifiant " \
            "d'une salle sous la forme |cmd|zone:mnémonique|ff|, " \
            "par exemple |ent|picte:1|ff|, ou alors un nom de joueur. " \
            "Exemple : %goto% |ent|nom_du_joueur|ff|."

    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        masque = dic_masques["identifiant"]
        if hasattr(masque, "salle"):
            salle = masque.salle
        elif hasattr(masque, "joueur"):
            salle = masque.joueur.salle
        else:
            raise ValueError(
                    "le masque {} est invalide pour cette commande".format(
                    masque))

        salle_courante = personnage.salle
        salle_courante.envoyer("{} disparaît avec un éclair de " \
                "|cyc|lumière bleue|ff|.", personnage)
        personnage.salle = salle
        personnage << personnage.salle.regarder(personnage)
        salle.envoyer("{} apparaît avec un éclair de |cyc|lumière " \
                "bleue|ff|.", personnage)
        importeur.hook["personnage:deplacer"].executer(
                personnage, salle, None, 0)
