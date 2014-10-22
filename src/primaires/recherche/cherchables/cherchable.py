# -*-coding:Utf-8 -*

# Copyright (c) 2012 NOEL-BARON Léo
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


"""Ce fichier définit la classe Cherchable, classe abstraite de base
pour les objets de recherche (voir plus bas).

"""

import argparse
import inspect
import re
import shlex
import textwrap

from abstraits.obase import BaseObj
from primaires.format.tableau import Tableau
from primaires.recherche.filtre import Filtre
from primaires.recherche.cherchables import MetaCherchable

INTERDITS = ["a", "aide", "o", "org", "c", "colonnes"]
PARAMS = {"str":"une chaîne",
    "str!":"une chaîne (n'accepte pas les regex)",
    "int":"un nombre entier",
    "bool":"un booléen",
}

class Cherchable(BaseObj, metaclass=MetaCherchable):

    """Classe de base des objets de recherche.

    Cette classe modélise les items que l'on est susceptible de rechercher
    dans l'univers : objets, salles, personnages... Elle associe à chacun une
    liste de filtres de recherche correspondant à des options (syntaxe Unix).

    De fait, c'est plutôt une enveloppe de filtres et d'objets à traiter.
    Pour un exemple d'utilisation, voir primaires/objet/cherchables/objet.py.

    """

    nom_cherchable = ""
    recherche_par_defaut = ""
    noms_colonnes = {}

    def __init__(self):
        """Constructeur de la classe"""
        self.filtres = []

        # Initialisation du cherchable
        self.init()

    def __getnewargs__(self):
        return ()

    def init(self):
        """Méthode d'initialisation.

        C'est ici que l'on ajoute réellement les filtres, avec la méthode
        dédiée.

        """
        raise NotImplementedError

    @property
    def courtes(self):
        """Renvoie une chaîne des options courtes au bon format"""
        avec = []
        sans = ""
        for filtre in self.filtres:
            courte = filtre.opt_courte
            courte += ":" if filtre.type else ""
            if filtre.opt_longue:
                avec.append(courte)
            else:
                sans += courte
        avec = "".join(sorted(avec))
        return avec + sans

    @property
    def longues(self):
        """Renvoie une liste des options longues au bon format"""
        ret = []
        for filtre in self.filtres:
            if filtre.opt_longue:
                egal = "=" if filtre.type else ""
                ret.append(filtre.opt_longue + egal)
        return sorted(ret)

    @property
    def items(self):
        """Renvoie la liste des objets traités"""
        raise NotImplementedError

    @property
    def attributs_tri(self):
        """Renvoie la liste des attributs par lesquels on peut trier"""
        return []

    @property
    def colonnes(self):
        """Retourne un dictionnaire des valeurs que l'on peut disposer en
        colonne à l'affichage final, de la forme :
        >>> {nom: attribut/méthode}
        (une colonne peut être remplie par une méthode du cherchable).

        """
        return {}

    @property
    def aide(self):
        """Retourne l'aide du cherchable"""
        aide = "Catégorie de recherche |cmd|" + self.nom_cherchable + "|ff|\n"
        aide += inspect.getdoc(self).rstrip() + "\n\n"
        aide += "Filtres disponibles :\n"
        noms_filtres = [str(f) for f in self.filtres]
        l_max = 0
        for f in noms_filtres:
            if len(f) > l_max:
                l_max = len(f)
        for i, filtre in enumerate(self.filtres):
            aide += "   " + noms_filtres[i].ljust(l_max) + " "
            if callable(filtre.test):
                aide_filtre = inspect.getdoc(filtre.test)
            else:
                param = textwrap.dedent(filtre.type.aide).strip()
                aide_filtre = "Recherche à partir de l'attribut |cmd|"
                aide_filtre += filtre.test + "|ff|. Cette option prend en "
                aide_filtre += "paramètre " + param + "."
            lignes = textwrap.wrap(aide_filtre, width=75 - l_max)
            aide += ("\n" + " " * (l_max + 4)).join(lignes).strip() + "\n"
        if self.attributs_tri:
            attr_tri = "|ent|" + "|ff|, |ent|".join(self.attributs_tri)
            attr_tri += "|ff|"
            aide += "\nPossibilités de tri : " + attr_tri + ".\n"
            aide += "L'option de tri (-o ARG, --org=ARG) permet, en précisant "
            aide += "une des possibilités\nqui précèdent, de trier le retour "
            aide += "de la recherche en fonction de cet argument.\n"
        if self.colonnes:
            colonnes = list(self.colonnes.keys())
            colonnes = "|ent|" + "|ff|, |ent|".join(colonnes) + "|ff|"
            aide += "\nColonnes possibles : " + colonnes + ".\n"
            aide += "L'option colonnes (-c ARG, --colonnes=ARG) permet "
            aide += "d'organiser le retour en un\ntableau ; précisez pour "
            aide += "cela une ou plusieurs des colonnes ci-dessus, séparées\n"
            aide += "par des virgules (par exemple |ent|nom, identifiant, "
            aide += "autre|ff|)."
        return aide.strip()

    def ajouter_filtre(self, opt_courte, opt_longue, test, type=""):
        """Ajoute le filtre spécifié"""
        longues = [f.opt_longue for f in self.filtres]
        if opt_courte in self.courtes or opt_courte in INTERDITS:
            raise ValueError("l'option courte '{}' est indisponible".format(
                    opt_courte))
        if opt_longue in longues or opt_longue in INTERDITS:
            raise ValueError("l'option longue '{}' est indisponible".format(
                    opt_longue))
        self.filtres.append(Filtre(opt_courte, opt_longue, test, type))

    def tester(self, args, liste):
        """Teste une liste de couples (option, argument)"""
        if not args:
            return liste

        if args.defaut and self.recherche_par_defaut:
            valeur = args.defaut
            setattr(args, self.recherche_par_defaut, valeur)

        for filtre in self.filtres:
            option = filtre.opt_courte
            if filtre.opt_longue:
                option = filtre.opt_longue

            if getattr(args, option) is not None:
                valeur = " ".join(getattr(args, option))
                liste = [item for item in liste if filtre.tester(
                        item, valeur)]

        return liste

    def afficher(self, objet):
        """Méthode d'affichage standard des objets traités"""
        raise NotImplementedError

    def colonnes_par_defaut(self):
        """Retourne les colonnes d'affichage par défaut.

        Si une ou plusieurs colonnes sont spécifiés lors de la recherche,
        les colonnes par défaut ne sont pas utilisées.

        Cette méthode doit retourner une liste de nom de colonnes.

        """
        raise NotImplementedError

    def tri_par_defaut(self):
        """Sur quelle colonne se base-t-on pour trier par défaut ?"""
        raise NotImplementedError

    @classmethod
    def trouver_depuis_chaine(cls, chaine):
        """Retourne un message en fonction de la chaîne passée en paramètre."""
        def n_exit(code, msg):
            """Ne quitte pas Python."""
            raise ValueError(msg)

        cherchable = cls()

        # On crée les listes d'options
        parser = argparse.ArgumentParser()
        parser.exit = n_exit

        # Ajout des options par défaut
        parser.add_argument("defaut", nargs='*')
        parser.add_argument("-a", "--aide", action="store_true")
        parser.add_argument("-o", "--ordre")
        parser.add_argument("-c", "--colonnes", nargs='+')

        # Ajout des options du cherchable
        for filtre in cherchable.filtres:
            options = ["-" + filtre.opt_courte]
            if filtre.opt_longue:
                options.append("--" + filtre.opt_longue)

            parser.add_argument(*options, nargs='*')

        retour = []
        tri = ""
        colonnes = []
        if not chaine.strip():
            retour = cherchable.items
        else:
            try:
                args = parser.parse_args(shlex.split(chaine))
            except ValueError as err:
                return "|err|Une option n'a pas été reconnue ou bien " \
                        "interprétée.|ff|\n" + str(err)

            # On récupère les options génériques
            if args.aide:
                return cherchable.aide
            if args.ordre:
                arg = args.ordre
                if arg in cherchable.attributs_tri:
                    tri = arg
                else:
                    return "|err|Vous ne pouvez trier ainsi.|ff|"
            if args.colonnes:
                arg = " ".join(args.colonnes)
                try:
                    colonnes = arg.split(",")
                    colonnes = [c.strip() for c in colonnes]
                    for c in colonnes:
                        assert c in cherchable.colonnes
                except AssertionError:
                    return "|err|Les colonnes spécifiées sont " \
                            "invalides.|ff|"

            # Interprétation des autres options
            try:
                retour = cherchable.tester(args, cherchable.items)
            except TypeError as err:
                return "|err|Les options n'ont pas été bien " \
                        "interprétées : " + str(err) + "|ff|"

        # Post-traitement et affichage
        if not retour:
            return "|att|Aucun retour pour ces paramètres de " \
                    "recherche.|ff|"
        else:
            # On trie la liste de retour
            if not tri:
                tri = cherchable.tri_par_defaut()

            retour = sorted(retour, key=lambda obj: getattr(obj, tri))

            retour_aff = Tableau()
            if not colonnes:
                colonnes = cherchable.colonnes_par_defaut()

            for colonne in colonnes:
                if colonne in cherchable.noms_colonnes:
                    colonne = cherchable.noms_colonnes[colonne]

                retour_aff.ajouter_colonne(colonne.capitalize())

            for i, o in enumerate(retour):
                ligne = []
                for l, c in enumerate(colonnes):
                    c = c.strip()
                    if callable(cherchable.colonnes[c]):
                        aff = cherchable.colonnes[c](o)
                    else:
                        aff = getattr(o, cherchable.colonnes[c])
                    ligne.append(aff)
                retour_aff.ajouter_ligne(*ligne)

            return retour_aff.afficher()
