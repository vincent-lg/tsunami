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


"""Package contenant la commande 'paix'.

"""

from primaires.interpreteur.commande.commande import Commande

class CmdPaix(Commande):

    """Commande 'paix'.

    """

    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "paix", "peace")
        self.schema = "(<ident_salle>)"
        self.groupe = "administrateur"
        self.nom_categorie = "combat"
        self.aide_courte = "supprime le combat dans une salle"
        self.aide_longue = \
            "Cette commande supprime le combat dans une salle. Sans " \
            "paramètres, la salle est celle où vous vous trouvez, mais " \
            "vous pouvez aussi préciser une salle (sous la forme " \
            "|ent|zone:mnémonique|ff|)."

    def interpreter(self, personnage, dic_masques):
        """Interprétation de la commande"""
        if dic_masques["ident_salle"]:
            salle = dic_masques["ident_salle"].salle
        else:
            salle = personnage.salle

        if salle.ident not in importeur.combat.combats:
            personnage << "|err|Aucun combat n'existe dans cette salle.|ff|"
            return

        importeur.combat.supprimer_combat(salle.ident)
        personnage << "|att|Le combat a été interrompu en salle " \
                "'{}'|ff|.".format(salle.ident)
