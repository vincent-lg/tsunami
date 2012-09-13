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


"""Jeu de poquiir."""

from random import *

from .. import BaseJeu

class Jeu(BaseJeu):
    
    """Ce jeu définit le jeu de poquiir.
    
    Il est rattaché au plateau poquiir.
    
    """
    
    nom = "poquiir"
    def init(self):
        """Construction du jeu."""
        self.nb_joueurs_min = 2
        self.nb_joueurs_max = 6
        self.en_main = {}
        self.non_distribuees = []
        self.abandons = []
    
    def peut_commencer(self):
        """La partie peut-elle commencer ?"""
        return True
    
    def peut_jouer(self, personnage):
        """Le personnage peut-il jouer ?"""
        if personnage in self.abandons:
            personnage << "Vous avez abandonné cette manche."
            return False
        
        return True
    
    def jouer(self, personnage, msg):
        """Joue au jeu.
        
        Les possibilités sont :
            m <montant> : pour miser davantage
            s : suivre (check) sans miser davantage
            ab : abandonner
        
        """
        possibilites = \
            "Les possibilités sont :\n\n" \
            " |cmd|m <montant>|ff| pour miser davantage (exemple " \
            "|cmd|m 200|ff|\n)" \
            " |cmd|s|ff| pour suivre sans miser davantage\n" \
            " |cmd|ab|ff| pour abandonner la manche\n\n" \
            "|att|Les montants sont toujours donnés en pièces de bronze.|ff|"
        
        if msg:
            opt = msg.split(" ")[0].lower()
            reste = msg[len(msg):]
            if opt == "m":
                try:
                    montant = int(reste)
                except ValueError:
                    personnage << "|err|Montant {} invalide|ff|.".format(
                            reste)
                    return False
                else:
                    return self.monter(personnage, reste)
            elif opt == "s":
                return self.suivre(personnage)
            elif opt == "ab":
                self.abandonner(personnage)
                return True
            else:
                personnage << possibilites
                return False

        return False
