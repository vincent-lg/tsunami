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
# ARE DISCLAIMED. IN NO Ematelot SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""Fichier contenant le paramètre 'renommer' de la commande 'matelot'."""

from primaires.interpreteur.masque.parametre import Parametre
from secondaires.navigation.equipage.ordres.revenir import Revenir

class PrmRenommer(Parametre):

    """Commande 'matelot renommer'.

    """

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "renommer", "rename")
        self.schema = "<ancien:nom_matelot> <nouveau:nom_matelot>"
        self.tronquer = True
        self.aide_courte = "renomme un matelot"
        self.aide_longue = \
            "Cette commande permet de changer le nom d'un matelot. " \
            "Vous devez entrer en premier paramètre son ancien nom " \
            "et en second paramètre son nouveau nom (un mot seulement)."

    def ajouter(self):
        """Méthode appelée lors de l'ajout de la commande à l'interpréteur"""
        nouveau = self.noeud.get_masque("nouveau")
        nouveau.proprietes["nouveau"] = "True"

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        salle = personnage.salle
        navire = salle.navire
        matelot = dic_masques["ancien"].matelot
        nouveau_nom = dic_masques["nouveau"].nom_matelot.capitalize()
        equipage = navire.equipage
        if not navire.a_le_droit(personnage, "maître d'équipage"):
            personnage << "|err|Vous ne pouvez donner d'ordre sur ce " \
                    "navire.|ff|"
            return

        personnage << "{} se nomme désormais {}.".format(
                matelot.nom.capitalize(), nouveau_nom)
        equipage.renommer_matelot(matelot, nouveau_nom)
