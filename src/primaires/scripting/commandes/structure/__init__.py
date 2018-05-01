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


"""Package contenant la commande 'structure'."""

from primaires.interpreteur.commande.commande import Commande
from primaires.scripting.commandes.structure.liste import PrmListe
from primaires.scripting.commandes.structure.supprimer import PrmSupprimer
from primaires.scripting.commandes.structure.voir import PrmVoir

class CmdStructure(Commande):

    """Commande 'structure'"""

    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "structure", "structure")
        self.groupe = "administrateur"
        self.nom_categorie = "batisseur"
        self.aide_courte = "manipule les structures"
        self.aide_longue = \
            "Cette commande permet de lister et rechercher dans les " \
            "structures. Les structures sont souvent créées par " \
            "le scripting et remplies par des éditeurs personnalisés " \
            "(voir la commande %editeur%). Les structures sont " \
            "regroupées dans différents groupes, sous une clé commune " \
            "décrivant l'usage de la structure (par exemple journal, " \
            "maison, poeme, doleance_picte, etc...). Au sein d'un " \
            "groupe, une structure est identifiée par un ID, un " \
            "numéro identifiant commençant à 1. Par exemple, la " \
            "première structure du groupe 'journal' aura l'ID 1, la " \
            "seconde aura l'ID 2 et ainsi de suite. Pour plus " \
            "d'information sur les structures, consultez " \
            "http://redmine.kassie.fr/projects/documentation/wiki/Structure ."

    def ajouter_parametres(self):
        """Ajout des paramètres."""
        self.ajouter_parametre(PrmListe())
        self.ajouter_parametre(PrmSupprimer())
        self.ajouter_parametre(PrmVoir())
