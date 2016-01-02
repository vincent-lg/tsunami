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


"""Package contenant la commande 'chemin'."""

from primaires.interpreteur.commande.commande import Commande
from .creer import PrmCreer
from .etendre import PrmEtendre
from .liste import PrmListe
from .supprimer import PrmSupprimer
from .voir import PrmVoir

class CmdChemin(Commande):

    """Commande 'chemin'"""

    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "chemin", "path")
        self.groupe = "administrateur"
        self.nom_categorie = "batisseur"
        self.aide_courte = "manipule les chemins pour PNJ"
        self.aide_longue = \
            "Cette commande permet de créer, lister, supprimer et " \
            "configurer les chemins pour PNJ. Un chemin est constitué " \
            "d'une suite de salle : vous devez d'abord le créez. Ayez " \
            "conscience qu'en utilisant la commande %chemin% " \
            "%chemin:créer%, vous marquerez le point de départ du " \
            "chemin dans la salle où vous vous trouvez. Vous devrez " \
            "ensuite utiliser la commande %chemin% %chemin:étendre% " \
            "pour ajouter des salles au chemin. Si votre chemin doit " \
            "être circulaire (c'est-à-dire qu'un PNJ l'empruntant " \
            "reviendra à son point de départ à la fin du chemin), n'oubliez " \
            "pas de faire en sorte que la destination du chemin soit son " \
            "origine."

    def ajouter_parametres(self):
        """Ajout des paramètres."""
        self.ajouter_parametre(PrmCreer())
        self.ajouter_parametre(PrmEtendre())
        self.ajouter_parametre(PrmListe())
        self.ajouter_parametre(PrmSupprimer())
        self.ajouter_parametre(PrmVoir())
