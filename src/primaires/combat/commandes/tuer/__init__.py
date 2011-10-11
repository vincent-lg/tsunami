
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


"""Package contenant la commande 'tuer'.

"""

from primaires.interpreteur.commande.commande import Commande

class CmdTuer(Commande):
    
    """Commande 'tuer'.
    
    """
    
    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "tuer", "kill")
        self.schema = "<nom_joueur>"
        self.aide_courte = "attaque un personnage présent"
        self.aide_longue = \
            "Cette commande attaque un personnage présent dans la pièce, " \
            "si vous pouvez le faire. Le combat se terminera plus vraissemblablement " \
            "par la fuite ou la mort d'un des deux combattants."
    
    def interpreter(self, personnage, dic_masques):
        """Interprétation de la commande"""
        attaque = dic_masques["nom_joueur"].joueur
        # A supprimer quand le masque sera créé
        if attaque.salle is not personnage.salle:
            return
        
        type(self).importeur.combat.creer_combat(personnage.salle,
                personnage, attaque)
        personnage << "Vous attaquez {}.".format(attaque.nom)
        attaque << "{} vous attaque.".format(personnage.nom)
