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


"""Package contenant la commande 'sorts editer'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmEditer(Parametre):
    
    """Commande 'sorts editer'.
    
    """
    
    def __init__(self):
        """Constructeur de la commande"""
        Parametre.__init__(self, "éditer", "edit")
        self.schema = "<ident>"
        self.groupe = "administrateur"
        self.nom_categorie = "batisseur"
        self.aide_courte = "édite un sort"
        self.aide_longue = \
            "Cette commande ouvre l'éditeur de sorts, qui permet d'éditer " \
            "des sorts en tout genre."
    
    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        cle_sort = dic_masques["ident"].ident
        if cle_sort not in importeur.magie.sorts:
            personnage << "|err|Ce sort n'existe pas.|ff|"
            return
        
        sort = importeur.magie.sorts[cle_sort]
        editeur = importeur.interpreteur.construire_editeur(
                "spedit", personnage, sort)
        personnage.contextes.ajouter(editeur)
        editeur.actualiser()
