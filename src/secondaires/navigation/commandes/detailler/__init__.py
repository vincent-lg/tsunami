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


"""Package contenant la commande 'détailler'."""

from primaires.interpreteur.commande.commande import Commande
from secondaires.navigation.visible import Visible

class CmdDetailler(Commande):

    """Commande 'détailler'"""

    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "détailler", "detail")
        self.nom_categorie = "navire"
        self.schema = "<point_visible>"
        self.aide_courte = "affiche les détails de l'étendue d'eau"
        self.aide_longue = \
            "Cette commande permet à un navigateur de connaître les " \
            "détails qui l'entourent. Sans paramètre, cette commande " \
            "affiche les côtes, ports, navires visibles sur l'étendue. " \
            "Vous pouvez préciser en paramètre un point à détailler " \
            "plus particulièrement sous la forme d'une direction, comme " \
            "|cmd|arrière|ff|, |cmd|bâbord|ff|, |cmd|tribord|ff| ou " \
            "|cmd|avant|ff|. Vous verrez alors dans un champ plus " \
            "restreint mais aussi plus détaillé."

    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        salle = personnage.salle
        if not hasattr(salle, "navire") or salle.navire is None:
            personnage << "|err|Vous n'êtes pas sur un navire.|ff|"
            return

        navire = salle.navire
        etendue = navire.etendue
        if salle.interieur:
            personnage << "|err|Vous ne pouvez rien voir d'ici.|ff|"
            return

        msg = dic_masques["point_visible"].retour
        if msg:
            personnage << msg
        else:
            personnage << "Rien n'est en vue auprès de vous."
