# -*-coding:Utf-8 -*

# Copyright (c) 2013 CORTIER Benoît
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


"""Package contenant la commande 'valider'"""

from primaires.interpreteur.commande.commande import Commande
from .voir import PrmVoir
from .accepter import PrmAccepter
from .editer import PrmEditer
from .lister import PrmLister
from .refuser import PrmRefuser

class CmdValider(Commande):

    """Commande 'valider'.

    """

    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "valider", "validate")
        self.nom_categorie = "moderation"
        self.groupe = "administrateur"
        self.aide_courte = "Modère les descriptions des joueurs."
        self.aide_longue = \
            "Cette commande permet de vérifier, manipuler et valider ou non " \
            "la description des joueurs." \

    def ajouter_parametres(self):
        """Méthode d'interprétation de commande"""
        self.ajouter_parametre(PrmVoir())
        self.ajouter_parametre(PrmAccepter())
        self.ajouter_parametre(PrmEditer())
        self.ajouter_parametre(PrmLister())
        self.ajouter_parametre(PrmRefuser())
