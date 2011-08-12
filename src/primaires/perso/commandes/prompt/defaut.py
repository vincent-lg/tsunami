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


"""Fichier contenant le paramètre 'defaut' de la commande 'prompt'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmDefaut(Parametre):
    
    """Commande 'prompt defaut'.
    
    """
    
    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "défaut", "default")
        self.schema = "(<prompt>)"
        self.aide_courte = "prompt par défaut"
        self.aide_longue = \
            "Sans paramètre, affiche votre prompt par défaut. Si " \
            "un prompt est précisé en paramètre, remplace le prompt actuel."
    
    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        prompt = dic_masques["prompt"] or None
        nt_stats = type(self).importeur.perso.stats_symboles()
        if prompt:
            prompt = prompt.prompt
            prompt = prompt.replace("{", "{{")
            prompt = prompt.replace("}", "}}")
            for stat in type(self).importeur.perso.modele_stats:
                prompt = prompt.replace("%{}".format(stat.symbole),
                        "{stats." + stat.nom + "}")
            personnage._prompt = prompt
            personnage << \
                "Votre prompt par défaut a bien été mis à jour :\n" + \
                personnage._prompt.format(stats=nt_stats)
        else:
            personnage << personnage._prompt.format(stats=nt_stats)
