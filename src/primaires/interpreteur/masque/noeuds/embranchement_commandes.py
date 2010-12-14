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


"""Fichier définissant la classe Embranchement détaillée plus bas."""

from primaires.interpreteur.masque.noeuds.embranchement import Embranchement
from primaires.interpreteur.masque.fonctions import *

class EmbranchementCommandes(Embranchement):
    """Un noeud embranchement, constitué non pas d'un seul suivant mais de
    plusieurs, sous la forme d'une liste extensible.
    A la différence des autres embranchements, il ne doit contenir que des
    noeuds commandes.
    
    """
    
    def __str__(self):
        """Méthode d'affichage"""
        msg = "emb_cmd("
        msg += ", ".join( \
            [str(cmd) + "=" + str(noeud) for noeud, cmd in \
            self.suivant.items()])
        msg += ")"
        return msg
    
    def erreur_validation(self, personnage, dic_masques, lst_commande):
        """Erreur retournée au joueur en cas de non validation"""
        str_commande = liste_vers_chaine(lst_commande)
        print(lst_commande)
        personnage.envoyer(
                "|err|Commande invalide (|ff||cmd|{0}|ff||err|).|ff|".format(
                str_commande))
