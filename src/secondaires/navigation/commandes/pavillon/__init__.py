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


"""Package contenant la commande 'pavillon'."""

from primaires.interpreteur.commande.commande import Commande
from .hisser import PrmHisser
from .montrer import PrmMontrer
from .retirer import PrmRetirer

class CmdPavillon(Commande):

    """Commande 'pavillon'"""

    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "pavillon", "flag")
        self.nom_categorie = "navire"
        self.aide_courte = "manipule le pavillon"
        self.aide_longue = \
            "Cette commande permet de manipuler le pavillon. Un " \
            "pavillon est un large pan de tissu que l'on peut hisser " \
            "en tête de mât. Il sera visible par les autres navires. " \
            "Les couleurs que vous montrerez pourront influer sur " \
            "la décision d'autres navires : les marchands auront " \
            "tendance à fuir devant un pavillon pirate, par exemple. " \
            "Certains ports auront des instructions spécifiques en " \
            "fonction des couleurs affichées et pourront décider " \
            "d'ordonner aux défenses du port d'éliminer le navire " \
            "si les couleurs ne sont pas celles attendues ou si elles " \
            "sont ouvertement hostiles. Au-delà des commandes pour " \
            "hisser (%pavillon% %pavillon:hisser%) et baisser " \
            "(%pavillon% %pavillon:retirer%) un pavillon, vous pouvez " \
            "aussi simplement faire des signaux avec (%pavillon% " \
            "%pavillon:montrer%) ce qui permet de signaler des intentions " \
            "avec des équipages amis et de convenir de signaux entre " \
            "officiers de différents navires."

    def ajouter_parametres(self):
        """Ajout des paramètres."""
        self.ajouter_parametre(PrmHisser())
        self.ajouter_parametre(PrmMontrer())
        self.ajouter_parametre(PrmRetirer())
