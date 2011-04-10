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


"""Fichier contenant le paramètre 'list' de la commande 'rapport'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmLister(Parametre):
    
    """Commande 'rapport lister'"""
    
    def __init__(self,typeRapport):
        """Constructeur de la commande"""
        Parametre.__init__(self, "lister", "list")
        
        rapports = type(self).importeur.rapports
        self.typeRapport = typeRapport
        self.nomType = rapports.nomType(typeRapport)
        self.determinant_nom = rapports.determinant_nom(typeRapport)
        
        self.groupe = "joueur"
        self.aide_courte = "affiche les {} en cours".format(self.nomType)
        self.aide_longue = "TODO"
    
    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        objets = type(self).importeur.rapports[self.typeRapport]
        
        lignes = []
        
        lignes = [ \
                str(objet.ident).ljust(10) + " | " + objet.resume.ljust(46) + "|"
                for objet in objets
            ]
        
        if lignes :
            res = "+" + "-" * 60 + "+\n"
            res += "| |tit|{}s ouverts|ff|".format(self.nomType).ljust(70) + "|\n"
            res += "+" + "-" * 60 + "+\n| "
            res += "\n| ".join(lignes)
            res += "\n+" + "-" * 60 + "+\n"
            res = res.rstrip("\n")
            personnage << res
        else:
            personnage.envoyer("|att|Aucun {} ouvert.|ff|".format(self.nomType))
        
    
