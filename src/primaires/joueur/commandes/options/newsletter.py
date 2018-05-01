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


"""Fichier contenant le paramètre 'newsletter' de la commande 'options'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmNewsletter(Parametre):
    
    """Commande 'options newsletter'.
    
    """
    
    def __init__(self):
        """Constructeur du paramètre."""
        Parametre.__init__(self, "newsletter", "newsletter")
        self.tronquer = True
        self.schema = "<etat>"
        self.aide_courte = "active / désactive la newsletter"
        self.aide_longue = \
            "Cette commande permet d'activer ou désactiver l'envoi de la " \
            "newsletter à ce compte. Si cette option est active, les " \
            "newsletters envoyées par les administrateurs seront envoyées " \
            "à ce compte. Elles ne seront pas envoyées si l'option est " \
            "désactivée. " \
            "Si la newsletter vous gène ou vous est inutile, " \
            "vous pouvez donc la désactiver en entrant %options% " \
            "%options:newsletter% |cmd|off|ff|. Remplacez |cmd|off|ff| " \
            "par |cmd|on|ff| pour voir de nouveau les newsletters."
   
    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre."""
        etat = dic_masques["etat"].flag
        if personnage.compte.newsletter == etat:
            personnage << "|att|C'est déjà le cas.|ff|"
        else:
            personnage.compte.newsletter = etat
            if etat:
                personnage << "Envoi des newsletters activé."
            else:
                personnage << "Envoi des newsletters désactivé."
