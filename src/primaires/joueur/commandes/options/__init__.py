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


"""Package contenant la commande 'options' et ses sous-commandes.
Dans ce fichier se trouve la commande même.

"""

from primaires.interpreteur.commande.commande import Commande
from .chmdp import PrmChmdp
from .couleur import PrmCouleur
from .encodage import PrmEncodage
from .langue import PrmLangue
from .newsletter import PrmNewsletter
from .voir import PrmVoir

class CmdOptions(Commande):
    
    """Commande 'options'.
    
    """
    
    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "options", "options")
        self.groupe = "joueur"
        self.aide_courte = "change vos options de compte et joueur"
        self.aide_longue = \
            "Cette commande permet de manipuler les options de votre " \
            "joueur et de votre compte. Tapez %options% sans paramètrse " \
            "pour voir les options disponibles, ou lisez l'aide des " \
            "sous-commandes ci-dessous."
    
    def ajouter_parametres(self):
        """Ajout des paramètres"""
        prm_couleur = PrmCouleur()
        prm_encodage = PrmEncodage()
        prm_langue = PrmLangue()
        prm_newsletter = PrmNewsletter()
        prm_voir = PrmVoir()
        prm_chmdp = PrmChmdp()
        
        self.ajouter_parametre(prm_couleur)
        self.ajouter_parametre(prm_encodage)
        self.ajouter_parametre(prm_langue)
        self.ajouter_parametre(prm_newsletter)
        self.ajouter_parametre(prm_voir)
        self.ajouter_parametre(prm_chmdp)
