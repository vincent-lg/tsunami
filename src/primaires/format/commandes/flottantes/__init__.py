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


"""Package contenant la commande 'flottantes'."""

from primaires.interpreteur.commande.commande import Commande
from .creer import PrmCreer
from .editer import PrmEditer
from .liste import PrmListe
from .supprimer import PrmSupprimer

class CmdFlottantes(Commande):

    """Commande 'flottantes'"""

    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "flottantes", "floating")
        self.groupe = "administrateur"
        self.nom_categorie = "batisseur"
        self.aide_courte = "manipule les descriptions flottantes"
        self.aide_longue = \
            "Cette commande permet de créer, éditer, lister " \
            "et supprimer les descriptions flottantes. Les descriptions " \
            "flottantes sont des descriptions \"standards\" de l'univers, " \
            "mais à la différence de celles manipulées d'ordinaire " \
            "(descriptions d'objets, de salles, de PNJ), les descriptions " \
            "flottantes n'ont par défaut aucun lien avec l'univers. Pour les " \
            "utiliser, il faut les inclure dans une autre description. Créez " \
            "d'abord une description flottante avec une clé explicite (si il " \
            "s'agit d'une description de plusieurs salles, par exemple, " \
            "faites comme si c'était une clé de salle, le nom de la zone, " \
            "le signe deux points et un mnémonique imaginaire). Ensuite, dans " \
            "les descriptions où vous voulez importer cette description " \
            "flottante, utilisez l'abréviation " \
            "|cmd|@cle_de_la_description_flottante|ff|. Cette commande peut " \
            "se trouver dans un paragraphe isolé de la description ou au " \
            "milieu d'un paragraphe (veillez à être cohérent dans le " \
            "résultat attendu). Les descriptions dynamiques peuvent être " \
            "utilisées conjointement avec les descriptions flottantes, " \
            "consultez la documentation des descriptions dynamiques à " \
            "l'adresse " \
        "http://redmine.kassie.fr/projects/documentation/wiki/DescriptionDynamique " \
            "pour plus d'informations."

    def ajouter_parametres(self):
        """Ajout des paramètres."""
        self.ajouter_parametre(PrmCreer())
        self.ajouter_parametre(PrmEditer())
        self.ajouter_parametre(PrmListe())
        self.ajouter_parametre(PrmSupprimer())
