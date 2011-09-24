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


"""Package contenant la commande 'prompt'.
Dans ce fichier ne se trouve que la commande.
Les sous-commandes peuvent être trouvées dans le package.

"""

from primaires.interpreteur.commande.commande import Commande

from .defaut import PrmDefaut

class CmdPrompt(Commande):
    
    """Commande 'prompt'.
    
    """
    
    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "prompt", "prompt")
        self.schema = ""
        self.aide_courte = "affiche ou configure votre prompt"
        self.aide_longue = \
            "Cette commande permet d'afficher ou configurer vos " \
            "différents prompts. les prompts sont des messages qui " \
            "apparaissent régulièrement pour vous signaler, par défaut, " \
            "les principales stats de votre personnage (sa vitalité, " \
            "sa mana, son endurance). Chaque prompt se voit attribuer " \
            "une sous-commande de %prompt%. Si vous entrez cette " \
            "sous-commande, vous verrez le prompt actuel. Si vous " \
            "entrez un prompt à la suite, vous modifierez le prompt actuel."
    
    def ajouter_parametres(self):
        """Ajoute les paramètres à la commande."""
        prm_defaut = PrmDefaut()
        
        self.ajouter_parametre(prm_defaut)
