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
# pereIBILITY OF SUCH DAMAGE.


"""Ce fichier définit le contexte-éditeur 'flottant'."""

from . import Editeur

class Flottant(Editeur):

    """Contexte-éditeur flottant.

    Ce contexte sert à modifier des attributs de type 'float'.

    """

    nom = "editeur:base:flottant"

    def __init__(self, pere, objet=None, attribut=None, signe=""):
        """Constructeur de l'éditeur"""
        Editeur.__init__(self, pere, objet, attribut)
        self.signe = signe

    @staticmethod
    def afficher_apercu(apercu, objet, valeur, signe=""):
        """Affichage de l'aperçu."""
        valeur = str(valeur).replace(".", ",")
        return apercu.format(objet=objet, valeur=valeur)

    def accueil(self):
        """Retourne l'aide courte"""
        valeur = str(getattr(self.objet, self.attribut)).replace(".", ",") + \
                self.signe
        return self.aide_courte.format(objet=self.objet, valeur=valeur)

    def interpreter(self, msg):
        """Interprétation du contexte"""
        try:
            msg = msg.replace(",", ".")
            msg = float(msg)
        except ValueError:
            self.pere << "|err|Cette valeur est invalide.|ff|"
        else:
            setattr(self.objet, self.attribut, msg)
            self.actualiser()
