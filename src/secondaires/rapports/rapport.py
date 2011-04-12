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

"""Fichier contenant la classe Bug, détaillée plus bas;"""

from abstraits.obase import *
from primaires.format.description import Description

class Rapport(BaseObj):
    
    """Cette classe définit un rapport.
    Un rapport possède un résumé et une description
    et un numéro d'identification
    
    """
    
    def __init__(self,typeRapport):
        """Constructeur du bug
        """
        BaseObj.__init__(self)
        self.resume = ""
        self.description = Description(parent=self)
        self.ident = -1
        self.typeRapport = typeRapport
        self._statut = "nouveau"
        self._categorie = "aucune"
        self.responsable = None
        self.commentaires = []
        
    def _get_statut(self):
        return self._statut
    
    def _set_statut(self, statut):
        statuts = type(self).importeur.rapports.statuts
        if ( (statut >= len(statuts)) or statut < 0 ):
            raise(ValueError)
        self._statut = statuts[statut]
    
    statut = property(_get_statut, _set_statut)
    
    def _get_categorie(self):
        return self._categorie
    
    def _set_categorie(self, categorie):
        self._categorie = type(self).importeur.rapports.categories[categorie]
    
    categorie = property(_get_categorie, _set_categorie)
    
    def __getinitargs__(self):
        return ("",)
    
    def enregistrer(self):
        pass
    
    def __str__(self):
        """Retourne l'identifiant du bug, son ident'"""
        if self.ident == -1:
            return "Nouveau bug"
        else:
            return str(self.ident)
    
