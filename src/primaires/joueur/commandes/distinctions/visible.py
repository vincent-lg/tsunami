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


"""Fichier contenant le paramètre 'visible' de la commande 'distinctions'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmVisible(Parametre):
    
    """Commande 'distinctions visible'.
    
    """
    
    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "visible", "visible")
        self.schema = "(<message>)"
        self.aide_courte = "manipule la distinction visible"
        self.aide_longue = \
            "Cette commande permet, sans paramètre, d'afficher la " \
            "distinction anonyme visible de votre personnage. Cette " \
            "distinction est utilisée quand votre personnage fait une " \
            "action en étant visible. Pour la modifier, entrez " \
            "%distinctions% %distinctions:visible% |ent|<votre nouvelle " \
            "distinction>|ff|."
    
    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        message = ""
        if dic_masques["message"]:
            message = dic_masques["message"].message
        
        if message:
            # Change la distinction anonyme
            message = message[0].lower() + message[1:]
            personnage.distinction_visible = message
            personnage << "Votre distinction visible est à présent {}.".format(
                    message)
        else:
            personnage << "Votre distinction visible actuelle : {}.".format(
                    personnage.get_distinction_visible())
