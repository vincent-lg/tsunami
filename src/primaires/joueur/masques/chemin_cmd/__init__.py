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


"""Fichier contenant le masque <chemin_commande>."""

from primaires.interpreteur.masque.masque import Masque
from primaires.interpreteur.masque.fonctions import *
from primaires.interpreteur.commande.commande import SEP
from primaires.interpreteur.masque.exceptions.erreur_validation \
        import ErreurValidation

class CheminCommande(Masque):
    
    """Masque <chemin_commande>.
    On attend en paramètre un chemin vers une commande.
    Exemple : commande:sous_commande:sou_sous_commande
    Le masque peut finir par un "." pour symboliser "seulement la commande
    indiquée et aucune de ses sous-commandes."
    
    """
    
    nom = "chemin_commande"
    
    def __init__(self):
        """Constructeur du masque"""
        Masque.__init__(self)
        self.nom_complet = "chemin vers une commande"
        self.joueur = None
    
    def valider(self, personnage, dic_masques, commande):
        """Validation du masque"""
        lstrip(commande)
        chemin_commande = liste_vers_chaine(commande)
        
        if not chemin_commande:
            raise ErreurValidation( \
                "Précisez le chemin vers la commande.")
        
        chemin_commande = chemin_commande.split(" ")[0]
        commande[:] = commande[len(chemin_commande):]
        print("ch_cmd", commande)

        trans_param = True # doit-on transmettre les sous-commandes ?
        if chemin_commande.endswith("."):
            chemin_commande = chemin_commande[:-1]
            trans_param = False
        
        # On cherche dans les chemins des commandes, dans interpreteur.groupes
        chemins = type(self).importeur.interpreteur.groupes.commandes.keys()
        commandes = []
        for chemin in chemins:
            if chemin == chemin_commande:
                commandes.append(chemin)
            elif trans_param and chemin.startswith(chemin_commande + SEP):
                commandes.append(chemin)
        
        if not commandes:
            raise ErreurValidation(
                "|err|Aucune commande correspondant au chemin n'a pu être " \
                "trouvée.|ff|")
        
        self.chemins = commandes
        
        return True
