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


"""Package contenant la commande 'commande'.

"""

from primaires.interpreteur.commande.commande import Commande
from primaires.format.fonctions import *

class CmdCommande(Commande):
    
    """Commande 'commande'.
    
    """
    
    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "commande", "command")
        self.schema = "(<nom_commande>)"
        self.aide_courte = "affiche les commandes chargées"
        self.aide_longue = \
            "Cette commande permet de visualiser les commandes chargées. " \
            "On peut lui donner en paramètre le nom d'une commande. Dans " \
            "ce cas, le système affiche l'aide de la commande passée en " \
            "paramètre."
    
    def interpreter(self, personnage, dic_masques):
        """Interprétation de la commande"""
        # Si aucune commande n'a été entré, on affiche la liste des commandes
        if dic_masques["nom_commande"] is None:
            categories = type(self).importeur.interpreteur.categories
            commandes = {}
            for cmd in type(self).importeur.interpreteur.commandes:
                if type(self).importeur.interpreteur.groupes. \
                        personnage_a_le_droit(personnage, cmd.commande):
                    commandes[cmd.commande.get_nom_pour(personnage)] = cmd.commande
            
            if not commandes:
                personnage << "Aucune commande ne semble être définie." \
                        "Difficile à croire, non ?"
            else:
                final = "Liste des commandes :\n\n"
                for id_categ, nom_categ in categories.items():
                    liste_commandes = []
                    for nom_commande, commande in commandes.items():
                        if commande.categorie.identifiant == id_categ:
                            liste_commandes.append(nom_commande)
                    if liste_commandes:
                        final += nom_categ + "\n "
                        final += "\n ".join(sorted(liste_commandes))
                        final += "\n\n"
                personnage << final
        
        else: # la commande existe
            commande = dic_masques["nom_commande"].commande
            personnage << souligner_sauts_de_ligne( \
                    commande.aide_longue_pour(personnage))
