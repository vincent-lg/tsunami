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


"""Package contenant le paramètre 'apparaître' de la commande 'navire_automatique'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmApparaitre(Parametre):

    """Commande 'navire_automatique apparaître'"""

    def __init__(self):
        """Constructeur du paramètre."""
        Parametre.__init__(self, "apparaître", "spawn")
        self.schema = "<cle>"
        self.aide_courte = "fait apparaître un navire automatique"
        self.aide_longue = \
            "Cette commande permet de faire apparaître un navire " \
            "automatique. Elle attend en paramètre la clé du navire " \
            "automatique. Selon cette fiche, le navire du modèle " \
            "indiqué sera créé, son équipage répartit, sa cale remplit, " \
            "son cap renseigné ainsi que d'autres actions automatiques."

    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        cle = dic_masques["cle"].cle
        if cle not in importeur.navigation.navires_automatiques:
            personnage << "|err|Cette clé de navire automatique " \
                    "est inconnue.|ff|"
            return

        navire_automatique = importeur.navigation.navires_automatiques[cle]
        navire = navire_automatique.creer()

        # Supprimer cette modification automatique du comportement
        navire.equipage.pirate = True

        personnage << "{} ({}) a bien été créé.".format(
                navire.desc_survol.capitalize(), navire.cle)
