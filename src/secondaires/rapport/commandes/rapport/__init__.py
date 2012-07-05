# -*-coding:Utf-8 -*

# Copyright (c) 2012 LE GOFF Vincent
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


"""Package contenant la commande 'rapport' et ses sous-commandes.

Dans ce fichier se trouve la commande même.

"""

from primaires.interpreteur.commande.commande import Commande
from .assigner import PrmAssigner
from .bug import PrmBug
from .editer import PrmEditer
from .evolution import PrmEvolution
from .fermer import PrmFermer
from .liste import PrmListe
from .message import PrmMessage
from .mien import PrmMien
from .nettoyer import PrmNettoyer
from .suggestion import PrmSuggestion
from .voir import PrmVoir

class CmdRapport(Commande):
    
    """Commande 'rapport'.
    
    """
    
    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "rapport", "report")
        self.aide_courte = "manipulation des rapports"
        self.aide_longue = \
            "Cette commande permet de créer un nouveau rapport de bug " \
            "ou de manipuler les rapports existants (pour une correction). " \
            "Pour créer un nouveau rapport, utilisez la sous-commande " \
            "%rapport:bug% si vous voulez rapporter un bug, " \
            "%rapport:suggestion% pour une suggestion ou %rapport:evolution% " \
            "pour une amélioration."
    
    def ajouter_parametres(self):
        """Ajout des paramètres"""
        self.ajouter_parametre(PrmAssigner())
        self.ajouter_parametre(PrmBug())
        self.ajouter_parametre(PrmEditer())
        self.ajouter_parametre(PrmEvolution())
        self.ajouter_parametre(PrmFermer())
        self.ajouter_parametre(PrmListe())
        self.ajouter_parametre(PrmMessage())
        self.ajouter_parametre(PrmMien())
        self.ajouter_parametre(PrmNettoyer())
        self.ajouter_parametre(PrmSuggestion())
        self.ajouter_parametre(PrmVoir())
