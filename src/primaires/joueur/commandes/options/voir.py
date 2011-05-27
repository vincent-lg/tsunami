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


"""Fichier contenant le paramètre 'voir' de la commande 'options'."""

from primaires.interpreteur.masque.parametre import Parametre
from reseau.connexions.client_connecte import ENCODAGES
from primaires.format.fonctions import oui_ou_non

class PrmVoir(Parametre):
    
    """Commande 'options voir'.
    
    """
    
    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "voir", "view")
        self.schema = ""
        self.aide_courte = "visualise les options du joueur"
        self.aide_longue = \
            "Cette commande permet de voir l'état actuel des options que " \
            "vous pouvez éditer avec la commande %options%. Elle donne aussi " \
            "un aperçu des valeurs disponibles."
    
    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        langue = personnage.langue_cmd
        encodage = personnage.compte.encodage
        res = "Options actuelles :\n\n"
        res += "  Couleurs : {}\n".format(oui_ou_non(
                personnage.compte.couleur))
        res += "  Votre encodage : |ent|" + encodage + "|ff|.\n"
        res += "  Encodages disponibles : |ent|" + "|ff|, |ent|". \
            join(ENCODAGES) + "|ff|.\n\n"
        res += "  Votre langue : |ent|" + langue + "|ff|.\n"
        res += "  Langues disponibles : |ent|français|ff|, " \
            "|ent|anglais|ff|."
        personnage << res
