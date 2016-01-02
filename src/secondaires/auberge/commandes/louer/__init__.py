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
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""Package contenant la commande 'louer'."""

from primaires.interpreteur.commande.commande import Commande
from .actuelles import PrmActuelles
from .chambre import PrmChambre
from .liste import PrmListe
from .renouveler import PrmRenouveler
from .valeur import PrmValeur

class CmdLouer(Commande):

    """Commande 'louer'"""

    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "louer", "rent")
        self.aide_courte = "loue une chambre d'auberge"
        self.aide_longue = \
            "Cette commande permet d'interagir avec les auberges pour " \
            "louer ou renouveler une chambre ainsi que consulter la " \
            "liste des chambres à louer. Pour utiliser ces trois " \
            "commandes, vous devez vous trouver dans le lieu assigné à " \
            "une auberge (l'aubergiste doit être présent). Vous " \
            "pouvez également consulter la liste des chambres que vous " \
            "louez actuellement ainsi que la durée de location restante " \
            "avant l'expiration de votre location. Le locataire d'une " \
            "chambre aura la faculté d'ouvrir et de refermer la porte " \
            "de sa location (les autres joueurs ou PNJ en seront " \
            "incapables). Il pourra recevoir, cependant, tant qu'il " \
            "laisse la porte ouverte. Les possessions laissées dans les " \
            "coffres mis à disposition dans certaines chambres obéissent " \
            "aux mêmes règles que celles conservées dans le reste de " \
            "l'univers : elles sont plus en séc urité, puisque vous " \
            "devriez être le seul à pouvoir entrer dans votre chambre, " \
            "mais n'oubliez pas de la renouveler avant que la location " \
            "n'arrive à son terme. Si un autre joueur loue la chambre " \
            "que vous occupiez, il pourra voler les objets laissés " \
            "dans vos coffres sans contrainte."

    def ajouter_parametres(self):
        """Ajout des paramètres."""
        self.ajouter_parametre(PrmActuelles())
        self.ajouter_parametre(PrmChambre())
        self.ajouter_parametre(PrmListe())
        self.ajouter_parametre(PrmRenouveler())
        self.ajouter_parametre(PrmValeur())
