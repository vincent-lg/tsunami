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


"""Fichier contenant le paramètre 'descendre' de la commande 'canot'."""

from primaires.format.fonctions import contient

from primaires.interpreteur.masque.parametre import Parametre

class PrmDescendre(Parametre):

    """Commande 'canot descendre'."""

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "descendre", "lower")
        self.schema = "<texte_libre>"
        self.aide_courte = "descend un canot"
        self.aide_longue = \
            "Cette commande permet de descendre un canot qui se trouve " \
            "sur le pont du navire où vous vous trouvez. Vous devez " \
            "vous tenir près d'un bossoir, permettant de faire descendre " \
            "le canot. Vous aurez sans doute besoin d'être plusieurs " \
            "pour cette opération. Précisez en paramètre le nom du " \
            "canot à descendre."

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre."""
        salle = personnage.salle
        personnage.agir("manip_canot")
        texte = dic_masques["texte_libre"].texte

        if not getattr(salle, "navire", None):
            personnage << "|err|Vous n'êtes pas sur un navire.|ff|"
            return

        navire = salle.navire
        if not navire.etendue:
            personnage << "|err|Vous n'êtes pas sur un navire.|ff|"
            return

        if not salle.get_element("bossoir"):
            personnage << "|err|Il n'y a pas de bossoir ici.|ff|"
            return

        # Recherche du canot
        canot = None
        for t_canot in navire.canots:
            if contient(t_canot.nom, texte):
                canot = t_canot
                break

        if canot is None:
            personnage << "|err|Impossible de trouver ce canot.|ff|"
            return

        navire.descendre_canot(canot)
        personnage << "Vous mettez {} à l'eau.".format(canot.nom)
