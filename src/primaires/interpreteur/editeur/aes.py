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

    Le constructeur attend plusieurs paramètres, dont les deux premiers sont obligatoires :

    *   Le nom de l'éditeur suivant appelé lors de l'édition
        (peut rester à None si l'éditeur ne supporte pas l'édition
        de sous-éléments) ;
    *   La liste des informations et de leur type, sous la forme
        d'un tuple de tuples comme par exemple
        (("nom", "chaîne), ("age", "entier")). Ces informations sont
        utilisées comme les colonnes d'un tableau à la création.
        La première colonne est une colonne unique (dans ce contexte,
        on ne peut avoir deux objets du même nom dans la liste).
        L'information de la première colonne est utilisée pour l'édition
        ou la suppression ;
    *   Le nom de la méthode de récupération (le nom d'une méthode
        définie dans l'objet passé en paramètre) ;
    *   Le nom de la méthode d'ajout ;
    *   Le nom de la méthode de suppression ;
    *   Le nom de l'attribut d'affichage. Ce nom est recherché sur
        l'élément ajouté, pas l'objet. Ce peut aussi être une propriété.
    *   L'objet de callback. Si défini, au lieu d'appeler les
        méthodes sur l'objet, on l'appelle sur le callback, ce qui
        permet pas mal de personnalisation.

    Utiliser cet éditeur est un peu complexe, mais beaucoup de code
    est mis en place pour permettre une édition sur plusieurs niveaux
    de façon transparente. Consultez les exemples dans le code pour
    avoir une bonne idée de l'utilisation de cette méthode.

    """

    nom = "editeur:base:aes"

    def __init__(self, pere, objet=None, attribut=None,
            editeur_suivant=None, colonnes=None, recuperation=None,
            ajout=None, suppression=None, affichage=None, callback=None):
        """Constructeur de l'éditeur"""
        Editeur.__init__(self, pere, objet, attribut)
        self.editeur_suivant = editeur_suivant or ""
        self.colonnes = colonnes or []
        self.recuperation = recuperation or ""
        self.ajout = ajout or ""
        self.suppression = suppression or ""
        self.affichage = affichage or ""
        self.callback = callback

        self.ajouter_option("a", self.opt_ajouter)
        self.ajouter_option("s", self.opt_supprimer)

        valeur = getattr(objet, attribut)
        if isinstance(valeur, list):
            self.ajouter_option("h", self.opt_haut)
            self.ajouter_option("b", self.opt_bas)

    @staticmethod
    def get_valeur(valeur, affichage, callback=None):
        """Retourne la valeur à afficher."""
        if valeur is None:
            valeur = []

        if isinstance(valeur, dict):
            valeur = list(valeur.values())

        liste = valeur
        if len(valeur) == 0:
            valeur = "\n  |att|Aucun élément à afficher|ff|"
        else:
            if callback:
                valeur = "\n  " + "\n  ".join(
                        [getattr(callback, affichage)(liste, v) for v in \
                        valeur])
            elif affichage:
                valeur = "\n  " + "\n  ".join([getattr(v, affichage) for \
                        v in valeur])
            else:
                valeur = "\n  " + "\n  ".join([str(v) for v in valeur])

        return valeur

    @staticmethod
    def afficher_apercu(apercu, objet, valeur, suivant=None, colonnes=None,
            recuperation=None, ajout=None, suppression=None, affichage=None, callback=None):
        """Affichage de l'aperçu."""
        valeur = AES.get_valeur(valeur, affichage, callback)
        return apercu.format(objet=objet, valeur=valeur)

    def accueil(self):
        """Retourne l'aide"""
        valeur = getattr(self.objet, self.attribut)
        valeur = AES.get_valeur(valeur, self.affichage, self.callback)
        return self.aide_courte.format(objet=self.objet, valeur=valeur)

    def entrer(self):
        """Quand on entre dans le contexte"""
        valeur = getattr(self.objet, self.attribut, None)
        if valeur is None:
            setattr(self.objet, self.attribut, [])

    def opt_ajouter(self, arguments):
        """Ajout d'un élément.

        Syntaxe :
          /a <paramètres>

        """
        valeur = getattr(self.objet, self.attribut)
        objet = self.callback or self.objet
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
        methode = getattr(objet, ajout)
        try:
            if self.callback:
                methode(self.objet, valeur, *arguments)
            else:
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
        valeur = getattr(self.objet, self.attribut)
        objet = self.callback or self.objet
        if self.suppression is None:
            self.pere << "|err|Vous ne pouvez faire cela.|ff|"
            return

        arg = arguments.strip()
        methode = getattr(objet, self.suppression)

        try:
            if self.callback:
                methode(self.objet, valeur, arg)
            else:
                methode(arg)
        except Exception as err:
            self.pere << "|err|" + str(err) + ".|ff|"
            return

        self.actualiser()

    def opt_haut(self, arguments):
        """Déplace la sélection vers le haut.

        Syntaxe :
            /h <indice ou clé>

        """
        valeur = getattr(self.objet, self.attribut)
        objet = self.callback or self.objet
        liste = getattr(self.objet, self.attribut)
        methode = getattr(objet, self.recuperation)

        try:
            if self.callback:
                element = methode(valeur, arguments)
            else:
                element = methode(arguments)
        except Exception as err:
            print(traceback.format_exc())
            self.pere << "|err|" + str(err) + ".|ff|"
            return
        else:
            indice = liste.index(element)
            if indice == 0:
                self.pere << "Cet élément est déjà tout en haut."
                return

            del liste[indice]
            liste.insert(indice - 1, element)
            self.actualiser()

    def opt_bas(self, arguments):
        """Déplace la sélection vers le bas.

        Syntaxe :
            /b <indice ou clé>

        """
        valeur = getattr(self.objet, self.attribut)
        objet = self.callback or self.objet
        liste = getattr(self.objet, self.attribut)
        methode = getattr(objet, self.recuperation)

        try:
            if self.callback:
                element = methode(valeur, arguments)
            else:
                element = methode(arguments)
        except Exception as err:
            print(traceback.format_exc())
            self.pere << "|err|" + str(err) + ".|ff|"
            return
        else:
            indice = liste.index(element)
            if indice == len(liste) - 1:
                self.pere << "Cet élément est déjà tout en bas."
                return

            del liste[indice]
            liste.insert(indice + 1, element)
            self.actualiser()

    def interpreter(self, msg):
        """Interprétation de l'éditeur."""
        objet = self.callback or self.objet
        liste = getattr(self.objet, self.attribut)
        methode = getattr(objet, self.recuperation)

        try:
            if self.callback:
                element = methode(liste, msg)
            else:
                element = methode(msg)
        except Exception as err:
            print(traceback.format_exc())
            self.pere << "|err|" + str(err) + ".|ff|"
            return

        if self.callback:
            self.callback.editer_element(self, self.objet, liste, element)
        else:
            TypeEditeur = importeur.interpreteur.contextes[self.editeur_suivant]
            enveloppe = EnveloppeObjet(TypeEditeur, element, None)
            enveloppe.parent = self
            contexte = enveloppe.construire(self.pere.joueur)
            self.migrer_contexte(contexte)
