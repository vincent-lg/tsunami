# -*-coding:Utf-8 -*

# Copyright (c) 2014 LE GOFF Vincent
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
# ARE DISCLAIMED. IN NO Ediligence SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""Package contenant la commande 'diligence' et ses sous-commandes.

Dans ce fichier se trouve la commande même.

"""

from primaires.interpreteur.commande.commande import Commande
from secondaires.diligence.commandes.diligence.apparaitre import PrmApparaitre
from secondaires.diligence.commandes.diligence.creer import PrmCreer
from secondaires.diligence.commandes.diligence.deplacer import PrmDeplacer
from secondaires.diligence.commandes.diligence.editer import PrmEditer
from secondaires.diligence.commandes.diligence.liste import PrmListe

class CmdDiligence(Commande):

    """Commande 'diligence'."""

    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "diligence", "stagecoach")
        self.groupe = "administrateur"
        self.nom_categorie = "batisseur"
        self.aide_courte = "manipulation les diligences maudites"
        self.aide_longue = \
            "Cette commande permet de manipuler les diligences maudites. " \
            "Les diligences maudites sont des formes de zones " \
            "semi-aléatoires qui peuvent être créées sur des modèles. " \
            "Cette commande particulière permet de créer, éditer et " \
            "lister les diligences maudites existantes. Le principe " \
            "de ce type de zone est qu'on doit créer d'abord sa zone " \
            "modèle. La commande %diligence% %diligenc:créer% crée " \
            "une nouvelle zone dans laquelle on peut se déplacer, éditer " \
            "le titre, la description, les détails et scripts, ajouter " \
            "des salles et des sortis pour faire une zone de " \
            "nombreuses salles. Au moment où une véritable diligence " \
            "est créée, toutes les salles du modèle sont copiées. " \
            "La zone copiée est rendue accessible aux joueurs grâce " \
            "à une sortie. La zone modèle ne sera pas modifiée et " \
            "l'on peut créer autant de zones copiées que l'on veut. " \
            "La commande %diligence% %diligence:créer% ou " \
            "%diligence% %diligence:éditer% ouvre un éditeur de " \
            "manipulation propre à la diligence en général, mais " \
            "la plupart de l'édition se fait de façon standard, " \
            "comme une zone simple."

    def ajouter_parametres(self):
        """Ajout des paramètres"""
        self.ajouter_parametre(PrmApparaitre())
        self.ajouter_parametre(PrmCreer())
        self.ajouter_parametre(PrmDeplacer())
        self.ajouter_parametre(PrmEditer())
        self.ajouter_parametre(PrmListe())
