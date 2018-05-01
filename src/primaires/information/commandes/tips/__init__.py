# -*-coding:Utf-8 -*

# Copyright (c) 2010-2017 LE GOFF Vincent
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


"""Package contenant la commande 'tips'."""

from primaires.interpreteur.commande.commande import Commande

class CmdTips(Commande):
    
    """Commande 'tips'.
    
    """
    
    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "tips", "tips")
        self.nom_categorie = "info"
        self.schema = "<etat>"
        self.aide_courte = "permet d'activer ou désactiver les tips"
        self.aide_longue = \
            "Les tips envoient des messages courtes d'aide " \
            "contextuelle en fonction de l'endroit où vous vous " \
            "trouvez, ce que vous faites, etc. Ces messages informatifs " \
            "sont très utiles pour apprendre les commandes en jeu mais " \
            "ne sont plus nécessaires à partir d'un certain moment. " \
            "Vous pouvez les désactiver ou réactiver quand vous " \
            "le souhaitez, en précisant |cmd|on|ff| ou |cmd|off|ff|."
    
    def interpreter(self, personnage, dic_masques):
        """Interprétation de la commande."""
        etat = dic_masques["etat"].flag
        if etat and personnage.tips:
            personnage << "|att|Le système de tips est déjà activé pour " \
                    "vous.|ff|"
        elif not etat and not personnage.tips:
            personnage << "|att|Le système de tips est déjà désactivé " \
                    "pour vous.|ff|"
        else:
            personnage.tips = etat
            if etat:
                personnage << "Tips activées."
            else:
                personnage << "Tips désactivées."
