# -*-coding:Utf-8 -*

# Copyright (c) 2010-2016 LE GOFF Vincent
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


"""Package contenant la commande 'sorties'."""

from primaires.interpreteur.commande.commande import Commande

class CmdSorties(Commande):

    """Commande 'sorties'"""

    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "sorties", "exits")
        self.nom_categorie = "bouger"
        self.aide_courte = "Affiche les sorties autour de vous"
        self.aide_longue = \
            "Cette commande vous permet de voir les sorties disponibles " \
            "autour de vous. C'est une commande très utile pour " \
            "l'exploration, qui peut s'avérer plus que pratique si " \
            "vous êtes perdus sans lumière et que vous ne trouvez " \
            "pas la sortie par laquelle vous êtes entrés."

    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        retour = "Sorties visibles :"
        for sortie in personnage.salle.sorties:
            if personnage.est_immortel() or not sortie.cachee:
                if sortie.porte is None or sortie.porte.ouverte:
                    if sortie.salle_dest.voit_ici(personnage):
                        retour += "\n  {} vers {}".format(
                                sortie.nom_complet.capitalize(),
                                sortie.salle_dest.titre.lower())
                    else:
                        retour += "\n  Il fait trop sombre vers {}...".format(
                                sortie.nom_complet)
                else:
                    retour += "\n  La sortie est fermée vers {}.".format(
                            sortie.nom_complet)

        personnage.envoyer(retour)
