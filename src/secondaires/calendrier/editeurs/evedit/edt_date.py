# -*-coding:Utf-8 -*

# Copyright (c) 2010-2016 AYDIN Ali-Kémal
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


"""Ce fichier définit le contexte-éditeur EdtDate."""

import datetime

from primaires.interpreteur.editeur import Editeur

class EdtDate(Editeur):
    
    """Contexte-éditeur d'édition de la date de l'évènement.
    
    """
    
    def __init__(self, pere, objet=None, attribut=None):
        """Constructeur de l'éditeur"""
        Editeur.__init__(self, pere, objet, attribut)
    
    def accueil(self):
        """Message d'accueil du contexte."""
        evenement = self.objet
        msg = "| |tit|" + "Edition de la date de l'évènement " \
                "de {}".format(evenement.titre).ljust(76)
        msg += "|ff||\n" + self.opts.separateur + "\n"
        msg += "Entrez la |ent|nouvelle date|ff| sous la forme " \
            "JJ-MM-AAAA.\n" \
            "Par exemple : |ent|10-05-2012|ff|\n\n" \
            "Date actuelle : |bc|" + evenement.str_date + "|ff|"
        return msg
    
    def interpreter(self, msg):
        """Interprétation de l'éditeur."""
        evenement = self.objet
        msg = msg.strip()
        if not msg:
            self.pere << "|err|Entrez la date sous la forme JJ-MM-AAAA.|ff|"
            return
        
        try:
            jour, mois, annee = msg.split("-")
        except ValueError:
            self.pere << "|err|Syntaxe invalide.|ff|"
            return
        
        try:
            jour = int(jour)
            assert jour >= 0 and jour < 32
        except (ValueError, AssertionError):
            self.pere << "|err|Numéro de jour invalide.|ff|"
            return
        
        try:
            mois = int(mois)
            assert mois >= 0 and mois <= 12
        except (ValueError, AssertionError):
            self.pere << "|err|Numéro de mois invalide.|ff|"
            return
        
        try:
            annee = int(annee)
            assert annee > 0
        except (ValueError, AssertionError):
            self.pere << "|err|Numéro d'année invalide.|ff|"
            return
        
        if annee < 100:
            annee = 2000 + annee
        
        n_date = datetime.date(year=annee, month=mois, day=jour)
        evenement.date = n_date
        self.actualiser()
