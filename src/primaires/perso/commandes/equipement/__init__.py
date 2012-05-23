
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


"""Package contenant la commande 'equipement'.

"""

from primaires.interpreteur.commande.commande import Commande

class CmdEquipement(Commande):
    
    """Commande 'equipement'.
    
    """
    
    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "equipement", "equipment")
        self.nom_categorie = "objets"
        self.aide_courte = "affiche votre équipement"
        self.aide_longue = \
                "Cette commande affiche votre équipement actuel, les " \
            "objets que vous portez ou ceux que vous équipez."
    
    def interpreter(self, personnage, dic_masques):
        """Interprétation de la commande"""
        equipement = personnage.equipement
        msg = ""
        objets = []
        for membre in equipement.membres:
            objet = membre.equipe and membre.equipe[-1] or membre.tenu
            if objet:
                objets.append("{} [{}]".format(membre.nom.capitalize(),
                        objet.get_nom()))
        
        if not objets:
            msg = "Vous ne portez rien actuellement."
        else:
            msg = "Votre équipement :\n\n  " + "\n  ".join(objets)
        
        personnage << msg
