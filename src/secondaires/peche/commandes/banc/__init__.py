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


"""Package contenant la commande 'banc'."""

from primaires.interpreteur.commande.commande import Commande
from .creer import PrmCreer
from .editer import PrmEditer
from .liste import PrmListe
from .voir import PrmVoir

class CmdBanc(Commande):
    
    """Commande 'banc'"""
    
    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "banc", "school")
        self.groupe = "administrateur"
        self.nom_categorie = "batisseur"
        self.aide_courte = "manipule les bancs de poisson"
        self.aide_longue = \
            "Cette commande permet de créer, éditer et lister " \
            "les bancs de poisson. Des bancs de poisson doivent être " \
            "créés pour permettre à un joueur de pêcher à un endroit. " \
            "Un banc de poisson peut être rattaché à une étendue " \
            "d'eau et à plusieurs salles. Notez que le banc nommé " \
            "'|ent|base|ff|', si existe, sera utilisé dans tous les " \
            "terrains permettant la pêche mais ne définissant pas " \
            "de banc particulier."
    
    def ajouter_parametres(self):
        """Ajout des paramètres."""
        self.ajouter_parametre(PrmCreer())
        self.ajouter_parametre(PrmEditer())
        self.ajouter_parametre(PrmListe())
        self.ajouter_parametre(PrmVoir())
