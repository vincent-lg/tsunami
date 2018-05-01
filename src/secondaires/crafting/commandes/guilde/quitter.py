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
# ARE DISCLAIMED. IN NO Eguilde SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""Fichier contenant le paramètre 'quitter' de la commande 'guilde'."""

from primaires.interpreteur.masque.parametre import Parametre
from secondaires.crafting.exception import ExceptionCrafting

class PrmQuitter(Parametre):

    """Commande 'guilde quitter'."""

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "quitter", "leave")
        self.schema = "<cle> (<nom_joueur>)"
        self.aide_courte = "quitte une guilde"
        self.aide_longue = \
            "Cette commande permet de forcer un joueur à quitter " \
            "une guilde. Vous devez préciser en premier " \
            "paramètre obligatoire la clé de la guilde. Le second " \
            "paramètre, facultatif, est le nom du joueur. Si ce " \
            "second paramètre n'est pas renseigné, cette commande " \
            "s'applique automatiquement à vous."

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        cle = dic_masques["cle"].cle
        try:
            guilde = importeur.crafting.guildes[cle]
        except KeyError:
            personnage << "|err|La clé de guilde {} n'existe pas.|ff|".format(
                    repr(cle))
            return

        joueur = dic_masques["nom_joueur"]
        if joueur:
            joueur = joueur.joueur
        else:
            joueur = personnage

        try:
            guilde.quitter(joueur)
        except ExceptionCrafting as err:
            msg = str(err).capitalize()
            personnage << "|err|" + msg + ".|ff|"
        else:
            personnage << "Le joueur {} a bien quitté la guilde {}.".format(
                    joueur.nom, guilde.cle)
