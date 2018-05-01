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


"""Package contenant la commande 'prompt'.
Dans ce fichier ne se trouve que la commande.
Les sous-commandes peuvent être trouvées dans le package.

"""

from primaires.interpreteur.commande.commande import Commande
from .defaut import PrmDefaut

# Constantes
AIDE = """
Cette commande permet de configurer vos différents prompts. Le prompt
est un message qui s'affiche généralement après l'entrée d'une commande ou une
action quelconque dans l'univers. Ce message donne des informations
générales sur votre personnage (par défaut, sa vitalité, mana et
endurance).
Il existe plusieurs prompts. Par exemple, celui que vous verrez à
votre première connexion est le prompt par défaut qui s'affiche dans
la plupart des circonstances. Il existe également un prompt de combat
qui est affiché quand votre personnage est en combat et peut donner
des informations supplémentaires.
Vous pouvez ici configurer votre prompt, c'est-à-dire changer ce
message. En utilisant une des sous-commandes ci-dessous, vous pouvez
soit consulter, masquer, modifier ou réinitialiser votre prompt.
Ce que vous entrez grâce à cette commande deviendra votre prompt. Vous
pouvez aussi utiliser des symboles (par exemple, vous pouvez entrer
%prompt% %prompt:défaut%|cmd| Vit(|pc|v) Man(|pc|m) End(|pc|e)|ff| pour
avoir un prompt sous la forme |ent|Vit(50) Man(50) End(50)|ff|.
Les symboles sont des combinaisons de lettres précédées du signe
pourcent (|pc|). Voici les symboles que vous pouvez utiliser pour tous
les prompts :
    |pc|v          Vitalité actuelle
    |pc|m          Mana actuelle
    |pc|e          Endurance actuelle
    |pc|vx         Vitalité maximum
    |pc|mx        Mana maximum
    |pc|ex         Endurance maximum
    |pc|sl         Saut de ligne (pour avoir un prompt sur deux lignes)
    |pc|f          Force
    |pc|a          Agilité
    |pc|r          Robustesse
    |pc|i          Intelligence
    |pc|c          Charisme
    |pc|s          Sensibilité
""".strip()

class CmdPrompt(Commande):

    """Commande 'prompt'.

    """

    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "prompt", "prompt")
        self.schema = ""
        self.aide_courte = "affiche ou configure votre prompt"
        self.aide_longue = AIDE

    def ajouter_parametres(self):
        """Ajout dynamique des paramètres."""
        for prompt in importeur.perso.prompts.values():
            self.ajouter_parametre(PrmDefaut(prompt))
