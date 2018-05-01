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


"""Fichier contenant le paramètre 'liste' de la commande 'cale'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmListe(Parametre):

    """Commande 'cale liste'.

    """

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "liste", "list")
        self.aide_courte = "liste le contenu de la cale"
        self.aide_longue = \
            "Cette commande vous permet de lister le contenu de la cale. " \
            "C'est une liste probablement partielle, cependant, puisque " \
            "vous ne pouvez pas voir toute la cale du même point du " \
            "navire. La cale n'est cependant pas propre à une salle : si " \
            "il se trouve deux soutes aux poudres dans le navire par " \
            "exemple, vous verrez la quantité totale de boulets et de " \
            "poudre dans les deux, pas une mesure différente pour chacune."

    def interpreter(self, personnage, dic_masques):
        """Méthode dinterprétation."""
        salle = personnage.salle
        if getattr(salle, "navire", None) is None:
            personnage << "|err|Vous ne vous trouvez pas sur un navire.|ff|"
            return
        elif not salle.cales:
            personnage << "|err|Il n'y a pas de cale que vous puissiez " \
                    "manipuler ici.|ff|"
            return

        msg = ""
        cale = salle.navire.cale
        for nom in sorted(salle.cales):
            noms = cale.get_noms(nom)
            msg += "\n" + nom.capitalize() + " :"
            if noms:
                for nom in noms:
                    msg += "\n  " + nom
            else:
                msg += "\n  Aucun"

        msg = msg.lstrip("\n") + "\n\n"

        # Affichage du poids
        facteur = (cale.poids / cale.poids_max) * 100
        if facteur < 7:
            msg += "Cette cale est vide, ou peu s'en faut"
        elif facteur < 25:
            msg += "Cette cale n'est pas même remplie au quart"
        elif facteur < 33:
            msg += "Cette cale est remplie au quart"
        elif facteur < 50:
            msg += "Cette cale ets remplie au tiers"
        elif facteur < 67:
            msg += "Cette cale est à moitié remplie"
        elif facteur < 75:
            msg += "Cette cale est remplie aux deux tiers"
        elif facteur < 85:
            msg += "Cette cale est remplie aux trois quarts"
        elif facteur < 99:
            msg += "Cette cale est presque pleine"
        else:
            msg += "Cette cale est pleine à craquer"

        if personnage.est_immortel():
            msg += " ({}%)".format(int(facteur))

        msg += "."
        personnage << msg
