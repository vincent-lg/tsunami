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
# POSSIBILITY OF SUCH DAMAGE.


"""Package contenant la commande 'talents'.

"""

from primaires.interpreteur.commande.commande import Commande

class CmdTalents(Commande):
    
    """Commande 'talents'.
    
    """
    
    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "talents", "skills")
        self.aide_courte = "affiche vos talents connus"
        self.aide_longue = \
            "Cette commande affiche la liste des talents que vous " \
            "connaissez, triés par niveau secondaire."
    
    def interpreter(self, personnage, dic_masques):
        """Interprétation de la commande"""
        talents = personnage.talents
        par_niveaux = {}
        for talent, connaissance in talents.items():
            talent = importeur.perso.talents[talent]
            if connaissance > 0:
                if talent.niveau.nom not in par_niveaux:
                    par_niveaux[talent.niveau.nom] = []
                
                par_niveaux[talent.niveau.nom].append("{} : {:>3}%".format(
                        talent.nom, connaissance))
        
        if par_niveaux:
            msg = "Talents que vous connaissez :\n"
            for niveau, talents in sorted(par_niveaux.items()):
                msg += "\n* {} :".format(niveau.capitalize())
                for talent in sorted(talents):
                    msg += "\n  " + talent.capitalize()
            
            personnage << msg
        else:
            personnage << "Vous ne maîtrisez pour l'heure aucun " \
                    "talent."
