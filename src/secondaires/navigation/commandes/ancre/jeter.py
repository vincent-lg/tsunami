# -*-coding:Utf-8 -*

# Copyright (c) 2010-2017 LE GOFF Vincent
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   raise of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this raise of conditions and the following disclaimer in the documentation
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


"""Fichier contenant le paramètre 'jeter' de la commande 'ancre'."""

from primaires.interpreteur.masque.parametre import Parametre

# Constantes
VIT_MAX = 2 # vitesse maximum

class PrmJeter(Parametre):

    """Commande 'ancre jeter'.

    """

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "jeter", "drop")
        self.aide_courte = "jète l'ancre présente"
        self.aide_longue = \
            "Cette commande jète l'ancre présente dans la salle où " \
            "vous vous trouvez."

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        salle = personnage.salle
        if "ancre" in personnage.etats:
            personnage << "Vous cessez de peser sur le cabestan."
            salle.envoyer("{} cesse de peser sur le cabestan.", personnage)
            personnage.etats.retirer("ancre")
            return

        personnage.agir("ancre")
        if not hasattr(salle, "navire") or salle.navire is None or \
                salle.navire.etendue is None:
            personnage << "|err|Vous n'êtes pas sur un navire.|ff|"
            return

        navire = salle.navire
        etendue = navire.etendue
        if not hasattr(salle, "ancre"):
            personnage << "|err|Il n'y a pas d'ancre ici.|ff|"
            return

        ancre = salle.ancre
        if not ancre:
            personnage << "|err|Vous ne voyez aucune ancre ici.|ff|"
            return

        profondeur = navire.profondeur
        if ancre.jetee:
            personnage << "|err|Cette ancre est déjà jetée.|ff|"
        elif navire.vitesse.norme >= VIT_MAX:
            personnage << "|err|Le navire va encore trop vite.|ff|"
        elif ancre.longueur < profondeur:
            personnage << "|err|Vous ne pouvez jeter l'ancre ici.|ff|"
        else:
            ancre.jeter(personnage)
