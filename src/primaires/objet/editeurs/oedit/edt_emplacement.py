# -*-coding:Utf-8 -*

# Copyright (c) 2010-2016 LE GOFF Vincent
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


"""Fichier contenant le contexte éditeur EdtEmplacement."""

from primaires.interpreteur.editeur.uniligne import Uniligne

class EdtEmplacement(Uniligne):
    
    """Classe définissant le contexte éditeur 'edt_emplacement'."""
    
    def __init__(self, pere, objet, attribut):
        Uniligne.__init__(self, pere, objet, attribut)
        self.ajouter_option("e", self.opt_epaisseur)
        self.ajouter_option("p", self.opt_positions)
    
    def opt_epaisseur(self, arguments):
        """Option épaisseur.
        
        Syntaxe :
            /e <épaisseur>
        
        """
        try:
            epaisseur = int(arguments)
        except ValueError:
            self.pere << "|err|Epaisseur invalide, spécifiez un nombre.|ff|"
        else:
            self.objet.epaisseur = epaisseur
            self.actualiser()
    
    def opt_positions(self, arguments):
        """Option positions.
        
        Syntaxe :
            /p <position1> (, <position2>, (...))
        
        """
        if not arguments.strip():
            self.pere << "|err|Entrez au moins une position ou plusieurs " \
                    "séparées par des virgules.|ff|"
            return
        
        arguments = arguments.split(",")
        positions = set()
        for arg in arguments:
            try:
                arg = arg.strip()
                position = int(arg)
            except ValueError:
                self.pere << "|err|Position invalide, spécifiez un " \
                        "nombre.|ff|"
                return
            else:
                positions.add(position)
        
        self.objet.positions = tuple(sorted(positions))
        self.actualiser()
    
    def accueil(self):
        """Retourne le message d'accueil."""
        msg = Uniligne.accueil(self)
        msg += "\nPositions actuelles : "
        
        positions = self.objet.positions
        if not positions:
            msg += "|rg|aucune|ff|"
        else:
            msg += ", ".join([str(p) for p in positions])
        
        return msg
