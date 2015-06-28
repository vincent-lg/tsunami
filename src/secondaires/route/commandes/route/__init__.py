# -*-coding:Utf-8 -*

# Copyright (c) 2015 LE GOFF Vincent
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


"""Package contenant la commande 'route'."""

from primaires.interpreteur.commande.commande import Commande
from secondaires.route.commandes.route.liste import PrmListe
from secondaires.route.commandes.route.marquer import PrmMarquer
from secondaires.route.commandes.route.trouver import PrmTrouver
from secondaires.route.commandes.route.voir import PrmVoir

# Constantes
AIDE = """
Cette commande permet de manipuler les routes. Les routes dans
Vancia forment une sorte de complexe, une carte avec différents
points et différents chemins pour mener de l'un à l'autre. Pour
ajouter une route, il suffit d'utiliser la commande %route%
%route:marquer% dans la salle que vous voulez comme point de départ
de la route. Déplacez-vous ensuite normalement (en empruntant les
sorties) tout au long de la route. Une fois dans la salle finale de
la route, entrez de nouveau %route% %route:marquer%. La route menant
de l'origine à la destination sera inscrite comme route empruntable
avec la suite des salles et sorties que vous avez empruntées. La
route inverse sera également renseignée.

Une fois la route (ou les routes) ajoutées, vous pouvez utiliser
la commande %route% %route:trouver% pour chercher le chemin le plus
court entre deux salles définies dans les routes : ce système
permet aussi de vérifier la solution de continuité dans le chemin
trouvé par le système.
""".strip()

class CmdRoute(Commande):

    """Commande 'route'"""

    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "route", "road")
        self.groupe = "administrateur"
        self.nom_categorie = "batisseur"
        self.aide_courte = "manipule les routes"
        self.aide_longue = AIDE

    def ajouter_parametres(self):
        """Ajout des paramètres."""
        self.ajouter_parametre(PrmListe())
        self.ajouter_parametre(PrmMarquer())
        self.ajouter_parametre(PrmTrouver())
        self.ajouter_parametre(PrmVoir())
