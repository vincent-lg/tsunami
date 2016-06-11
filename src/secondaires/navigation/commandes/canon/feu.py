# -*-coding:Utf-8 -*

# Copyright (c) 2010-2016 LE GOFF Vincent
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


"""Fichier contenant le paramètre 'feu' de la commande 'canon'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmFeu(Parametre):

    """Commande 'canon feu'.

    """

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "feu", "fire")
        self.aide_courte = "fait détonner le canon"
        self.aide_longue = \
            "Cette commande permet de faire détonner un canon " \
            "présent dans la salle où vous vous trouvez. Celui-ci doit " \
            "avoir été chargé en projectile (%canon% %canon:charger%) " \
            "et poudre (%canon% %canon:poudre%). La quantité de poudre, " \
            "sa puissance, le poids du projectile et d'autres facteurs " \
            "déterminent la course du boulet."

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        salle = personnage.salle
        personnage.agir("manip_canon")
        canon = None
        if hasattr(salle, "navire"):
            for element in salle.elements:
                if element.nom_type == "canon":
                    canon = element
                    break

        if canon is None:
            personnage << "|err|Aucun canon ne se trouve ici.|ff|"
            return

        if canon.onces == 0:
            personnage << "|err|Ce canon n'est pas chargé en poudre.|ff|"
            return

        if canon.projectile is None:
            personnage << "|err|Ce canon ne contient pas de projectile.|ff|"
            return

        # Si le joueur doit pouvoir enflammer le canon, mettre le code ici
        canon.tirer(auteur=personnage)
