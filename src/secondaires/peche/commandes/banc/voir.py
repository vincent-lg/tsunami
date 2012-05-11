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


"""Fichier contenant le paramètre 'voir' de la commande 'banc'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmVoir(Parametre):
    
    """Commande 'banc voir'.
    
    """
    
    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "voir", "view")
        self.schema = "<cle>"
        self.aide_courte = "visionne un banc particulier"
        self.aide_longue = \
            "Cette commande offre un affichage détaillé d'un banc de poisson."
    
    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        cle = dic_masques["cle"].cle
        if cle not in importeur.peche.bancs:
            personnage << "|err|Ce banc n'existe pas.|ff|"
            return
        
        banc = importeur.peche.bancs[cle]
        proba_max = sum(p for b, p in banc.poissons.items())
        poissons = []
        for poisson, proba in banc.poissons.items():
            poissons.append("{:<20} {:>3} / {:>3} ({:>3}%)".format(
                    poisson.cle, proba, proba_max, int(
                    proba / proba_max * 100)))
        if not poissons:
            poissons.append("Aucun")
        
        msg = "Banc {}:\n".format(banc.cle)
        msg += "\n  Abondance actuelle / abondance maximum : {} / {} " \
                "({}%)".format(banc.abondance_actuelle, banc._abondance_max,
                int(banc.abondance_actuelle / banc._abondance_max * 100))
        msg += "\n  Poissons :\n    " + "\n    ".join(poissons)
        personnage << msg
