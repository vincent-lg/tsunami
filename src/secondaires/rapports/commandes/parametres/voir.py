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


"""Fichier contenant le paramètre 'voir' de la commande 'report'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmVoir(Parametre):
    
    """Commande 'rapport voir'"""
    
    def __init__(self,typeRapport):
        """Constructeur de la commande"""
        Parametre.__init__(self, "voir", "see")
        
        rapports = type(self).importeur.rapports
        self.typeRapport = typeRapport
        self.nomType = rapports.nomType(typeRapport)
        self.determinant_nom = rapports.determinant_nom(typeRapport)
        
        self.groupe = "joueur"
        self.schema = "<ident_{}>".format(self.typeRapport)
        self.aide_courte = "affiche {}".format(self.determinant_nom)
        self.aide_longue = "TODO"
    
    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        rapport = dic_masques["ident_{}".format(self.typeRapport)].objet
        
        rap_cfg = type(self.importeur).anaconf.get_config("rapports")
        
        res = "+" + "-" * 60 + "+\n"
        res += "| |tit|{} {ident}|ff|".format(self.nomType, \
                ident=rapport.ident).ljust(70) + "|\n"
        res += "+" + "-" * 60 + "+\n"
        res += "| " + rapport.resume.ljust(59) + "|\n"
        res += "+" + "-" * 60 + "+\n"
        
        if not rap_cfg.cache:
            res += "| Statut : " + rapport.statut.ljust(50) + "|\n"
            res += "+" + "-" * 60 + "+\n"
            res += "| Catégorie : " + rapport.categorie.ljust(47) + "|\n"
            res += "+" + "-" * 60 + "+\n"
        
        res += "| Description : ".ljust(61) + "|\n"
        res += "".join([ "|  " + l.ljust(58) + "|\n" for l in \
                str(rapport.description).split("\n") ])
        res += "+" + "-" * 60 + "+\n"
        
        if not rap_cfg.cache:
            if rapport.commentaires != []:
                res += "| Commentaires : " + rapport.categorie.ljust(59) + "|\n"
                for (nom, text) in rapport.commentaires:
                    res += "+" + "-" * 20 + "\n"
                    res += "| " (nom + " :").ljust(47) + "|\n"
                    res += "".join([ "|  " + l.ljust(58) + "|\n" for l in \
                        str(text).split("\n") ])
            else:
                res += "| Pas de commentaire".ljust(61) + "|\n"
            res += "+" + "-" * 60 + "+\n"
        
        res = res.rstrip("\n")
        personnage << res
        
