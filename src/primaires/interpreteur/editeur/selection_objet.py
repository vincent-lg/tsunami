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


"""Ce fichier définit le contexte-éditeur 'SelectionObjet'."""

from . import Editeur
from primaires.format.fonctions import supprimer_accents

class SelectionObjet(Editeur):

    """Contexte-éditeur selection_objet.

    Ce contexte permet de créer une liste d'objets. On doit
    lui donner en paramètre un dictionnaire clé => objet.

    """

    nom = "editeur:base:selection_objet"

    def __init__(self, pere, objet=None, attribut=None, dictionnaire=None,
            feminin=False):
        """Constructeur de l'éditeur"""
        Editeur.__init__(self, pere, objet, attribut)
        self.dictionnaire = dictionnaire or {}

    def entrer(self):
        """Quand on entre dans le contexte"""
        valeur = getattr(self.objet, self.attribut, None)
        if valeur is None:
            setattr(self.objet, self.attribut, [])

    def accueil(self):
        """Retourne l'aide courte"""
        valeur = getattr(self.objet, self.attribut)
        valeur = [str(v) for v in valeur if v]
        valeur = ", ".join(valeur)
        return self.aide_courte.format(objet=self.objet, valeur=valeur)

    @staticmethod
    def afficher_apercu(apercu, objet, valeur, dictionnaire=None,
            feminin=False):
        """Affichage de l'aperçu."""
        if valeur:
            valeur = [str(v) for v in valeur if v]
            valeur = ", ".join([v for v in valeur])
            Valeur = valeur.capitalize()
        else:
            e = "e" if feminin else ""
            valeur = Valeur = "|att|Aucun{e}|ff|".format(e=e)

        return apercu.format(objet=objet, valeur=valeur, Valeur=Valeur)

    def interpreter(self, msg):
        """Interprétation du contexte"""
        liste = getattr(self.objet, self.attribut)
        msg_sa = supprimer_accents(msg).lower()
        dictionnaire = self.dictionnaire
        cles = list(dictionnaire.keys())
        cles_sa = [supprimer_accents(c).lower() for c in cles]
        if msg_sa in cles:
            objet = dictionnaire[cles[cles_sa.index(msg_sa)]]
            if objet in liste:
                while objet in liste:
                    liste.remove(objet)
            else:
                liste.append(objet)
            liste[:] = [e for e in liste if e]
            self.actualiser()
        else:
            self.pere << "|err|La clé {} est introuvable.|ff|".format(
                    repr(msg))
