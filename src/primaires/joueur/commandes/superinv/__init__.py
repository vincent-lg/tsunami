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


"""Package contenant la commande 'superinv'"""

from primaires.interpreteur.commande.commande import Commande

class CmdSuperinv(Commande):
    
    """Commande 'superinv'.
    
    """
    
    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "superinv", "superinv")
        self.groupe = "administrateur"
        self.aide_courte = "passe super invisible"
        self.aide_longue = \
            "Cette commande permet de devenir super invisible " \
            "(invisibilité \"divine\" que seuls les administrateurs " \
            "pourront voir). Utiliser une nouvelle fois cette commande " \
            "pour être de nouveau visible."
    
    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        if not personnage.super_invisible:
            personnage << "Vous devenez invisible."
            personnage.salle.envoyer("{} devient subitement invisible.",
                    personnage)
        
        personnage.super_invisible = not personnage.super_invisible
        if not personnage.super_invisible:
            personnage << "Vous n'êtes plus invisible."
            personnage.salle.envoyer("{} apparaît subitement.",
                    personnage)
