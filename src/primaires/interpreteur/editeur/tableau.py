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


"""Ce fichier définit le contexte-éditeur 'Tableau'."""

from corps.fonctions import valider_cle
from primaires.format.fonctions import *
from primaires.format.tableau import Tableau as AffTableau, DROITE, GAUCHE
from . import Editeur

class Tableau(Editeur):

    """Contexte-éditeur tableau.

    Cet éditeur est puissant : il permet de renseigner une liste
    de listes (ou une liste dans un dictionnaire). L'attribut à
    modifier est un tableau pour le joueur, comportant plusieurs
    informations organisées en colonnes. Par exemple, on pourrait
    configurer un éditeur tableau pour éditer un attribut faisant
    correspondre un membre à une clé de prototype d'objet (ce
    pourrait être le cas pour éditer l'équipement d'un PNJ,
    par exemple).

    À la création de l'éditeur, il faut préciser le nom et
    type de chaque colonne. L'argument doit être une liste de
    tuples : le premier élément du tuple doit être le nom de la
    colonne (tel qu'il sera affiché), le second peut être soit :
        *   Une chaîne contenant le nom du type
        *   Une liste de chaînes quand il s'agit d'une sélection
        *   Un dictionnaire de chaîne->objet quand il s'agit d'une
            séleciton contrôlée

    Le constructeur prend également un autre paramètr qui
    peut être renseigné comme dictionnaire. Il permet de faire la
    correspondance entre ce qui se trouve en données enregistrées
    et ce qu'il faut afficher dans le tableau, pour le confort de
    l'utilisateur.

    """

    nom = "editeur:base:tableau"

    def __init__(self, pere, objet=None, attribut=None, colonnes=None,
            affichage=None, callback=None, nouveau="list"):
        """Constructeur de l'éditeur."""
        Editeur.__init__(self, pere, objet, attribut)
        self.colonnes = colonnes
        self.affichage = affichage or {}
        self.callback = callback
        self.nouveau = [] if nouveau == "list" else {}
        self.ajouter_option("s", self.opt_supprimer)

    def accueil(self):
        """Retourne l'aide courte"""
        objet = getattr(self.objet, self.attribut)
        objet = objet or self.nouveau
        if isinstance(objet, dict):
            lignes = []
            for cle, valeur in objet.items():
                if isinstance(valeur, (tuple, list)):
                    lignes.append([cle] + list(valeur))
                else:
                    lignes.append([cle, valeur])
        else:
            lignes = list(objet)

        if lignes:
            # Constitution du tableau
            tableau = AffTableau()
            for nom, n_type in self.colonnes:
                alignement = GAUCHE
                if n_type in ("entier", "flottant"):
                    alignement = DROITE

                tableau.ajouter_colonne(nom.capitalize(),
                        alignement=alignement)

            # Parcourt des lignes
            for ligne in lignes:
                # Transformation de l'affichage
                for indice, rempl in self.affichage.items():
                    ligne[indice] = rempl.get(ligne[indice], "")
                tableau.ajouter_ligne(*ligne)
            valeur = "\n" + tableau.afficher()
        else:
            valeur = "|att|\nAucune donnée à afficher pour l'instant|ff|"

        return self.aide_courte.format(objet=objet, valeur=valeur)

    @staticmethod
    def afficher_apercu(apercu, objet, valeur, colonnes=None,
            affichage=None, callback=None, nouveau=None):
        """Affichage de l'aperçu."""
        taille = 0
        if valeur:
            taille = len(valeur)

        return apercu.format(objet=objet, taille=taille, valeur=taille)

    def opt_supprimer(self, arguments):
        """Supprime l'objet si autorisé."""
        cle = supprimer_accents(arguments).lower()
        objet = getattr(self.objet, self.attribut)
        objet = objet or self.nouveau
        if isinstance(objet, dict):
            # cle doit être une clé dans le dictionnaire
            cles = tuple(objet.keys())
            cles_sa = [supprimer_accents(c).lower() for c in cles]
            if cle in cles_sa:
                cle = cles[cles_sa.index(cle)]
                del objet[cle]
                self.actualiser()
            else:
                self.pere << "|err|Impossible de supprimer {}.|ff|".format(
                        repr(cle))
        elif isinstance(objet, list):
            try:
                indice = int(cle)
                assert indice > 0
                assert indice <= len(objet)
            except (ValueError, AssertionError):
                self.pere << "|err|Indice de suppression invalide.|ff|"
            else:
                del objet[indice - 1]
                self.actualiser()

    def interpreter(self, msg):
        """Interprétation du contexte"""
        objet = getattr(self.objet, self.attribut)
        if objet is None:
            objet = self.nouveau
            setattr(self.objet, self.attribut, objet)

        msgs = msg.split(" / ")
        colonnes = self.colonnes
        if len(msgs) != len(colonnes):
            self.pere << "|err|Le nombre d'informations précisées " \
                    "est invalide.\n{} colonnes attendues contre " \
                    "{} renseignées.|ff|".format(len(colonnes), len(msgs))
            return

        # On transforme maintenant chaque colonnes
        i = 0
        for nom, n_type in self.colonnes:
            valeur = msgs[i]
            valeur_sa = supprimer_accents(valeur).lower()
            if isinstance(n_type, str):
                if n_type == "chaîne":
                    pass
                elif n_type == "clé":
                    try:
                        valider_cle(valeur)
                    except ValueError:
                        self.pere << "|err|Colonne {} : {} n'est " \
                                "pas ue clé valide.".format(i + 1, valeur)
                        return
                elif n_type == "entier":
                    try:
                        valeur = int(valeur)
                    except ValueError:
                        self.pere << "|err|Colonne {} : {} n'est " \
                                "pas un nombre.".format(i + 1, valeur)
                        return
                    else:
                        msgs[i] = valeur
                elif n_type == "flottant":
                    try:
                        valeur = float(valeur.replace(",", "."))
                    except ValueError:
                        self.pere << "|err|Colonne {} : {} n'est " \
                                "pas un flottant.".format(i + 1, valeur)
                        return
                    else:
                        msgs[i] = valeur
                else:
                    raise ValueError("Type inconnu {}".format(n_type))
            elif isinstance(n_type, list):
                liste = [supprimer_accents(c).lower() for c in n_type]
                if liste and valeur_sa not in liste:
                    self.pere << "|err|Colonne {} : valeur {} " \
                            "invalide.|ff|".format(i + 1, valeur)
                    return
                else:
                    msgs[i] = n_type[liste.index(valeur_sa)]
            elif isinstance(n_type, dict):
                cles = list(n_type.keys())
                liste = [supprimer_accents(c).lower() for c in cles]
                if liste and valeur_sa not in liste:
                    self.pere << "|err|Colonne {} : valeur {} " \
                            "invalide.|ff|".format(i + 1, valeur)
                    return
                else:
                    msgs[i] = n_type[cles[liste.index(valeur_sa)]]
            else:
                raise ValueError("Type inconnu : {}".format(type(n_type)))

            i += 1

        if isinstance(objet, dict):
            cle = msgs[0]
            args = msgs[1:]
            if len(args) == 1:
                args = args[0]

            objet[cle] = args
        else:
            objet.append(msgs)

        if self.callback:
            methode = getattr(self.objet, self.callback)
            methode()

        self.actualiser()
