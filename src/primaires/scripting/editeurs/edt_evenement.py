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


"""Ce fichier contient l'éditeur EdtEvenement, détaillé plus bas."""

from textwrap import wrap

from primaires.interpreteur.editeur import Editeur
from primaires.interpreteur.editeur.env_objet import EnveloppeObjet
from primaires.format.fonctions import *
from .edt_instructions import EdtInstructions

class EdtEvenement(Editeur):

    """Contexte-éditeur d'un évènement.

    L'objet appelant est l'évènement.

    """

    def __init__(self, pere, objet=None, attribut=None):
        """Constructeur de l'éditeur"""
        Editeur.__init__(self, pere, objet, attribut)
        self.ajouter_option("d", self.opt_supprimer_test)
        self.ajouter_option("r", self.opt_modifier_test)
        self.ajouter_option("h", self.opt_remonter_test)
        self.ajouter_option("b", self.opt_descendre_test)

    def opt_supprimer_test(self, arguments):
        """Supprime un test.

        Syntaxe :
            /d no

        """
        evenement = self.objet
        try:
            no = int(arguments) - 1
            assert no >= 0
            assert no < len(evenement.tests)
        except (ValueError, AssertionError):
            self.pere << "|err|Numéro invalide ({}).|ff|".format(arguments)
        else:
            evenement.supprimer_test(no)
            self.actualiser()

    def opt_modifier_test(self, arguments):
        """Modifie un test.

        Syntaxe :
            /r <id> <ligne>

        """
        evenement = self.objet
        msgs = arguments.split(" ")
        if len(msgs) < 2:
            self.pere << "|err|Précisez un numéro de test suivi " \
                    "d'une nouvelle suite de tests.|ff|"
            return

        try:
            i = int(msgs[0])
            assert i > 0
        except (ValueError, AssertionError):
            self.pere << "|err|Nombre invalide.|ff|"
            return

        msg = " ".join(msgs[1:])
        try:
            test = evenement.tests[i - 1]
        except IndexError:
            self.pere << "|err|Test introuvable.|ff|"
            return

        try:
            test.construire(msg)
        except ValueError as err:
            self.pere << "|err|Erreur lors du parsage du test.|ff|"
        else:
            self.actualiser()

    def opt_remonter_test(self, arguments):
        """Remonte un test.

        Syntaxe :
            /h no

        """
        evenement = self.objet
        try:
            no = int(arguments) - 1
            assert no > 0
            assert no < len(evenement.tests)
        except (ValueError, AssertionError):
            self.pere << "|err|Numéro invalide ({}).|ff|".format(arguments)
        else:
            evenement.remonter_test(no)
            self.actualiser()

    def opt_descendre_test(self, arguments):
        """Descend un test.

        Syntaxe :
            /b no

        """
        evenement = self.objet
        try:
            no = int(arguments) - 1
            assert no >= 0
            assert no < len(evenement.tests) - 1
        except (ValueError, AssertionError):
            self.pere << "|err|Numéro invalide ({}).|ff|".format(arguments)
        else:
            evenement.descendre_test(no)
            self.actualiser()

    def accueil(self):
        """Message d'accueil du contexte"""
        evenement = self.objet
        msg = "| |tit|"
        msg += "Édition de l'évènement {} de {}".format(evenement.nom_complet,
                evenement.script.parent).ljust(76)
        msg += "|ff||\n" + self.opts.separateur + "\n"
        paragraphes = ["\n".join(wrap(p)) for p in evenement.aide_longue.split(
                "\n")]
        aide_longue = "\n".join(paragraphes)
        msg += aide_longue + "\n\n"
        variables = evenement.variables.values()
        if variables:
            msg += "Variables définies dans ce script :\n"
            t_max = 0
            for v in variables:
                if len(v.nom) > t_max:
                    t_max = len(v.nom)
            lignes = ["|grf|" + var.nom.ljust(t_max) + "|ff| : " + var.aide \
                    for var in variables]
            msg += "\n".join(lignes)
            msg += "\n\n"
        evenements = sorted(evenement.evenements.values(),
                key=lambda evt: evt.nom)
        if evenements:
            msg += "|cy|Sous-évènements disponibles :|ff|\n\n"
            t_max = 0
            for evt in evenements:
                if len(evt.nom) > t_max:
                    t_max = len(evt.nom)
            lignes = ["  " + evt.nom.ljust(t_max) + " : " + evt.aide_courte \
                    for evt in evenements]
            msg += "\n".join(lignes)
        else:
            msg += "|cy|Options :\n\n"
            msg += " Entrez |ent|une suite de prédicats|ff| pour "
            msg += "ajouter un test\n"
            msg += " Ou |ent|un numéro de ligne|ff| pour l'éditer\n"
            msg += " Ou |cmd|*|ff| pour éditer le test sinon\n"
            msg += " |cmd|/d <numéro de ligne>|ff| pour supprimer un test\n"
            msg += " |cmd|/r <numéro de ligne> <prédicats>|ff| pour "
            msg += "modifier un test\n"
            msg += " |cmd|/h <numéro de ligne>|ff| pour remonter un test\n"
            msg += " |cmd|/b <numéro de ligne>|ff| pour descendre un test\n\n"
            msg += "|cy|Conditions :|ff|\n"
            tests = evenement.tests
            longueur = 1
            if tests:
                if len(tests) >= 10:
                    longueur = 2
                for i, test in enumerate(tests):
                    si = "|mr|si|ff| " if i == 0 else "|mr|sinon si|ff| "
                    msg += "\n  |cmd|" + str(i + 1).rjust(longueur) + "|ff| "
                    msg += si + str(test)
            msg += "\n " + " " * longueur + "|cmd|*|ff| |mr|sinon|ff|"

        return msg

    def interpreter(self, msg):
        """Interprétation de l'éditeur"""
        evenement = self.objet
        if evenement.evenements:
            nom_evt = supprimer_accents(msg).lower()
            if nom_evt in evenement.evenements:
                evenement = evenement.evenements[nom_evt]
                enveloppe = EnveloppeObjet(EdtEvenement, evenement)
                enveloppe.parent = self
                contexte = enveloppe.construire(self.pere)

                self.migrer_contexte(contexte)
            else:
                self.pere << "|err|Cet évènement n'existe pas.|ff|"
            return

        if msg == "*":
            if evenement.sinon is None:
                evenement.creer_sinon()

            enveloppe = EnveloppeObjet(EdtInstructions, evenement.sinon)
            enveloppe.parent = self
            contexte = enveloppe.construire(self.pere)

            self.migrer_contexte(contexte)
        elif msg.isdigit():
            no_tests = int(msg) - 1
            try:
                tests = evenement.tests[no_tests]
            except IndexError:
                self.pere << "|err|Ce test n'existe pas.|ff|"
            else:
                enveloppe = EnveloppeObjet(EdtInstructions, tests)
                enveloppe.parent = self
                contexte = enveloppe.construire(self.pere)

                self.migrer_contexte(contexte)
        elif not msg:
            self.pere << "|err|Précisez un test.|ff|"
        else:
            try:
                evenement.ajouter_test(msg)
            except ValueError as err:
                self.pere << "|err|Erreur lors du parsage du test.|ff|"
            else:
                self.actualiser()
