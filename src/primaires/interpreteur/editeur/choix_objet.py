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


"""Ce fichier définit le contexte-éditeur 'ChoixObjet'."""

from . import Editeur
from primaires.format.fonctions import *

class ChoixObjet(Editeur):

    """Contexte-éditeur choix.

    Ce contexte permet de faire choisir l'utilisateur une option
    parmi un dictionnaire : les clés doivent être les chaînes de
    choix et les valeurs sont les objets correspondants. Cet éditeur
    peut être utilisé pour choisir un joueur, une étendue d'eau, un
    prototype d'objet ou bien d'autres choses.

    """

    nom = "editeur:base:choix_objet"

    def __init__(self, pere, objet=None, attribut=None, dictionnaire=None,
            autoriser_none=True, feminin=False):
        """Constructeur de l'éditeur."""
        Editeur.__init__(self, pere, objet, attribut)
        self.dictionnaire = dictionnaire or {}
        self.autoriser_none = autoriser_none
        self.feminin = feminin
        self.ajouter_option("s", self.opt_supprimer)

    def accueil(self):
        """Retourne l'aide courte"""
        objet = getattr(self.objet, self.attribut)
        if objet is None:
            objet = "|att|aucun|ff|"
            if self.feminin:
                objet = "|att|aucune|ff|"

        return self.aide_courte.format(objet=objet, valeur=objet)

    @staticmethod
    def afficher_apercu(apercu, objet, valeur, dictionnaire=None,
            none=False, feminin=False):
        """Affichage de l'aperçu."""
        if valeur is None:
            if feminin:
                valeur = "|att|aucune|ff|"
                Valeur = "|att|Aucune|ff|"
            else:
                valeur = "|att|aucun|ff|"
                Valeur = "|att|Aucun|ff|"

        Valeur = valeur
        return apercu.format(objet=objet, valeur=valeur, Valeur=Valeur)

    def opt_supprimer(self, arguments):
        """Supprime l'objet si autorisé."""
        if self.autoriser_none:
            setattr(self.objet, self.attribut, None)
            self.actualiser()
        else:
            self.pere.envoyer("|err|Impossible de réinitialiser cette " \
                    "valeur.|ff|")

    def interpreter(self, msg):
        """Interprétation du contexte"""
        liste = list(self.dictionnaire.keys())
        sa_liste = [supprimer_accents(e).lower() for e in liste]
        msg = supprimer_accents(msg).lower()
        if msg in sa_liste:
            indice = sa_liste.index(msg)
            cle = liste[indice]
            objet = self.dictionnaire[cle]
            setattr(self.objet, self.attribut, objet)
            self.actualiser()
        else:
            self.pere << "|err|Ce choix n'est pas valide.|ff|"
