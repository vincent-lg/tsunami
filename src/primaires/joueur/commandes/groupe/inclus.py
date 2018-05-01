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


"""Fichier contenant le paramètre 'inclus' de la commande 'groupe'."""

from primaires.interpreteur.masque.parametre import Parametre
from .inclus_ajouter import PrmInclusAjouter
from .inclus_supprimer import \
    PrmInclusSupprimer
from .inclus_vider import PrmInclusVider

class PrmInclus(Parametre):
    
    """Commande 'groupe inclus'.
    
    """
    
    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "inclus", "include")
        self.aide_courte = "gère les groupes inclus"
        self.aide_longue = \
                "Cette commande permet de gérer les groupes inclus " \
            "d'un groupe. Si un groupe |tit|a|ff| inclus d'un groupe " \
            "|tit|b|ff|, alors |tit|a|ff| possédera les commandes de " \
            "|tit|b|ff|. Par défaut, |tit|administrateur|ff| inclus " \
            "|tit|joueur|ff| qui lui-même inclus |tit|pnj|ff|. " \
            "Référez-vous aux sous-commandes pour plus d'information."
    
    def ajouter_parametres(self):
        """Ajout des paramètres"""
        prm_ajouter = PrmInclusAjouter()
        prm_supprimer = PrmInclusSupprimer()
        prm_vider = PrmInclusVider()
        
        self.ajouter_parametre(prm_ajouter)
        self.ajouter_parametre(prm_supprimer)
        self.ajouter_parametre(prm_vider)
