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


"""Fichier contenant le paramètre 'apparaître' de la commande 'familier'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmApparaitre(Parametre):

    """Commande 'familier apparaître'.

    """

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "apparaître", "spawn")
        self.nom_groupe = "administrateur"
        self.tronquer = True
        self.schema = "<cle>"
        self.aide_courte = "fait apparaître un familier"
        self.aide_longue = \
                "Cette commande permet de faire apparaître un familier " \
                "modelé sur la fiche de familier précisée en paramètre. " \
                "Souvenez-vous que la fiche de familier a la même clé que " \
                "le prototype de PNJ. Vous pouvez donc utliiser cette " \
                "commande comme %pspawn%, à ceci près qu'un PNJ sera " \
                "effectivement créé, mais qu'il s'agira d'un familier " \
                "et que vous en serez le maître."

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        cle = dic_masques["cle"].cle
        if cle not in importeur.familier.fiches:
            personnage << "|err|La fiche de familier {} n'existe " \
                    "pas.|ff|".format(cle)
            return

        fiche = importeur.familier.fiches[cle]
        salle = personnage.salle
        prototype = fiche.prototype
        if prototype.squelette is None:
            personnage << "|err|Ce prototype n'a aucun squelette défini.|ff|"
            return

        pnj = importeur.pnj.creer_PNJ(prototype)
        pnj.salle = salle
        familier = importeur.familier.creer_familier(pnj)
        familier.maitre = personnage
        salle.envoyer("{} apparaît du néant.".format(
                pnj.nom_singulier))
