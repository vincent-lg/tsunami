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


"""Package contenant la commande 'dyncom'."""

from primaires.interpreteur.commande.commande import Commande
from .editer import PrmEditer
from .liste import PrmListe

class CmdDyncom(Commande):
    
    """Commande 'dyncom'"""
    
    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "dyncom", "dyncom")
        self.groupe = "administrateur"
        self.nom_categorie = "batisseur"
        self.aide_courte = "manipule les commandes dynamiques"
        self.aide_longue = \
            "Cette commande permet de créer, éditer et lister " \
            "les commandes dynamiques. Une commande dynamique, " \
            "à la différence des commandes statiques (définies dans " \
            "le code) peut être créée par les bâtisseurs. En fonction " \
            "des noms (français et anglais) qui lui sont assignés, " \
            "elle se connecte avec des évènements d'éélments observables " \
            "dans la salle d'action. Si par exemple une commande " \
            "dynamique |cmd|pousser/push|ff| est définie, elle pourra " \
            "être utilisée par les joueurs pour pousser des éléments " \
            "observables dans la salle. Les éléments observables " \
            "peuvent être des détails descriptifs, des objets, " \
            "même des joueurs ou PNJ. Pour modifier le comportement " \
            "d'un de ces éléments en particulier, il faut le scripter " \
            "en lui ajoutant un évènement portant le nom français " \
            "de la commande (|ent|pousser|ff| dans cet exemple)."
    
    def ajouter_parametres(self):
        """Ajout des paramètres."""
        self.ajouter_parametre(PrmEditer())
        self.ajouter_parametre(PrmListe())
