# -*-coding:Utf-8 -*

# Copyright (c) 2010-2017 AYDIN Ali-Kémal
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
# ARE DISCLAIMED. IN NO evenement SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""Module contenant le paramètre 'voir' de la commande 'calendrier'"""

import datetime

from primaires.interpreteur.masque.parametre import Parametre

class PrmVoir(Parametre):

    """Commande 'calendrier voir'"""
    
    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "voir", "view")
        self.schema = "(<date>)"
        self.aide_courte = "liste les évènements à venir"
        self.aide_longue = \
            "Cette commande permet de voir le calendrier (les " \
            "évènements à venir). Vous pouvez préciser en paramètre " \
            "une date sous la forme |ent|JJ-MM-AAAA|ff| pour voir " \
            "tous les évènements après cette date."
            
    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        date = datetime.date.today()
        if dic_masques["date"]:
            jour = dic_masques["date"].jour
            mois = dic_masques["date"].mois
            annee = dic_masques["date"].annee
            date = datetime.date(year=annee, month=mois, day=jour)
        
        evenements = sorted(
            [e for e in importeur.calendrier.evenements.values() if \
            e.date >= date], key=lambda e: e.date)
        
        if not evenements:
            personnage << "|att|Aucun évènement défini.|ff|"
        else:
            hl = "+-" + "-" * 20 + "-+-" + "-" * 15 + "-+-" + "-" * 10 + "-+"
            ret = \
                hl + "\n" + \
                "| " + "Titre".ljust(20) + " | " + "Responsable".ljust(15) + \
                " | " + "Date".ljust(10) + " |\n" + hl
            
            for e in evenements:
                titre = e.titre
                if titre:
                    titre = titre[0].upper() + titre[1:]
                if len(titre) > 20:
                    titre = titre[:17] + "..."
                
                titre = titre.ljust(20)
                
                if e.responsables:
                    responsable = e.responsables[0].nom
                else:
                    responsable = "aucun"
                responsable = responsable.ljust(15)
                
                ret += "\n| " + titre + " | " + responsable + " | " + \
                        str(e.date) + " |"
            
            ret += "\n" + hl
            personnage << ret
