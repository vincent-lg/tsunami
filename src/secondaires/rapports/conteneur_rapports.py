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

from abstraits.unique import Unique
from primaires.interpreteur.groupe.groupe import Groupe

class ConteneurRapports(Unique):
    
    """Classe conteneur des rapports.
    
    """
    
    def __init__(self,typeRapport):
        """Constructeur du conteneur."""
        Unique.__init__(self, "rapports", typeRapport)
        self.newIdent = 0
        self._rapports = {} # ident:rapport
    
    def __getnewargs__(self):
        return ("",)
    
    def ajouter_nouveau_rapport(self,rapport):
        """Permet de créer un rapport"""
        
        rapport.ident = self.newIdent
        
        self._rapports[rapport.ident] = rapport
        self.newIdent += 1
        
        return rapport
    
    def __delitem__(self,ident):
        del self._rapports[ident]
    
    def __iter__(self):
        return iter(self._rapports.values())
    
    def __contains__(self, nom_rapport):
        """Retourne True si le groupe est dans le dictionnaire, False sinon"""
        return nom_rapport in self._groupes.keys()
    
    def __getitem__(self, nom_rapport):
        """Retourne le groupe avec le nom spécifié"""
        return self._rapports[nom_rapport]
    
    def __len__(self):
        """Retourne le nombre de groupes"""
        return len(self._rapports)


