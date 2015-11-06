# -*-coding:Utf-8 -*

# Copyright (c) 2015 LE GOFF Vincent
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


"""Ce fichier définit le contexte-éditeur 'AES'."""

import traceback

from corps.fonctions import valider_cle
from primaires.format.fonctions import supprimer_accents
from primaires.interpreteur.editeur.env_objet import EnveloppeObjet
from . import Editeur

class AES(Editeur):

    """Contexte-éditeur AES.

    L'éditeur AES (Ajout / Édition / Suppression) est un
    éditeur conçu pour ajouter, retirer ou éditer des éléments
    particuliers. Cet éditeur, conçu pour être extensible au
    maximum, permet d'éditer des listes d'informations, ajouter
    ou retirer des éléments et éditer un élément précis (ce qui
    crée un nouvel éditeur).

    Le constructeur attend un paramètre supplémentaire, la liste des
    informations et de leur type, sous la forme d'un tuple de tuples
    comme par exemple (("nom", "chaîne), ("age", "entier")). Ces
    informations sont utilisées comme les colonnes d'un tableau à
    la création. La première colonne est une colonne unique
    (dans ce contexte, on ne peut avoir deux objets du même nom
    dans la liste). L'information de la première colonne est utilisée
    pour l'édition ou la suppression.

    Le constructeur possède également deux autres paramètres, le
    nom de la méthode d'ajout et le nom de la méthode de suppression.
    On peut préciser après un point (.) le type d'objet à renseigner.
    Ce peut être "indice" (pour spécifier l'indice de la liste),
    "clé" pour spécifier la première colonne ou "objet" pour
    préciser l'objet à supprimer. Par exemple,
    "supprimer_element.objet" enverra à la méthode 'supprimer_element'
    de self.objet l'élément-même à supprimer.

    """

    nom = "editeur:base:aes"

    def __init__(self, pere, objet=None, attribut=None,
            editeur_suivant=None, colonnes=None, recuperation=None,
            ajout=None, suppression=None, affichage=None):
        """Constructeur de l'éditeur"""
        Editeur.__init__(self, pere, objet, attribut)
        self.editeur_suivant = editeur_suivant or ""
        self.colonnes = colonnes or []
        self.recuperation = recuperation or ""
        self.ajout = ajout or ""
        self.suppression = suppression or ""
        self.affichage = affichage or ""

        self.ajouter_option("a", self.opt_ajouter)
        self.ajouter_option("s", self.opt_supprimer)

    @staticmethod
    def get_valeur(valeur, affichage):
        """Retourne la valeur à afficher."""
        if valeur is None:
            valeur = []

        if isinstance(valeur, dict):
            valeur = list(valeur.values())

        if len(valeur) == 0:
            valeur = "\n  |att|Aucun élément à afficher|ff|"
        else:
            if affichage:
                valeur = "\n  " + "\n  ".join([getattr(v, affichage) for \
                        v in valeur])
            else:
                valeur = "\n  " + "\n  ".join([str(v) for v in valeur])

        return valeur

    @staticmethod
    def afficher_apercu(apercu, objet, valeur, suivant=None, colonnes=None,
            recuperation=None, ajout=None, suppression=None, affichage=None):
        """Affichage de l'aperçu."""
        valeur = AES.get_valeur(valeur, affichage)
        return apercu.format(objet=objet, valeur=valeur)

    def accueil(self):
        """Retourne l'aide"""
        valeur = getattr(self.objet, self.attribut)
        valeur = AES.get_valeur(valeur, self.affichage)
        return self.aide_courte.format(objet=self.objet, valeur=valeur)

    def opt_ajouter(self, arguments):
        """Ajout d'un élément.

        Syntaxe :
          /a <paramètres>

        """
        colonnes = self.colonnes
        ajout = self.ajout
        arguments = arguments.strip().split(" / ")
        if len(arguments) != len(colonnes):
            self.pere << "|err|Nombre invalide d'arguments : {} " \
                    "attendus contre {} reçus.\nSyntaxe : |ent|".format(
                    len(colonnes), len(arguments)) + " / ".join(
                    [c[0] for c in colonnes]) + "|ff|"
            return

        for i, arg in enumerate(list(arguments)):
            colonne = colonnes[i]
            n_type = colonne[1]
            if n_type == "chaîne":
                pass
            elif n_type == "entier":
                try:
                    arg = int(arg)
                except ValueError:
                    self.pere << "|err|Colonne {} ({}) : nombre entier {} " \
                            "invalide.|ff|".format(i + 1, colonne[0], arg)
                    return
                else:
                    arguments[i] = arg
            elif n_type == "flottant":
                try:
                    arg = float(arg.replace(",", "."))
                except ValueError:
                    self.pere << "|err|Colonne {} ({}) : nombre flottant {} " \
                            "invalide.|ff|".format(i + 1, colonne[0], arg)
                    return
                else:
                    arguments[i] = arg
            elif n_type == "clé":
                try:
                    valider_cle(arg)
                except ValueError:
                    self.pere << "|err|Colonne {} ({}) : clé invalide " \
                            "{}|ff|".format(i + 1, colonne[0], repr(arg))
                    return
                else:
                    arguments[i] = arg
            else:
                raise ValueError("colonne {} : type inconnu ({})".format(
                        i + 1, repr(n_type)))

        # On essaye d'ajouter l'élément
        methode = getattr(self.objet, ajout)
        try:
            methode(*arguments)
        except Exception as err:
            self.pere << "|err|" + str(err) + ".|ff|"
            return

        self.actualiser()

    def opt_supprimer(self, arguments):
        """Suppression d'un élément.

        Syntaxe :
            /s <clé>

        """
        if self.suppression is None:
            self.pere << "|err|Vous ne pouvez faire cela.|ff|"
            return

        arg = arguments.strip()
        methode = getattr(self.objet, self.suppression)

        try:
            methode(arg)
        except Exception as err:
            self.pere << "|err|" + str(err) + ".|ff|"
            return

        self.actualiser()

    def interpreter(self, msg):
        """Interprétation de l'éditeur."""
        liste = getattr(self.objet, self.attribut)
        methode = getattr(self.objet, self.recuperation)

        try:
            element = methode(msg)
        except Exception as err:
            print(traceback.format_exc())
            self.pere << "|err|" + str(err) + ".|ff|"
            return

        TypeEditeur = importeur.interpreteur.contextes[self.editeur_suivant]
        enveloppe = EnveloppeObjet(TypeEditeur, element, None)
        enveloppe.parent = self
        contexte = enveloppe.construire(self.pere.joueur)
        self.migrer_contexte(contexte)
