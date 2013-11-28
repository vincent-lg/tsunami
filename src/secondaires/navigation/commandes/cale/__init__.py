# -*-coding:Utf-8 -*

# Copyright (c) 2013 LE GOFF Vincent
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


"""Package contenant la commande 'cale'."""

from primaires.interpreteur.commande.commande import Commande
from .placer import PrmPlacer
from .retirer import PrmRetirer

class CmdCale(Commande):

    """Commande 'cale'"""

    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "cale", "hold")
        self.nom_categorie = "navire"
        self.aide_courte = "manipule la cale"
        self.aide_longue = \
            "Cette commande permet de placer des objets à fond de " \
            "cale. Tous les objets ne peuvent pas être mis en cale " \
            "et la cale n'est pas manipulable de partout sur le navire. " \
            "La cale est surtout faite pour conserver les vivres, les " \
            "marchandises, les boulets de canon, la poudre, certains " \
            "instruments (comme des écopes ou des tonneaux de poix). " \
            "Mettre ces objets à fond de cale a deux avantages : " \
            "d'abord, ils seront plus à l'abri qu'abandonnés sur le " \
            "pont. Si le navire est ancré ou amarré dans un port, " \
            "personne sauf le propriétaire du navire et les membres " \
            "d'équipage ne pourront retirer des marchandises de la " \
            "cale. Ensuite, l'équipage pourra accéder à ces marchandises " \
            ": les artilleurs ne touchent pas aux boulets de canon " \
            "sur le pont, se servant de préférance dans la cale. Les " \
            "charpentiers utiliseront la poix et les écopes disposés " \
            "dans la cale. Le maître cuisinier utilisera les vivres de " \
            "la cale. Si vous comptez utiliser des matelots sur votre " \
            "navire, passer par la cale est donc préférable."

    def ajouter_parametres(self):
        """Ajout des paramètres."""
        self.ajouter_parametre(PrmPlacer())
        self.ajouter_parametre(PrmRetirer())
