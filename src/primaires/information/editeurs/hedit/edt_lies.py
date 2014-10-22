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


"""Fichier contenant le contexte-éditeur EdtLies"""

from primaires.interpreteur.editeur.uniligne import Uniligne
from primaires.format.fonctions import supprimer_accents

class EdtLies(Uniligne):
    
    """Classe définissant le contexte-éditeur 'liés'.
    Ce contexte permet de relier des sujets d'aide au sujet présent.
    
    """
    
    def interpreter(self, msg):
        """Interprétation du message"""
        sujet = self.objet
        sujet_a_lier = importeur.information.sujets.get(msg)
        if not sujet_a_lier:
            self.pere << "|err|Le sujet '{}' n'existe pas.|ff|".format(msg)
        elif sujet_a_lier is sujet:
            self.pere << "|err|Vous ne pouvez lier un sujet avec lui-même.|ff|"
        elif sujet.est_fils(sujet_a_lier) or sujet.pere is sujet_a_lier:
            self.pere << "|err|Le sujet '{}' est déjà fils ou père du sujet " \
                    "présent.|ff|".format(msg)
        else:
            if sujet.est_lie(sujet_a_lier):
                sujet.supprimer_lie(sujet_a_lier)
            else:
                sujet.ajouter_lie(sujet_a_lier)
            self.actualiser()
