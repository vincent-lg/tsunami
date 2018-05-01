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
# pereIBILITY OF SUCH DAMAGE.


"""Ce fichier contient l'éditeur EdtInstructions, détaillé plus bas."""

import inspect
import traceback
from textwrap import wrap

from primaires.interpreteur.editeur import Editeur
from primaires.interpreteur.editeur.env_objet import EnveloppeObjet
from primaires.format.fonctions import *

class EdtInstructions(Editeur):

    """Contexte-éditeur d'une suite d'instructions.

    L'objet appelant est la suite de tests contenant le code.
    Par code, il faut entendre ici la liste des instructions constituant
    un script.

    """

    def __init__(self, pere, objet=None, attribut=None):
        """Constructeur de l'éditeur"""
        Editeur.__init__(self, pere, objet, attribut)
        self.ajouter_option("?", self.opt_aide_generale)
        self.ajouter_option("?s", self.opt_aide_syntaxe)
        self.ajouter_option("?o", self.opt_aide_options)
        self.ajouter_option("?f", self.opt_aide_fonctions)
        self.ajouter_option("?a", self.opt_aide_actions)
        self.ajouter_option("c", self.opt_corriger_instruction)
        self.ajouter_option("d", self.opt_supprimer_instructions)
        self.ajouter_option("h", self.opt_afficher_cache)
        self.ajouter_option("i", self.opt_inserer_instruction)
        self.ajouter_option("o", self.opt_copier)
        self.ajouter_option("q", self.opt_relier_quete)
        self.ajouter_option("r", self.opt_remplacer_instruction)
        self.ajouter_option("v", self.opt_coller)
        self.ajouter_option("x", self.opt_couper)

    def opt_afficher_cache(self, arguments):
        """Affiche ou réactualiser le cache.

        Syntaxe :
            /h
            /h reset
            /h -<variable>

        """
        test = self.objet
        if arguments.startswith("-"):
            variable = arguments[1:]
            test.evenement.supprimer_variable(variable)
            self.pere << "La variable '{}' a bien été supprimée.".format(
                    variable)
        elif arguments.lower() == "reset":
            self.pere << "|att|Le cache a été réinitialisé.|ff|"
            test.calculer_cache()

        cache = test.get_cache()
        self.pere << "Cache actuel :\n" + cache

    def opt_remplacer_instruction(self, arguments):
        """Remplace une ligne par une nouvelle instruction."""
        test = self.objet
        instructions = test.instructions
        if not arguments.strip():
            self.pere << "|err|Entrez un numéro de ligne.|ff|"
            return

        arguments = arguments.split(" ")
        no = arguments[0]
        ligne = " ".join(arguments[1:])

        try:
            no = int(no) - 1
            assert no >= 0
            assert no < len(instructions)
        except (ValueError, AssertionError):
            self.pere << "|err|Entrez un numéro de ligne valide.|ff|"
            return

        if not ligne.strip():
            self.pere << "|err|Entrez une nouvelle instruction " \
                    "pour remplacer celle de la ligne {}.|ff|".format(no + 1)
            return

        try:
            test.remplacer_instruction(no, ligne)
        except ValueError as err:
            self.pere << "|err|" + str(err).capitalize() + "|ff|"
        else:
            self.actualiser()

    def opt_corriger_instruction(self, arguments):
        """Corrige une ligne d'instruction."""
        test = self.objet
        instructions = test.instructions
        if not arguments.strip():
            self.pere << "|err|Entrez un numéro de ligne.|ff|"
            return

        arguments = arguments.split(" ")
        no = arguments[0]
        reste = " ".join(arguments[1:])

        try:
            no = int(no) - 1
            assert no >= 0
            assert no < len(instructions)
        except (ValueError, AssertionError):
            self.pere << "|err|Entrez un numéro de ligne valide.|ff|"
            return

        try:
            texte, remplacement = reste.split(" / ")
        except ValueError:
            self.pere << "|err|Entrez le texte à remplacer suivi d'un " \
                    "espace, d'un slash et du texte\nde remplacement. " \
                    "Exemple : |ent|/c 5 chemise / cravate|ff|"
            return

        try:
            test.corriger_instruction(no, texte, remplacement)
        except ValueError as err:
            self.pere << "|err|" + str(err).capitalize() + "|ff|"
        else:
            self.actualiser()

    def opt_reordonner(self, arguments):
        """Obsolète. Ne plus utiliser."""
        self.actualiser()

    def opt_inserer_instruction(self, arguments):
        """Insère une instruction avant la ligne précisée.

        Syntaxe : /i no

        """
        test = self.objet
        instructions = test.instructions
        if not arguments.strip():
            self.pere << "|err|Entrez un numéro de ligne.|ff|"
            return

        arguments = arguments.split(" ")
        no = arguments[0]
        ligne = " ".join(arguments[1:])

        try:
            no = int(no) - 1
            assert no >= 0
            assert no < len(instructions)
        except (ValueError, AssertionError):
            self.pere << "|err|Entrez un numéro de ligne valide.|ff|"
            return

        if not ligne.strip():
            self.pere << "|err|Entrez une nouvelle instruction " \
                    "à insérer avant celle de la ligne {}.|ff|".format(no + 1)
            return

        try:
            test.inserer_instruction(no, ligne)
        except ValueError as err:
            self.pere << "|err|" + str(err).capitalize() + "|ff|"
        else:
            self.actualiser()

    def opt_supprimer_instructions(self, arguments):
        """Supprime des instructions du test.

        Syntaxe : /d x-y ou /d x, y, z... ou /d *

        """
        if arguments == "*":
            longueur = len(self.objet.instructions)
            for n in range(longueur):
                self.objet.supprimer_instruction(longueur - (n + 1))
            self.actualiser()
            return

        try:
            min, max = arguments.split("-")
            min = int(min)
            max = int(max)
            lignes = [n for n in range(min, max + 1)]
            assert min < max
            assert min > 0
            assert max <= len(self.objet.instructions)
        except AssertionError:
            self.pere << "|err|Précisez un intervalle correct " \
                    "(|ent|min-max|ff||err|).|ff|"
            return
        except ValueError:
            try:
                lignes = [int(n) for n in arguments.split(",")]
                assert len(lignes) > 0
                assert all([0 < n <= len(self.objet.instructions) \
                        for n in lignes])
            except (ValueError, AssertionError):
                self.pere << "|err|Précisez la (les) ligne(s) à supprimer " \
                        "dans un format correct.|ff|"
                return
        lignes = sorted(lignes, reverse=True)
        for n in lignes:
            self.objet.supprimer_instruction(n - 1)
        self.actualiser()

    def copier_instructions(self, arguments, supprimer=False):
        """Copie (ou coupe) les instructions précisées."""
        if arguments.isdigit():
            # C'est de toute évidence un nombre
            nb = int(arguments)
            if nb <= 0 or nb > len(self.objet.instructions):
                self.pere << "|err|Ce nu;éro de ligne est invalide.|ff|"
                return

            indices = [nb - 1]
        elif arguments == "*":
            indices = range(0, len(self.objet.instructions))
        else:
            try:
                min, max = arguments.split("-")
                min = int(min)
                max = int(max)
                lignes = [n for n in range(min, max + 1)]
                assert min < max
                assert min > 0
                assert max <= len(self.objet.instructions)
            except (ValueError, AssertionError):
                self.pere << "|err|Précisez un intervalle correct " \
                        "(|ent|min-max|err|).|ff|"
                return

            indices = [l - 1 for l in lignes]

        indices = sorted(indices, reverse=True)
        lignes = []
        for n in indices:
            instruction = self.objet.instructions[n]
            ligne = instruction.sans_couleurs
            lignes.insert(0, ligne)
            if supprimer:
                self.objet.supprimer_instruction(n)

        lignes.insert(0, "instructions")
        importeur.scripting.presse_papier[self.pere.joueur] = lignes
        self.actualiser()
        return

    def opt_couper(self, arguments):
        """Coupe une ou plusieurs lignes.

        Syntaxe : /x * ou /x X ou /x X-Y

        """
        self.copier_instructions(arguments, supprimer=True)

    def opt_copier(self, arguments):
        """Copie une ou plusieurs lignes.

        Syntaxe : /o * ou /o X ou /o X-Y

        """
        self.copier_instructions(arguments)

    def opt_coller(self, arguments):
        """Colle le texte contenu dans le presse-papier.

        Syntaxe :
            /v
            /v 0
            /v <indice de la ligne ou insérer le code>

        """
        presse_papier = importeur.scripting.presse_papier.get(
                self.pere.joueur)

        if presse_papier is None or len(presse_papier) == 0:
            self.pere << "Vous n'avez aucun texte dans le presse-papier."
            return

        p_type = presse_papier[0]
        if p_type != "instructions":
            self.pere << "Ce presse-papier ne contient pas d'instructions " \
                    " : type {}.".format(p_type)
            return

        if not arguments.strip():
            msg = "Presse-papier actuel :\n"
            i = 1
            for ligne in presse_papier[1:]:
                msg += "\n{:>3} {}".format(i, ligne)
                i += 1

            self.pere << msg
            return

        test = self.objet
        if arguments.strip() == "0":
            # On insert le presse-papier à la fin
            for ligne in presse_papier[1:]:
                try:
                    test.ajouter_instruction(ligne)
                except ValueError as err:
                    self.pere << "|err|" + str(err).capitalize() + "|ff|"
                    return

            self.actualiser()
            return

        instructions = test.instructions
        no = arguments
        try:
            no = int(no) - 1
            assert no >= 0
            assert no < len(instructions)
        except (ValueError, AssertionError):
            self.pere << "|err|Entrez un numéro de ligne valide.|ff|"
            return

        for ligne in reversed(presse_papier[1:]):
            try:
                test.inserer_instruction(no, ligne)
            except ValueError as err:
                self.pere << "|err|" + str(err).capitalize() + "|ff|"
                return

        self.actualiser()

    def opt_relier_quete(self, argument):
        """Relie à une quête.

        Syntaxe :
            /q 0
            /q <quête>

        La quête doit être au format :
            nom_quete:niveau

        """
        test = self.objet
        if not argument.strip():
            self.pere << "|err|Précisez |cmd|0|err| ou <quete:niveau>.|ff|"
            return

        if argument.strip() == "0":
            if test.etape:
                if test.etape is test:
                    test.etape.test = None
                test.etape = None
            self.actualiser()
            return

        try:
            quete, niveau = argument.split(":")
        except ValueError:
            self.pere << "|err|Formatage de quête invalide.|ff|"
        else:
            # On cherche la quête
            if not quete in type(self).importeur.scripting.quetes:
                self.pere << "|err|Quête {} inconnue.|ff|".format(quete)
                return

            quete = type(self).importeur.scripting.quetes[quete]
            try:
                etape = quete.etapes[niveau]
            except KeyError:
                self.pere << "|err|Le niveau {} est inconnue pour la " \
                        "quête {}.|ff|".format(niveau, quete)
                return

            etape.test = test
            test.etape = etape
            self.actualiser()

    def opt_aide_generale(self, argument):
        """Option aide générale.

        Aucun argument n'est attendu.

        """
        self.pere << \
            "Bienvenue dans l'éditeur d'instructions.\n\n" \
            "Vous pouvez ici entrer des instructions en respectant " \
            "une certaine syntaxe\net modifier les instructions déjà " \
            "existantes. Vous pouvez obtenir plus d'aide\ngrâce " \
            "aux sujets suivants :\n" \
            "  |cmd|/?s|ff| : aide sur la |ent|syntaxe|ff| du " \
            "scripting\n" \
            "  |cmd|/?o|ff| : liste des |ent|options|ff| de " \
            "l'éditeur\n" \
            "  |cmd|/?a|ff| : liste des |ent|actions|ff| " \
            "disponibles\n" \
            "  |cmd|/?f|ff| : liste des |ent|fonctions|ff| " \
            "disponibles\n\n" \
            "Si donc la syntaxe du scripting ne vous est pas familière, " \
            "il vous est\nconseillé de lire l'aide consacrée en tapant " \
            "|cmd|/?s|ff|.\nSi vous connaissez la syntaxe mais " \
            "que vous voulez connaître les\npossibilités actuelles " \
            "du scripting, tapez |cmd|/?a|ff| pour connaître " \
            "la liste des\nactions et |cmd|/?f|ff| pour connaître " \
            "la liste des fonctions."

    def opt_aide_options(self, argument):
        """Option d'aide sur les options.

        Aucun argument attendu.

        """
        self.pere << \
            "Options disponibles :\n" \
            " - |cmd|/r <no> <instruction>|ff| : remplace l'instruction en " \
            "ligne |ent|no|ff| par celle précisée\n" \
            " - |cmd|/c <no> <recherche> / <remplacement>|ff| : corrige " \
            "l'instruction en ligne |ent|no|ff|\n" \
            " - |cmd|/i <no> <instruction>|ff| : insère " \
            "l'|ent|instruction|ff| " \
            "avant la ligne |ent|no|ff|\n" \
            " - |cmd|/d <no1>(, <no2>, <no3>...)|ff| / " \
            "|cmd|<no1>-<no2>|ff| / " \
            "|cmd|*|ff| : supprime des instructions.\n   Si vous précisez " \
            "une plage à l'aide du tiret |cmd|-|ff|, en supprime " \
            "l'intégralité.\n   Si vous entrez l'étoile |cmd|*|ff|, " \
            "supprime tout.\n" \
            " - |cmd|/o|ff| : réordonne les instructions. Cette option est " \
            "à utiliser si vous\n   constatez une incohérence dans " \
            "l'indentation de votre script (voir |cmd|/?s|ff|).\n" \
            " - |cmd|/q <quete>:<niveau>|ff| : relie le script à une quête"

    def opt_aide_syntaxe(self, argument):
        """Option aide syntaxe.

        L'argument peut préciser l'aide spécifique.
        -   action      Syntaxe d'une action
        -   condition   Syntaxe d'une condition
        -   affectation Syntaxe d'une affectation

        """
        sujets = type(self).importeur.scripting.sujets_aides
        if not argument:
            self.pere << sujets["syntaxe"]
        else:
            self.pere << "A faire..."

    def opt_aide_fonctions(self, arguments):
        """Donne de l'aide sur les fonctions existantes.

        Syntaxes :
            /?f -- liste les fonctions
            /?f fonction -- affiche l'aide d'une fonction
            /?f fonction no -- affiche l'aide d'une méthode de la fonction

        """
        self.pere << importeur.scripting.aide_fonction(arguments)

    def opt_aide_actions(self, arguments):
        """Donne de l'aide sur les actions existantes.

        Syntaxes :
            /?a -- liste les actions
            /?a action -- affiche l'aide d'une action
            /?a action no -- affiche l'aide d'une méthode de l'action

        """
        self.pere << importeur.scripting.aide_action(arguments)

    def accueil(self):
        """Message d'accueil du contexte"""
        tests = self.objet
        instructions = tests.instructions
        evenement = tests.evenement
        appelant = evenement.script.parent
        msg = "| |tit|"
        msg += "Edition d'un test de {}[{}]".format(appelant,
                evenement.nom).ljust(76)
        msg += "|ff||\n" + self.opts.separateur + "\n"
        msg += "Entrez directement une |ent|instruction|ff| pour l'ajouter, "
        msg += "ou |cmd|/|ff| pour revenir à la\nfenêtre précédente. L'option "
        msg += "|cmd|/?|ff| vous fournira toute l'aide nécessaire si\n"
        msg += "vous n'êtes pas à l'aise avec cet éditeur.\n\n"
        if isinstance(evenement.variables, dict):
            variables = evenement.variables.values()
        else:
            variables = evenement.variables

        if tests.etape:
            msg += "|att|ATTENTION : ce script est relié à la quête " \
                    "{} (étape {}).\n\n|ff|".format(tests.etape.quete.cle,
                    tests.etape.str_niveau)
        if variables:
            msg += "Variables definies dans ce script :\n"
            t_max = 0
            for v in variables:
                if len(v.nom) > t_max:
                    t_max = len(v.nom)
            lignes = ["|grf|" + var.nom.ljust(t_max) + "|ff| : " + var.aide \
                    for var in variables]
            msg += "\n".join(lignes)
            msg += "\n\n"

        msg += "|cy|Instructions :|ff|\n\n "
        if instructions:
            msg += "\n ".join(["|grf|{:>3}|ff| {}{}".format(i + 1,
                    "  " * instruction.niveau, str(instruction)) \
                    for i, instruction in enumerate(instructions)])
        else:
            msg += " Aucune instruction n'est définie dans ce script."

        return msg

    def interpreter(self, msg):
        """Interprétation de l'éditeur"""
        tests = self.objet

        if not msg:
            self.actualiser()
        else:
            try:
                tests.ajouter_instruction(msg)
            except ValueError as err:
                print(traceback.format_exc())
                self.pere << "|err|" + str(err).capitalize() + "|ff|"
            else:
                self.actualiser()
