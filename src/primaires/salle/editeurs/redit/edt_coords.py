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


"""Fichier contenant le contexte éditeur EdtCoords"""

import re

from primaires.interpreteur.editeur.uniligne import Uniligne

# Constantes
COORDS_VALIDE = r"^-?[0-9]+\.-?[0-9]+\.-?[0-9]+$"

class EdtCoords(Uniligne):
    
    """Classe définissant le contexte éditeur 'coords'.
    Ce contexte permet d'éditer les coordonnées de la salle.
    
    """
    
    def interpreter(self, msg):
        """Interprétation du message"""
        msg = msg.lower()
        if msg == "inv":
            self.objet.coords.valide = False
            self.actualiser()
        elif not re.search(COORDS_VALIDE, msg):
            self.pere.envoyer("|err|Ces coordonnées sont invalides. " \
                    "Veuillez réessayer.|ff|")
        else:
            # On va découper msg
            # Grâce aux regex, on est sûr d'avoir le bon format
            x, y, z = msg.split(".")
            try:
                x, y, z = int(x), int(y), int(z)
            except ValueError:
                self.pere.envoyer("|err|Ces coordonnées sont invalides. " \
                    "Veuillez réessayer.|ff|")
            else:
                if (x, y, z) in type(self).importeur.salle:
                    self.pere.envoyer("|err|Ces coordonnées sont déjà " \
                            "utilisées dans l'univers.|ff|")
                else:
                    self.objet.coords.x = x
                    self.objet.coords.y = y
                    self.objet.coords.z = z
                    self.objet.coords.valide = True
                    self.actualiser()
