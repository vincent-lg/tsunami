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


"""Fichier contenant le paramètre 'voir' de la commande 'chemin'."""

from primaires.format.fonctions import oui_ou_non
from primaires.interpreteur.masque.parametre import Parametre
from primaires.pnj.chemin import FLAGS
class PrmVoir(Parametre):

    """Commande 'chemin voir'.

    """

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "voir", "view")
        self.schema = "<cle>"
        self.aide_courte = "affiche le détail d'un chemin"
        self.aide_longue = \
            "Cette commande permet d'obtenir plus d'informations sur " \
            "un chemin (ses flags actifs, ses salles et sorties...)."

    def ajouter(self):
        """Méthode appelée lors de l'ajout de la commande à l'interpréteur"""
        cle = self.noeud.get_masque("cle")
        cle.proprietes["regex"] = r"'[a-z0-9_:]{3,}'"

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        cle = dic_masques["cle"].cle
        if cle not in importeur.pnj.chemins:
            personnage << "|err|Ce chemin n'existe pas.|ff|"
            return

        chemin = importeur.pnj.chemins[cle]
        msg = "Détail sur le chemin {} :".format(chemin.cle)
        msg += "\n  Flags :"
        for nom_flag in FLAGS.keys():
            msg += "\n    {}".format(nom_flag.capitalize())
            msg += " : " + oui_ou_non(chemin.a_flag(nom_flag))
        msg += "\n  Salles du chemin :"
        if len(chemin.salles) == 0:
            msg += "\n    Aucune"
        else:
            for salle, direction in chemin.salles.items():
                msg += "\n    " + salle.ident.ljust(20) + " "
                msg += direction.ljust(10)
                if salle in chemin.salles_retour and \
                        chemin.salles_retour[salle]:
                    msg += " (retour " + chemin.salles_retour[salle] + ")"

        personnage << msg
