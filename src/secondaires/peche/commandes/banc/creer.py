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


"""Package contenant le paramètre 'créer' de la commande 'banc'."""

from primaires.interpreteur.masque.parametre import Parametre
from primaires.interpreteur.editeur.presentation import Presentation

class PrmCreer(Parametre):
    
    """Commande 'banc créer'"""
    
    def __init__(self):
        """Constructeur du paramètre."""
        Parametre.__init__(self, "creer", "create")
        self.schema = "<cle>"
        self.aide_courte = "crée un banc de poisson"
        self.aide_longue = \
            "Cette commande permet de créer un nouveau banc de " \
            "poisson. Vous devez préciser en argument la clé identifiant " \
            "le banc."
    
    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        cle = dic_masques["cle"].cle
        if cle in importeur.peche.bancs:
            personnage << "|err|Ce banc existe déjà.|ff|"
            return
        
        banc = importeur.peche.creer_banc(cle)
        editeur = importeur.interpreteur.construire_editeur(
                "schooledit", personnage, banc)
        personnage.contextes.ajouter(editeur)
        editeur.actualiser()
