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


"""Package contenant la commande 'sorts liste'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmListe(Parametre):
    
    """Commande 'sorts liste'.
    
    """
    
    def __init__(self):
        """Constructeur de la commande"""
        Parametre.__init__(self, "list", "list")
        self.groupe = "administrateur"
        self.aide_courte = "liste les sorts existants"
        self.aide_longue = \
            "Cette commande permet de lister les sorts existants."
    
    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        sorts = sorted([sort for sort in importeur.magie.sorts.values()], \
                key=lambda sort: sort.cle)
        if not sorts:
            personnage << "|err|Aucun sort n'a encore été créé."
            return
        
        lignes = [
            "+-----------------+----------------------+------------+",
            "| Clé du sort     | Nom                  | Cible      |",
        ]
        
        lignes.append(lignes[0])
        for sort in sorts:
            lignes.append("| {:<15} | {:<20} | {:<10} |".format(
                    sort.cle, sort.nom, sort._type_cible))
        
        lignes.append(lignes[0])
        personnage << "\n".join(lignes)
