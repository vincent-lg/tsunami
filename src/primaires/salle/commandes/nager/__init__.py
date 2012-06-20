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


"""Package contenant la commande 'nager'."""

from primaires.interpreteur.commande.commande import Commande
from primaires.interpreteur.masque.exceptions.erreur_interpretation import \
    ErreurInterpretation


class CmdNager(Commande):
    
    """Commande 'nager'"""
    
    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "nager", "swim")
        self.nom_categorie = "bouger"
        self.schema = "<nom_sortie>"
        self.aide_courte = "nage dans une direction"
        self.aide_longue = \
            "Cette commande permet de nager dans une direction " \
            "indiquée. Nager peut être le seul moyen d'avancer dans " \
            "une rivière. Si vous nagez sous l'eau, attention à la " \
            "noyade !"
    
    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        sortie = dic_masques["nom_sortie"].sortie
        salle = personnage.salle
        nom_complet = sortie.nom_complet.capitalize()
        
        personnage.deplacer_vers(sortie.nom, nage=True)
