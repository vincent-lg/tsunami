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


"""Package contenant la commande 'auberge'."""

from primaires.interpreteur.commande.commande import Commande
from .creer import PrmCreer
from .editer import PrmEditer
from .liste import PrmListe
from .supprimer import PrmSupprimer

class CmdAuberge(Commande):

    """Commande 'auberge'"""

    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "auberge", "inn")
        self.groupe = "administrateur"
        self.nom_categorie = "batisseur"
        self.aide_courte = "manipule les auberges"
        self.aide_longue = \
            "Cette commande permet de créer, éditer, lister " \
            "et supprimer les auberges. Pour paramétrer le détail " \
            "d'une auberge (ses chambres à louer, leur prix et d'autres " \
            "informations), il faut l'éditer."

    def ajouter_parametres(self):
        """Ajout des paramètres."""
        self.ajouter_parametre(PrmCreer())
        self.ajouter_parametre(PrmEditer())
        self.ajouter_parametre(PrmListe())
        self.ajouter_parametre(PrmSupprimer())
