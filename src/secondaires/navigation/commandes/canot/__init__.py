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


"""Package contenant la commande 'canot'."""

from primaires.interpreteur.commande.commande import Commande

from .descendre import PrmDescendre
from .hisser import PrmHisser

class CmdCanot(Commande):

    """Commande 'canot'"""

    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "canot", "dinghy")
        self.nom_categorie = "navire"
        self.aide_courte = "manipule les canots"
        self.aide_longue = \
            "Cette commande permet de manipuler les canots. Les canotts " \
            "sont de petites embarcations, principalement utiles " \
            "pour rejoindre des navires plus importants, dont le " \
            "tirant d'eau ne permet pas de s'amarrer contre un quai. Les " \
            "canots sont très utiles pour l'exploration de côtes " \
            "également. Ils peuvent être placés sur le pont d'un navire " \
            "et utilisés pour se rendre à terre ou explorer un rivage."

    def ajouter_parametres(self):
        """Ajout des paramètres."""
        self.ajouter_parametre(PrmDescendre())
        self.ajouter_parametre(PrmHisser())
