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


"""Fichier contenant le contexte éditeur EdtMnemonic"""

import re

from primaires.interpreteur.editeur.uniligne import Uniligne

# Constantes
MNEMONIC_VALIDE = r"^[a-z0-9_]{1,10}$"

class EdtMnemonic(Uniligne):
    
    """Classe définissant le contexte éditeur 'mnemonic'.
    Ce contexte permet simplement d'éditer le mnémonic de la salle.
    
    """
    
    def interpreter(self, msg):
        """Interprétation du message"""
        msg = msg.lower()
        ancien_ident = self.objet.ident
        ident = self.objet.zone + ":" + msg
        print(ancien_ident, ident)
        if not re.search(MNEMONIC_VALIDE, msg):
            self.pere.envoyer("|err|Ce mnémonic est invalide. Veuillez " \
                    "réessayer.|ff|")
        elif ident in type(self).importeur.salle and ancien_ident != ident:
            self.pere.envoyer("|err|L'identifiant {} est déjà utilisé " \
                    "dans l'univers.|ff|".format(ident))
        else:
            self.objet.mnemonic = msg
            self.actualiser()
