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
# pereIBILITY OF SUCH DAMAGE.


"""Ce fichier définit le contexte-éditeur EdtDate."""

from primaires.interpreteur.editeur import Editeur

class EdtDate(Editeur):
    
    """Contexte-éditeur d'édition de la date de fin de période.
    
    """
    
    def __init__(self, pere, objet=None, attribut=None):
        """Constructeur de l'éditeur"""
        Editeur.__init__(self, pere, objet, attribut)
    
    def accueil(self):
        """Message d'accueil du contexte."""
        periode = self.objet
        msg = "| |tit|" + "Edition de la date de fin de période " \
                "de {}".format(periode.nom).ljust(76)
        msg += "|ff||\n" + self.opts.separateur + "\n"
        msg += "Entrez la |ent|nouvelle date|ff| sous la forme " \
            "du numéro de jour, suivi\nd'un espace puis du numéro " \
            "de mois.\nPar exemple : |ent|5 12|ff|\n\n" \
            "Date actuelle : |bc|" + periode.date_fin + "|ff|"
        return msg
    
    def interpreter(self, msg):
        """Interprétation de l'éditeur."""
        periode = self.objet
        msg = msg.strip()
        if not msg:
            self.pere << "Entrez le numéro du jour, un espace " \
                    "puis le numéro du mois."
            return
        
        try:
            jour, mois = msg.split(" ")
        except ValueError:
            self.pere << "|err|Syntaxe invalide.|ff|"
            return
        
        try:
            jour = int(jour) - 1
            assert jour >= 0 and jour < len(importeur.temps.cfg.noms_jours)
        except (ValueError, AssertionError):
            self.pere << "|err|Numéro de jour invalide.|ff|"
            return
        
        try:
            mois = int(mois) - 1
            assert mois >= 0 and mois < len(importeur.temps.cfg.mois)
        except (ValueError, AssertionError):
            self.pere << "|err|Numéro de mois invalide.|ff|"
            return
        
        periode.fin = (jour, mois)
        self.actualiser()
