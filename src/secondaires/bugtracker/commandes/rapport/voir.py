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
    
    def __init__(self):
        """Constructeur de la commande"""
        Parametre.__init__(self, "voir", "see")
        self.groupe = "joueur"
        self.schema = "<ident_bug>"
        self.aide_courte = "affiche un bug"
        self.aide_longue = "TODO"
    
    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        bug = dic_masques["ident_bug"].bug
        
        res = "+" + "-" * 60 + "+\n"
        res += "| |tit|Bug {}|ff|".format(bug.ident).ljust(70) + "|\n"
        res += "+" + "-" * 60 + "+\n"
        res += "| " + bug.resume.ljust(59) + "|\n"
        res += "+" + "-" * 60 + "+\n"
        res += "".join([ "| " + l.ljust(59) + "|\n" for l in str(bug.description).split("\n") ])
        res += "+" + "-" * 60 + "+\n"
        res = res.rstrip("\n")
        personnage << res
        
