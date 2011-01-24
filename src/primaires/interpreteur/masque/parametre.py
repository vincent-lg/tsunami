# -*-coding:Utf-8 -*

# Copyright (c) 2010 LE GOFF Vincent
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


"""Fichier définissant la classe Parametre, détaillée plus bas."""

from primaires.interpreteur.commande.commande import Commande
from primaires.interpreteur.masque.masque import Masque
from primaires.interpreteur.masque.fonctions import *

class Parametre(Commande):
    
    """Un paramètre est à la fois un masque et une commande.
    Il possède en effet un nom français et anglais et une arborescence qui lui
    est propre.
    En somme, il s'agit d'une sous-commande.
    
    """
    
    def __init__(self, francais, anglais):
        """Constructeur du paramètre"""
        Commande.__init__(self, francais, anglais)
        Masque.__init__(self, self.nom_francais)
        self.nom = self.nom_francais
        self.groupe = ""
        self.tronquer = False
        self.schema = ""
    
    def __str__(self):
        """Fonction d'affichage"""
        return "p" + Commande.__str__(self)
    
    def valider(self, personnage, dic_masques, commande):
        """Fonction de validation du masque Parametre.
        Un paramètre se valide si la commande qu'on lui passe débute par un
        espace puis son nom de paramètre (en fonction de la langue du
        personnage).
        
        """
        str_commande = liste_vers_chaine(commande)
        
        if str_commande.startswith(" "):
            commande.pop(0)
            valide = Commande.valider(self, personnage, dic_masques, \
                    commande)
            if not valide:
                commande.insert(0, " ")
        else:
            valide = False
        
        return valide
    
    def est_parametre(self):
        """Return True puisque c'est un paramètre"""
        return True
