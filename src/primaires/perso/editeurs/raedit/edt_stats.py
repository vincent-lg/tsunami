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


"""Fichier contenant le contexte éditeur EdtStats"""

from primaires.interpreteur.editeur import Editeur
from primaires.format.fonctions import contient

class EdtStats(Editeur):
    
    """Classe définissant le contexte éditeur 'stats'.
    Ce contexte permet d'éditer les stats d'une race.
    
    """
    
    def __init__(self, pere, objet=None, attribut=None):
        """Constructeur de l'éditeur"""
        Editeur.__init__(self, pere, objet, attribut)
    
    def accueil(self):
        """Message d'accueil"""
        msg = \
            "Entrez |cmd|/|ff| pour revenir à la fenêtre parente, ou le " \
            "|ent|nom|ff| d'une stat suivi\nd'un slash |cmd|/|ff| et d'une " \
            "|ent|valeur|ff| pour modifier la stat.\n\n"
        stats = self.objet
        msg += "+-" + "-" * 20 + "-+-" + "-" * 6 + "-+\n"
        msg += "||tit| " + "Nom".ljust(20) + " |ff|||tit| "
        msg += "Valeur".ljust(6) + " |ff||\n"
        msg += "+-" + "-" * 20 + "-+-" + "-" * 6 + "-+\n"
        for stat in stats:
            if not stat.max:
                msg += "| |ent|" + stat.nom.ljust(20) + "|ff| | "
                msg += str(stat.defaut).rjust(6) + " |\n"
        msg += "+-" + "-" * 20 + "-+-" + "-" * 6 + "-+"
        
        return msg
    
    def interpreter(self, msg):
        """Interprétation du message"""
        try:
            nom_stat, valeur = msg.split(" / ")
        except ValueError:
            self.pere << "|err|Syntaxe invalide.|ff|"
        else:
            # On cherche la stat
            stat = None
            for t_stat in self.objet:
                if not t_stat.max and contient(t_stat.nom, nom_stat):
                    stat = t_stat
                    break
            
            if not stat:
                self.pere << "|err|Cette stat est introuvable.|ff|"
            else:
                # Convertion
                try:
                    valeur = int(valeur)
                    assert valeur > 0
                    assert valeur >= stat.marge_min
                    assert valeur <= stat.marge_max
                except (ValueError, AssertionError):
                    self.pere << "|err|Valeur invalide.|ff|"
                else:
                    stat.defaut = valeur
                    self.actualiser()
