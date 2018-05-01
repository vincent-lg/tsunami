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

"""Ce fichier définit le contexte-éditeur 'Uniligne'."""

from corps.fonctions import valider_cle
from . import Editeur

# Flags de vérification
CLE = 1

# Flags de modification
CAPITALIZE = 1
LOWER = 2

class Uniligne(Editeur):

    """Contexte-éditeur uni_ligne.

    Ce contexte sert à modifier des attributs de type 'str', conçu pour
    être écrits sur une ligne (le titre d'une salle, sa zone, son mnémonique...
    par exemple).

    """

    nom = "editeur:base:uniligne"

    def __init__(self, pere, objet=None, attribut=None,
            verification=0, modification=0):
        """Constructeur de l'éditeur"""
        Editeur.__init__(self, pere, objet, attribut)
        self.type = str
        self.verification = verification
        self.modification = modification

    def __getstate__(self):
        attrs = Editeur.__getstate__(self)
        attrs["type"] = attrs["type"].__name__
        return attrs

    def __setstate__(self, attrs):
        types = {
                "float": Float,
                "int": Int,
                "str": str,
        }

        attrs["type"] = types.get(attrs["type"], str)
        Editeur.__setstate__(self, attrs)

    def accueil(self):
        """Retourne l'aide courte"""
        valeur = "inconnue"
        if isinstance(self.attribut, str):
            valeur = getattr(self.objet, self.attribut, "inconnue")
            if valeur is None:
                valeur = "non précisé"

        return self.aide_courte.format(objet = self.objet, valeur=valeur)

    def interpreter(self, msg):
        """Interprétation du contexte"""
        msg = msg.strip()
        try:
            msg = self.type(msg)
        except ValueError:
            self.pere << "|err|Cette valeur est invalide.|ff|"
        else:
            # Vérification
            verification = self.verification
            if verification & CLE:
                try:
                    valider_cle(msg)
                except ValueError as err:
                    self.pere << "|err|" + str(err) + ".|ff|"
                    return

            # Modification
            modification = self.modification
            if modification & CAPITALIZE:
                msg = msg[0].upper() + msg[1:]
            elif modification & LOWER:
                msg = msg.lower()

            setattr(self.objet, self.attribut, msg)
            self.actualiser()
