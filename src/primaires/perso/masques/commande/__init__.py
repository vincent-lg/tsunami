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


"""Fichier contenant le masque <commande>."""

from primaires.interpreteur.masque.masque import Masque
from primaires.interpreteur.masque.fonctions import *
from primaires.interpreteur.masque.exceptions.erreur_validation \
        import ErreurValidation

class Commande(Masque):
    
    """Masque <commande>.
    On attend un nom de commande en paramètre.
    
    """
    
    nom = "nom_commande"
    
    def __init__(self):
        """Constructeur du masque"""
        Masque.__init__(self)
        self.nom_complet = "nom d'une commande"
        self.commande = None
    
    def valider(self, personnage, dic_masques, commande):
        """Validation du masque"""
        nom_commande = liste_vers_chaine(commande).lstrip()
        
        if not nom_commande:
            raise ErreurValidation( \
                "De quelle commande souhaitez-vous voir l'aide ?")
        
        # On cherche dans les commandes du module interpreteur
        commande = None
        commandes = type(self).importeur.interpreteur.commandes
        commandes = sorted(commandes, key=lambda noeud: \
                noeud.commande.get_nom_pour(personnage))
        for cmd in commandes:
            if type(self).importeur.interpreteur.groupes. \
                    personnage_a_le_droit(personnage, cmd.commande):
                nom = cmd.commande.get_nom_pour(personnage)
                if nom.startswith(nom_commande):
                    commande = cmd
                    break
        
        if not commande:
            raise ErreurValidation(
                "|att|Cette commande est introuvable.|ff|")
        
        self.commande = commande.commande
        
        return True
