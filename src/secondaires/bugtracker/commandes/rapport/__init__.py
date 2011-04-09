# -*-coding:Utf-8 -*

# Copyright (c) 2010 DAVY Guillaume
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


"""Package contenant la commande 'rapport'."""

from primaires.interpreteur.commande.commande import Commande
from secondaires.bugtracker.commandes.rapport.nouveau import PrmNouveau
from secondaires.bugtracker.commandes.rapport.lister import PrmLister
from secondaires.bugtracker.commandes.rapport.voir import PrmVoir
from secondaires.bugtracker.commandes.rapport.effacer import PrmEffacer
from secondaires.bugtracker.commandes.rapport.editer import PrmEditer

class CmdRapport(Commande):
    
    """Commande 'rapport'.
    
    """
    
    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "rapport", "report")
        self.groupe = "joueur"
        self.nom_categorie = "bugs"
        self.aide_courte = "Manipulation des bugs"
        self.aide_longue = \
            "Cette commande permet de manipuler les bugs " \
    
    def ajouter_parametres(self):
        """Ajout des paramètres"""
        prm_nouveau = PrmNouveau()
        prm_list = PrmList()
        prm_voir = PrmVoir()
        prm_effacer = PrmEffacer()
        prm_editer = PrmEditer()
        
        self.ajouter_parametre(prm_nouveau)
        self.ajouter_parametre(prm_list)
        self.ajouter_parametre(prm_voir)
        self.ajouter_parametre(prm_effacer)
        self.ajouter_parametre(prm_editer)
        
