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
# ARE DISCLAIMED. IN NO Etags SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""Package contenant la commande 'tags' et ses sous-commandes.

Dans ce fichier se trouve la commande même.

"""

from primaires.interpreteur.commande.commande import Commande
from secondaires.tags.commandes.tags.creer import PrmCreer
from secondaires.tags.commandes.tags.liste import PrmListe
from secondaires.tags.commandes.tags.script import PrmScript

class CmdTags(Commande):

    """Commande 'tags'."""

    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "tags", "tags")
        self.nom_categorie = "batisseur"
        self.groupe = "administrateur"
        self.aide_courte = "manipulation des tag"
        self.aide_longue = \
            "Les tags sont des sortes d'étiquettes que l'on peut " \
            "placer sur différentes structures de l'univers, comme " \
            "des PNJ ou objets. Ces étiquettes permettent de regrouper " \
            "des fonctionnalités. Par exemple, tous les PNJ vendeur " \
            "dans des magasins pourraient partager le même tag, " \
            "'vendeur' par exemple. Ceci pourrait simplifier la " \
            "recherche dans certains cas. Mais les tags permettent " \
            "aussi de copier rapidement des fonctionnalités grâce au " \
            "scripting. Par exemple, créer le tag de PNJ 'vendeur' " \
            "et lui dire de récupérer les scripts depuis un vendeur " \
            "PNJ déjà défini suffirait : si un autre PNJ vendeur " \
            "est créé, il suffira de lui donner le tag 'vendeur' et " \
            "il copiera ses scripts depuis le tag, ce qui permet de " \
            "copier rapidement des fonctionnalités."

    def ajouter_parametres(self):
        """Ajout des paramètres"""
        self.ajouter_parametre(PrmCreer())
        self.ajouter_parametre(PrmListe())
        self.ajouter_parametre(PrmScript())
