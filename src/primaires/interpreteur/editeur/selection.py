# -*-coding:Utf-8 -*

# Copyright (c) 2010 DAVY Guillaume
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


"""Ce fichier définit le contexte-éditeur 'Selection'."""

from . import Editeur
from primaires.format.dictionnaires import DictSansAccent
from primaires.format.fonctions import supprimer_accents

class Selection(Editeur):

    """Contexte-éditeur selection.

    Ce contexte permet de faire sélectionner à l'utilisateur 0, 1, N ou tous
    les éléments d'une liste. Si la liste passée en paramètre
    est une liste vide, la sélection peut porter sur n'importe quel
    choix.

    """

    nom = "editeur:base:selection"

    def __init__(self, pere, objet=None, attribut=None, liste=None):
        """Constructeur de l'éditeur"""
        Editeur.__init__(self, pere, objet, attribut)
        self.liste = liste or []

    def accueil(self):
        """Retourne l'aide courte"""
        valeur = getattr(self.objet, self.attribut)
        valeur = ", ".join(sorted([str(v) for v in valeur]))
        return self.aide_courte.format(objet=self.objet, valeur=valeur)

    @staticmethod
    def afficher_apercu(apercu, objet, valeur, liste=None):
        """Affichage de l'aperçu."""
        liste = liste or []
        if valeur == ["*"]:
            valeur = "tous"
        else:
            valeur = ", ".join([str(v) for v in valeur])
        Valeur = valeur.capitalize()
        return apercu.format(objet=objet, valeur=valeur, Valeur=Valeur)

    def interpreter(self, msg):
        """Interprétation du contexte"""
        nom = msg
        msg_sa = supprimer_accents(msg).lower()

        if self.liste and msg == "*":
            setattr(self.objet, self.attribut, ["*"])
        else:
            # Si la chaîne est déjà sélectionéne, on la supprime
            selectionnes = getattr(self.objet, self.attribut)
            selectionnes_sa = [supprimer_accents(s).lower() for s in \
                    selectionnes]
            if msg_sa in selectionnes_sa:
                selectionnes = [s for s in selectionnes if \
                        supprimer_accents(s).lower() != msg_sa]
            elif self.liste:
                liste_sa = [supprimer_accents(l) for l in self.liste]
                if msg_sa in liste_sa:
                    if "*" in selectionnes:
                        selectionnes.remove("*")
                    selectionnes.append(self.liste[liste_sa.index(msg_sa)])
                else:
                    self.pere << "Élément introuvable : {}".format(msg)
                    return
            else:
                selectionnes.append(msg)

            setattr(self.objet, self.attribut, selectionnes)

        self.actualiser()
