
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


"""Package contenant la commande 'plist'.

"""

from primaires.interpreteur.commande.commande import Commande

class CmdPlist(Commande):
    
    """Commande 'plist'.
    
    """
    
    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "plist", "plist")
        self.groupe = "administrateur"
        self.nom_categorie = "batisseur"
        self.aide_courte = "affiche la liste des prototypes de PNJ"
        self.aide_longue = \
            "Cette commande affiche une liste ordonnée des prototypes " \
            "de PNJ existant."
    
    def interpreter(self, personnage, dic_masques):
        """Interprétation de la commande"""
        prototypes = type(self).importeur.pnj.prototypes
        prototypes = [(identifiant, prototype.nom_singulier) \
                for identifiant, prototype in sorted(prototypes.items())]
        
        res = []
        for identifiant, nom in prototypes:
            res.append("{: <20} : {}".format(identifiant, nom))
        
        if not res:
            personnage << "|att|Aucun prototype n'a pu être trouvé.|ff|"
        else:
            personnage << "Liste des prototypes de PNJ existants :\n\n" + \
                    "\n".join(res)
