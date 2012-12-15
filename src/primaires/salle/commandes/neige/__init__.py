# -*-coding:Utf-8 -*

# Copyright (c) 2012 LE GOFF Vincent
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


"""Package contenant la commande 'neige' et ses sous-commandes.

Dans ce fichier se trouve la commande même.

"""

from primaires.interpreteur.commande.commande import Commande
from .creer import PrmCreer
from .detruire import PrmDetruire
from .edit import PrmEdit
from .fabriquer import PrmFabriquer
from .installer import PrmInstaller
from .poursuivre import PrmPoursuivre
from .retirer import PrmRetirer

class CmdNeige(Commande):
    
    """Commande 'neige'.
    
    """
    
    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "neige", "snow")
        self.aide_courte = "gère la construction dans la neige"
        self.aide_longue = \
            "Cette commande permet la construction de bonhommes " \
            "de neige et de boule de neige. Voir plus en détail " \
            "la commande %neige:fabriquer%."
    
    def ajouter_parametres(self):
        """Ajout des paramètres"""
        self.ajouter_parametre(PrmCreer())
        self.ajouter_parametre(PrmDetruire())
        self.ajouter_parametre(PrmEdit())
        self.ajouter_parametre(PrmFabriquer())
        self.ajouter_parametre(PrmInstaller())
        self.ajouter_parametre(PrmPoursuivre())
        self.ajouter_parametre(PrmRetirer())
