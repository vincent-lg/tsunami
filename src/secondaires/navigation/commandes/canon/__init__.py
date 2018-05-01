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


"""Package contenant la commande 'canon'."""

from primaires.interpreteur.commande.commande import Commande

from .charger import PrmCharger
from .feu import PrmFeu
from .pivoter import PrmPivoter
from .poudre import PrmPoudre

class CmdCanon(Commande):

    """Commande 'canon'"""

    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "canon", "cannon")
        self.nom_categorie = "combat"
        self.aide_courte = "manipule un canon dans la salle"
        self.aide_longue = \
            "Cette commande vous permet de manipuler un canon présent " \
            "(sous la forme d'un élément de navire ou d'un objet) dans " \
            "la salle où vous vous trouvez. Vous pouvez le charger " \
            "en poudre et projectile, l'orienter et le faire détonner. " \
            "Utilisez pour ce faire les sous-commandes proposées."

    def ajouter_parametres(self):
        """Ajout des paramètres."""
        self.ajouter_parametre(PrmCharger())
        self.ajouter_parametre(PrmFeu())
        self.ajouter_parametre(PrmPivoter())
        self.ajouter_parametre(PrmPoudre())
