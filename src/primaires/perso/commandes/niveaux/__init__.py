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


"""Package contenant la commande 'niveaux'.

"""

from primaires.interpreteur.commande.commande import Commande

class CmdNiveaux(Commande):
    
    """Commande 'niveaux'.
    
    """
    
    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "niveaux", "levels")
        self.aide_courte = "affiche vos niveaux actuels"
        self.aide_longue = \
            "Cette commande affiche la liste de vos niveaux ainsi " \
            "que l'avancement dans chacun des niveaux. Vous noterez, " \
            "invariablement, le niveau principal, ainsi " \
            "qu'optionnellement des niveaux secondaires " \
            "qui caractériseront plus vos aptitudes plus spécifiques."
    
    def interpreter(self, personnage, dic_masques):
        """Interprétation de la commande"""
        grille = [(0, 1)] + list(importeur.perso.gen_niveaux.grille_xp)
        xp = personnage.xp
        niveau = personnage.niveau
        xp_total = grille[niveau][1]
        pourcentage = int(xp / xp_total * 100)
        msg = \
            "+-----------------+-----+-------------------+------+\n" \
            "| {:<15} | {:>3} | {:>8}/{:>8} | {:>3}% |\n".format(
            "Principal", niveau, xp, xp_total, pourcentage)
        
        niveaux = sorted([(cle, nb) for cle, nb in personnage.niveaux.items()],
                key=lambda e: e[1], reverse=True)
        for cle, nb in niveaux:
            nom = importeur.perso.niveaux[cle].nom.capitalize()
            xp = personnage.xps[cle]
            niveau = personnage.niveaux[cle]
            if niveau == 0:
                return
            
            xp_total = grille[niveau][1]
            pourcentage = int(xp / xp_total * 100)
            msg += \
                    "\n| {:<15} | {:>3} | {:>8}/{:>8} | {:>3}% |\n".format(
                    nom, niveau, xp, xp_total, pourcentage)
        
        msg += \
            "\n+-----------------+-----+-------------------+------+"
        personnage << msg
