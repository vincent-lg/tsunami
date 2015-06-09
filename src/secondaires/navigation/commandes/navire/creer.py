# -*-coding:Utf-8 -*

# Copyright (c) 2010 LE GOFF Vincent
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


"""Fichier contenant le paramètre 'créer' de la commande 'navire'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmCreer(Parametre):

    """Commande 'navire créer'.

    """

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "créer", "create")
        self.schema = "<modele_navire>"
        self.aide_courte = "crée un navire sur un modèle"
        self.aide_longue = \
                "Crée un navire sur un modèle existant. Cette commande " \
                "crée un navire mais ne le place dans aucune étendue d'eau."

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        # On récupère le modèle
        modele = dic_masques["modele_navire"].modele
        navire = importeur.navigation.creer_navire(modele)

        # Génération du graph
        if (len(navire.salles) ** 2 - len(navire.salles)) != \
                len(modele.graph):
            personnage << "Génération du graph du modèle {}.".format(
                    modele.cle)
            importeur.navigation.nav_logger.info(
                    "Calcul du graph du modèle de navire {}.".format(
                            modele.cle))
            modele.generer_graph()
            importeur.navigation.nav_logger.info(
                    "Génération du graph terminée.")

        personnage << "Le navire {} a bien été créé.".format(navire.cle)
