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


"""Package contenant la commande 'distinction'"""

from primaires.interpreteur.commande.commande import Commande

class CmdDistinction(Commande):
    
    """Commande 'distinction'.
    
    """
    
    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "distinction", "distinction")
        self.groupe = "joueur"
        self.schema = "(<message>)"
        self.aide_courte = "manipule votre distinction anonyme"
        self.aide_longue = \
            "Cette commande permet d'afficher ou de modifier votre " \
            "distinction anonyme. Il s'agit de la description que verront " \
            "les autres personnages quand vous ferez une action. " \
            "En effet, les personnages ne vous connaissant pas ne voient " \
            "pas votre nom mais la distinction anonyme que vous spécifiez. " \
            "Votre destinction pourrait être, par exemple : |ent|un jeune nain|ff|. " \
            "Entrez la commande %distinction% sans argument pour voir votre " \
            "distinction anonyme actuelle. Si vous précisez un argument à la commande " \
            "%distinction%, votre distinction anonyme sera modifiée."
    
    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        if dic_masques["message"] is not None:
            message = dic_masques["message"].message
        print("A compléter...")
