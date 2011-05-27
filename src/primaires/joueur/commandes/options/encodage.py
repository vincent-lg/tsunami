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


"""Fichier contenant le paramètre 'encodage' de la commande 'options'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmEncodage(Parametre):
    
    """Commande 'options encodage'.
    
    """
    
    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "encodage", "encoding")
        self.schema = "<nom_encodage>"
        self.aide_courte = "change l'encodage du compte"
        self.aide_longue = \
            "Cette commande permet de changer l'encodage de votre " \
            "compte. Cette commande influencera les autres joueurs de " \
            "votre compte puisqu'il est présupposé qu'ils sont connecté " \
            "du même point. Vous devez lui préciser en paramètre un nom " \
            "d'encodage comme |ent|utf-8|ff| par exemple."
    
    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        encodage = dic_masques["nom_encodage"].encodage
        anc_encodage = personnage.compte.encodage
        if encodage == anc_encodage:
            personnage << "|err|Votre encodage est déjà réglé sur {}.|ff|" \
                    .format(encodage)
        else:
            personnage.compte.encodage = encodage
            personnage << "Vous changez l'encodage du compte de {} à {}." \
                    .format(anc_encodage, encodage)
