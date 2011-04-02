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


"""Fichier contenant le paramètre 'langue' de la commande 'options'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmLangue(Parametre):
    
    """Commande 'options langue'.
    
    """
    
    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "lang", "lang")
        self.schema = "<langue>"
        self.aide_courte = "change la langue du joueur"
        self.aide_longue = \
            "Cette commande permet de changer la langue d'affichage des " \
            "commandes de votre joueur. Vous pouvez choisir des commandes " \
            "en |ent|anglais|ff| ou en |ent|français|ff| selon votre " \
            "choix. Précisez en paramètre le nom de la langue."
    
    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        langue = dic_masques["langue"].langue
        anc_langue = personnage.langue_cmd
        personnage.langue_cmd = langue
        personnage << "Vous changez la langue du joueur de {} à {}.".format(
                anc_langue, langue)
