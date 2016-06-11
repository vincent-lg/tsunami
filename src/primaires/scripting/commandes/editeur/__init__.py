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


"""Package contenant la commande 'editeur'."""

from primaires.interpreteur.commande.commande import Commande
from primaires.scripting.commandes.editeur.creer import PrmCreer
from primaires.scripting.commandes.editeur.editer import PrmEditer
from primaires.scripting.commandes.editeur.liste import PrmListe

class CmdEditeur(Commande):

    """Commande 'editeur'"""

    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "editeur", "editor")
        self.groupe = "administrateur"
        self.nom_categorie = "batisseur"
        self.aide_courte = "manipule les éditeurs personnalisés"
        self.aide_longue = \
            "Cette commande permet de créer, éditer et lister " \
            "des éditeurs personnalisés. Un éditeur personnalisé " \
            "est un éditeur... pour créer d'autres éditeurs. À l'instar " \
            "de %dyncom% pour créer des commandes dynamiques, %editeur% " \
            "permet de créer des éditeurs dynamiques, créables et " \
            "scriptables par les bâtisseurs. Pour une explication " \
            "détaillée, et un tutoriel pas à pas sur la création " \
            "d'éditeurs, consultez http://redmine.kassie.fr/projects/" \
            "documentation/wiki/EditeurPersonnalise"

    def ajouter_parametres(self):
        """Ajout des paramètres."""
        self.ajouter_parametre(PrmCreer())
        self.ajouter_parametre(PrmEditer())
        self.ajouter_parametre(PrmListe())
