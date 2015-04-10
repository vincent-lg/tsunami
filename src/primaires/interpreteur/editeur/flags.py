# -*-coding:Utf-8 -*

# Copyright (c) 2013 LE GOFF Vincent
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


"""Ce fichier définit le contexte-éditeur 'flags'.

À la différence du contexte-éditeur 'flag', celui-ci permet d'éditer
plusieurs flags contenus dans un même attribut, un entier. On
doit préciser les flags sous la forme d'un dictionnaire {nom: valeur},
les valeurs étant toutes des résultats de l'expression 2 ^N (0 pour aucun,
1, 2, 4, 8, 16, 32...).

"""

from primaires.format.fonctions import oui_ou_non
from . import Editeur

class Flags(Editeur):

    """Contexte-éditeur flags.

    Ce contexte éditeur permet d'éditer les flags d'un unique attribut.
    Entrer le flag une première fois l'active, entrer son nom une
    seconde fois le désactive.

    """

    nom = "editeur:base:flags"

    def __init__(self, pere, objet=None, attribut=None, flags=None):
        """Constructeur de l'éditeur."""
        Editeur.__init__(self, pere, objet, attribut)
        self.flags = flags or {}

    def accueil(self):
        """Message d'accueil du contexte."""
        msg = self.aide_courte.format(objet=self.objet) + "\n\n"
        msg += "Flags actuels :"
        flags = sorted(self.flags.items())
        flag = getattr(self.objet, self.attribut)
        for nom, valeur in flags:
            msg += "\n  " + nom.capitalize().ljust(20)
            actif = flag & valeur != 0
            msg += " : " + oui_ou_non(actif)

        return msg

    @staticmethod
    def afficher_apercu(apercu, objet, valeur, flags):
        """Affichage de l'aperçu."""
        flags = sorted(flags.items())
        flag = valeur
        actifs = []
        for nom, valeur in flags:
            actif = flag & valeur != 0
            if actif:
                actifs.append(nom)

        if actifs:
            valeur = ", ".join(actifs)
            Valeur = valeur.capitalize()
        else:
            valeur = "|att|aucun|ff|"
            Valeur = "|att|Aucun|ff|"

        return apercu.format(objet=objet, valeur=valeur, Valeur=Valeur)

    def interpreter(self, msg):
        """Interprétation du message."""
        msg = msg.lower()
        flags = self.flags
        if msg in flags:
            setattr(self.objet, self.attribut, getattr(
                    self.objet, self.attribut) ^ flags[msg])
            self.actualiser()
        else:
            self.pere << "|err|Ce flag est introuvable.|ff|"
