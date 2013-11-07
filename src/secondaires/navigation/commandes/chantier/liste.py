# -*-coding:Utf-8 -*

# Copyright (c) 2013 LE GOFF Vincent
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


"""Fichier contenant le paramètre 'liste' de la commande 'chantier'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmListe(Parametre):

    """Commande 'chantier liste'.

    """

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "liste", "list")
        self.aide_courte = "consulte vos navires"
        self.aide_longue = \
            "Cette commande vous permet de consulter la liste des navires " \
            "que vous possédez, si ils se trouvent dans les eaux du chantier " \
            "naval dans lequel vous vous trouvez. Si le navire sur " \
            "lequel vous souhaitez effectuer une opération (changer son " \
            "nom par exemple), il doit se trouver dans le chantier " \
            "naval. Cette commande affiche la liste avec chaque navire " \
            "numéroté. Ces numéros vous permettront d'effectuer d'autres " \
            "actions dans le chantier naval et vous devrez le préciser " \
            "lors des autres commandes."

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        salle = personnage.salle
        chantier = importeur.navigation.get_chantier_naval(salle)
        if chantier is None:
            personnage << "|err|Vous ne vous trouvez pas dans un chantier " \
                    "naval.|ff|"
            return

        if salle.magasin is None:
            personnage << "|err|Vous ne vous trouvez pas dans un chantier " \
                    "naval.|ff|"
            return

        magasin = salle.magasin
        if magasin.vendeur is None:
            personnage << "|err|Aucun vendeur n'est présent pour l'instant.|ff|"
            return

        navires = chantier.get_navires_possedes(personnage)
        if navires:
            en_tete = "+-" + "-" * 2 + "-+-" + "-" * 25 + "-+-" + "-" * 25 + \
                    "-+"
            msg = en_tete + "\n"
            msg += "| ID | " + "Type".ljust(25) + " | "
            msg += "Nom".ljust(25) + " |\n" + en_tete
            for i, navire in enumerate(navires):
                msg += "\n| " + "{:>2} | ".format(i + 1)
                msg += navire.nom.ljust(25) + " | "
                if navire.nom_personnalise:
                    nom_personnalise = navire.nom_personnalise
                else:
                    nom_personnalise = "Non précisé"

                msg += nom_personnalise.ljust(25) + " |"
            msg += "\n" + en_tete
            personnage << msg
        else:
            personnage << "Vous n'avez aucun navire dans ce " \
                    "chantier naval."
