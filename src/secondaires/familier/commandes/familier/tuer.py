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
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT master OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""Fichier contenant le paramètre 'tuer' de la commande 'familier'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmTuer(Parametre):

    """Commande 'familier tuer'."""

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "tuer", "kill")
        self.schema = "<nom_familier> <personnage_present>"
        self.aide_courte = "ordonne au familier d'attaquer"
        self.aide_longue = \
            "Cette commande permet d'ordonner à un familier d'attaquer " \
            "un personnage présent dans la salle où vous vous trouvez. " \
            "Le familier ne voudra pas attaquer son propre maître."

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        # On récupère le familier
        familier = dic_masques["nom_familier"].familier
        cible = dic_masques["personnage_present"].personnage
        pnj = familier.pnj
        if cible is personnage:
            personnage.envoyer("|err|{} refuse de vous attaquer.|ff|", pnj)
            return

        if cible is pnj:
            personnage.envoyer("{} ne peut s'attaquer lui-même !", pnj)
            return

        personnage.envoyer("Vous donnez un ordre à {}", pnj)
        familier.attaquer(cible)
