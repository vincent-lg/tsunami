# -*-coding:Utf-8 -*

# Copyright (c) 2014 LE GOFF Vincent
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


"""Fichier contenant le paramètre 'créer' de la commande 'familier'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmCreer(Parametre):

    """Commande 'familier créer'.

    """

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "créer", "create")
        self.nom_groupe = "administrateur"
        self.schema = "<cle>"
        self.aide_courte = "crée une fiche de familier"
        self.aide_longue = \
                "Cette commande permet de créer une fiche de familier. " \
                "Le seul paramètre à préciser est la clé de la fiche " \
                "qui doit être identique à la clé du prototype de " \
                "PNJ que vous souhaitez utiliser. Par exemple, si " \
                "vous voulez créer un familier modelé sur 'cheval', " \
                "vous devez créer une fiche de familier de même clé " \
                "que le prototype de PNJ."

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        cle = dic_masques["cle"].cle
        if cle in importeur.familier.fiches:
            personnage << "|err|La fiche de familier {} existe " \
                    "déjà.|ff|".format(cle)
            return

        try:
            prototype = importeur.pnj.prototypes[cle]
        except KeyError:
            personnage << "|err|Le prototype de PNJ {} est introuvable." \
                    "|ff|".format(cle)
            return

        fiche = importeur.familier.creer_fiche_familier(cle)
        editeur = type(self).importeur.interpreteur.construire_editeur(
                "famedit", personnage, fiche)
        personnage.contextes.ajouter(editeur)
        editeur.actualiser()
