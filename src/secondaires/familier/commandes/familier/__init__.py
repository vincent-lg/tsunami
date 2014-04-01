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
# ARE DISCLAIMED. IN NO Efamilier SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""Package contenant la commande 'familier' et ses sous-commandes.

Dans ce fichier se trouve la commande même.

"""

from primaires.interpreteur.commande.commande import Commande
from secondaires.familier.commandes.familier.apparaitre import PrmApparaitre
from secondaires.familier.commandes.familier.attacher import PrmAttacher
from secondaires.familier.commandes.familier.brouter import PrmBrouter
from secondaires.familier.commandes.familier.chasser import PrmChasser
from secondaires.familier.commandes.familier.creer import PrmCreer
from secondaires.familier.commandes.familier.deplacer import PrmDeplacer
from secondaires.familier.commandes.familier.detacher import PrmDetacher
from secondaires.familier.commandes.familier.editer import PrmEditer
from secondaires.familier.commandes.familier.emote import PrmEmote
from secondaires.familier.commandes.familier.harnacher import PrmHarnacher
from secondaires.familier.commandes.familier.liste import PrmListe
from secondaires.familier.commandes.familier.maitre import PrmMaitre
from secondaires.familier.commandes.familier.mener import PrmMener
from secondaires.familier.commandes.familier.miens import PrmMiens
from secondaires.familier.commandes.familier.niveaux import PrmNiveaux
from secondaires.familier.commandes.familier.nom import PrmNom
from secondaires.familier.commandes.familier.relacher import PrmRelacher
from secondaires.familier.commandes.familier.renommer import PrmRenommer
from secondaires.familier.commandes.familier.score import PrmScore
from secondaires.familier.commandes.familier.tuer import PrmTuer

class CmdFamilier(Commande):

    """Commande 'familier'."""

    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "familier", "pet")
        self.nom_categorie = "familier"
        self.aide_courte = "manipulation des familiers"
        self.aide_longue = \
            "Cette commande permet de manipuler les familiers. Les " \
            "familiers sont des personnages non-joueurs dont vous " \
            "êtes le maître. Ils peuvent être extrêmement différent : " \
            "certains peuvent servir de monture, d'autres d'aides pour " \
            "chasser, ainsi de suite. Consultez les sous-commandes pour " \
            "de l'aide plus spécifique."

    def ajouter_parametres(self):
        """Ajout des paramètres"""
        self.ajouter_parametre(PrmApparaitre())
        self.ajouter_parametre(PrmAttacher())
        self.ajouter_parametre(PrmBrouter())
        self.ajouter_parametre(PrmChasser())
        self.ajouter_parametre(PrmCreer())
        self.ajouter_parametre(PrmDeplacer())
        self.ajouter_parametre(PrmDetacher())
        self.ajouter_parametre(PrmEditer())
        self.ajouter_parametre(PrmEmote())
        self.ajouter_parametre(PrmHarnacher())
        self.ajouter_parametre(PrmListe())
        self.ajouter_parametre(PrmMaitre())
        self.ajouter_parametre(PrmMener())
        self.ajouter_parametre(PrmMiens())
        self.ajouter_parametre(PrmNiveaux())
        self.ajouter_parametre(PrmNom())
        self.ajouter_parametre(PrmRelacher())
        self.ajouter_parametre(PrmRenommer())
        self.ajouter_parametre(PrmScore())
        self.ajouter_parametre(PrmTuer())
