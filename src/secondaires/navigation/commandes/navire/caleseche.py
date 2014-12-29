# -*-coding:Utf-8 -*

# Copyright (c) 2014 LE GOFF Vincent
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


"""Fichier contenant le paramètre 'calesèche' de la commande 'navire'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmCaleseche(Parametre):

    """Commande 'navire calesèche'.

    """

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "calesèche", "dryhold")
        self.tronquer = True
        self.schema = "(<cle_navire>)"
        self.aide_courte = "met le navire en cale sèche"
        self.aide_longue = \
            "Cette commande permet de mettre en cale sèche le navire. " \
            "Le navire doit être précisé en paramètre sous la forme " \
            "de son identifiant : " \
            "si le navire n'est pas précisé, essaye de mettre en " \
            "cale sèche le navire sur lequel vous vous trouvez. Le " \
            "chantier navale correspondant à l'étendue sera recherché " \
            "parmi les chantiers existants."

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        navire = dic_masques["cle_navire"]
        salle = personnage.salle
        if navire is None:
            if not hasattr(salle, "navire") or salle.navire is None:
                personnage << "|err|Vous n'êtes pas sur un navire.|ff|"
                return

            navire = salle.navire
        else:
            navire = navire.navire

        try:
            navire.mettre_en_cale_seche()
        except ValueError as err:
            personnage << str(err)
        else:
            personnage << "Le navire {} a bien été mis en cale sèche.".format(
                    navire.cle)
