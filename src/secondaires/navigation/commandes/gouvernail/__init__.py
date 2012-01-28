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


"""Package contenant la commande 'gouvernail'."""

from primaires.interpreteur.commande.commande import Commande
from .tenir import PrmTenir
from .relacher import PrmRelacher
from .droite import PrmDroite
from .gauche import PrmGauche
from .centre import PrmCentre

class CmdGouvernail(Commande):
    
    """Commande 'gouvernail'"""
    
    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "gouvernail", "tiller")
        self.nom_categorie = "navire"
        self.aide_courte = "manipule le gouvernail"
        self.aide_longue = \
            "Cette commande vous permet de tourner le gouvernail " \
            "vers tribord ou bâbord. Vous devez le tenir auparavant " \
            "(%gouvernail% %gouvernail:tenir%). Un gouvernail possède " \
            "5 degrés vers tribord et le même nombre vers bâbord. " \
            "Pour virer vers bâbord, entrez %gouvernail% " \
            "%gouvernail:gauche%. La barre sera alors inclinée vers " \
            "bâbord et le navire se mettra à tourner vers bâbord. " \
            "Pour le faire s'arrêter, vous devrez replacer la barre " \
            "droite en l'inclinant vers tribord (%gouvernail% " \
            "%gouvernail:droite%). Vous pouvez également utiliser la " \
            "commande %gouvernail% %gouvernail:centre% pour remettre " \
            "la barre droite. Les commandes %gouvernail% " \
            "%gouvernail:gauche% et %gouvernail:droite% peuvent " \
            "prendre en paramètre optionnel un nombre entre 1 et 5. " \
            "Cela permet d'incliner le gouvernail plus fortement et " \
            "ainsi, tourner plus vite. Pour relâcher le gouvernail, " \
            "entrez %gouvernail% %gouvernail:relâcher%. Si vous " \
            "le faites en marche, vous perdrez le contrôle du navire."
    
    def ajouter_parametres(self):
        """Ajout des paramètres."""
        self.ajouter_parametre(PrmGauche())
        self.ajouter_parametre(PrmDroite())
        self.ajouter_parametre(PrmCentre())
        self.ajouter_parametre(PrmTenir())
        self.ajouter_parametre(PrmRelacher())
