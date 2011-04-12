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


"""Fichier contenant le paramètre 'effacer' de la commande 'report'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmEffacer(Parametre):
    
    """Commande 'rapport effacer'"""
    
    def __init__(self,typeRapport):
        """Constructeur de la commande"""
        Parametre.__init__(self, "effacer", "delete")
        
        rapports = type(self).importeur.rapports
        self.typeRapport = typeRapport
        self.nomType = rapports.nomType(typeRapport)
        self.determinant_nom = rapports.determinant_nom(typeRapport)
        
        self.groupe = "administrateur"
        self.schema = "<ident_{}>".format(self.typeRapport)
        self.aide_courte = "Efface {}".format(self.determinant_nom)
        self.aide_longue = "Enlève de manière définitive du gestionnaire " \
            "{}".format(self.determinant_nom)
    
    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        rapports = type(self).importeur.rapports[self.typeRapport]
        ident = dic_masques["ident_{}".format(self.typeRapport)].ident
        del rapports[ident]
        rapports.enregistrer()
        personnage << "{} numéro {ident} effacer".format(self.nomType,ident=ident)
        
