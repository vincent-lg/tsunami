# -*-coding:Utf-8 -*

# Copyright (c) 2010 LE GOFF Vincent
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


"""Ce fichier contient l'éditeur EdtScript, détaillé plus bas."""

from primaires.interpreteur.editeur import Editeur
from primaires.interpreteur.editeur.env_objet import EnveloppeObjet
from primaires.format.fonctions import *
from .edt_evenement import EdtEvenement
from .edt_instructions import EdtInstructions

class EdtScript(Editeur):

    """Contexte-éditeur des évènements d'uns script.

    L'objet appelant est le script.
    Ses évènements se trouvent dans l'attribut evenements
    (en lecture uniquement).

    """

    def __init__(self, pere, objet=None, attribut=None):
        """Constructeur de l'éditeur"""
        Editeur.__init__(self, pere, objet, attribut)
        self.ajouter_option("a", self.opt_ajouter_bloc)
        self.ajouter_option("d", self.opt_supprimer_bloc)
        self.ajouter_option("av", self.opt_ajouter_variable)
        self.ajouter_option("dv", self.opt_supprimer_variable)

    def opt_ajouter_bloc(self, argument):
        """Ajoute un nouveau bloc.

        Syntaxe :
            /a <nom du bloc>

        """
        script = self.objet
        bloc = supprimer_accents(argument.lower())
        try:
            script.creer_bloc(bloc)
        except ValueError as err:
            self.pere << "|err|" + str(err).capitalize() + ".|ff|"
        else:
            self.actualiser()

    def opt_supprimer_bloc(self, argument):
        """Supprime un bloc existant.

        Syntaxe :
            /d <nom du bloc>

        """
        script = self.objet
        bloc = supprimer_accents(argument.lower())
        try:
            script.supprimer_bloc(bloc)
        except ValueError as err:
            self.pere << "|err|" + str(err).capitalize() + ".|ff|"
        else:
            self.actualiser()

    def opt_ajouter_variable(self, argument):
        """Ajoute une variable à un bloc.

        Syntaxe :
            /av <nom du bloc> <nom de la variable> <type> <aide>

        """
        script = self.objet
        arguments = argument.split(" ")
        if len(arguments) < 4:
            self.pere << "|err|Précisez le nom du bloc, le nom de la " \
                    "variable, son type et l'aide de la variable.|ff|\n\n" \
                    "Exemple : |ent|/av planter age nombre l'âge de la " \
                    "plante|ff|"
            return

        bloc = supprimer_accents(arguments[0]).lower()
        variable = supprimer_accents(arguments[1]).lower()
        str_type = supprimer_accents(arguments[2])
        aide = " ".join(arguments[3:])
        if bloc not in script.blocs:
            self.pere << "|err|Le bloc '{}' n'existe pas.|ff|".format(bloc)
            return

        bloc = script.blocs[bloc]
        try:
            bloc.ajouter_variable(variable, str_type, aide)
        except ValueError as err:
            self.pere << "|err|" + str(err).capitalize() + ".|ff|"
        else:
            self.actualiser()

    def opt_supprimer_variable(self, argument):
        """Retire une variable d'un bloc.

        Syntaxe :
            /dv <nom du bloc> <nom de la variable>

        """
        script = self.objet
        arguments = argument.split(" ")
        if len(arguments) < 2:
            self.pere << "|err|Précisez le nom du bloc et le nom de la " \
                    "variable à supprimer.|ff|"
            return

        bloc = supprimer_accents(arguments[0]).lower()
        variable = supprimer_accents(arguments[1]).lower()
        if bloc not in script.blocs:
            self.pere << "|err|Le bloc '{}' n'existe pas.|ff|".format(bloc)
            return

        bloc = script.blocs[bloc]
        try:
            bloc.supprimer_variable(variable)
        except ValueError as err:
            self.pere << "|err|" + str(err).capitalize() + ".|ff|"
        else:
            self.actualiser()

    def accueil(self):
        """Message d'accueil du contexte"""
        script = self.objet
        msg = "| |tit|"
        msg += "Edition des scripts de {}".format(script.parent).ljust(76)
        msg += "|ff||\n" + self.opts.separateur + "\n"
        msg += "Voici les différents évènements que vous pouvez éditer pour " \
                "cet objet.\n" \
                "Entrez simplement son |ent|nom|ff| pour éditer un " \
                "évènement ou |cmd|/|ff| pour revenir à\n" \
                "la fenêtre parente.\n\n"
        evenements = sorted(script.evenements.values(),
                key=lambda evt: evt.nom)
        if evenements:
            def compter_lignes(evt):
                if not evt.evenements:
                    sinon = len(evt.sinon.instructions) if evt.sinon else 0
                    return sum(len(t.instructions) for t in evt.tests) + sinon
                else:
                    return sum(compter_lignes(e) for e in evt.evenements.values())
            msg += "|cy|Evènements disponibles :|ff|\n\n"
            t_max = 0
            for evt in evenements:
                if len(evt.nom) > t_max:
                    t_max = len(evt.nom)
            lignes = []
            for evt in evenements:
                ligne = "  " + evt.nom.ljust(t_max) + " : " + evt.aide_courte
                nb_lignes = compter_lignes(evt)
                if nb_lignes > 0:
                    ligne += " (|rgc|{}|ff| ligne{s})".format( \
                            nb_lignes, s="s" if nb_lignes > 1 else "")
                lignes.append(ligne)
            msg += "\n".join(lignes)
        else:
            msg += "|att|Aucun évènement n'est disponible pour cet objet.|ff|"

        msg += "\n\nBlocs définis :\n"
        if script.blocs:
            for bloc in sorted(script.blocs.values(), \
                    key=lambda bloc: bloc.nom):
                msg += "\n  " + bloc.nom + "("
                msg += ", ".join(v.nom for v in bloc.variables) + ")"
        else:
            msg += "\nAucun bloc n'a été défini dans ce script."

        return msg

    def interpreter(self, msg):
        """Interprétation de l'éditeur"""
        script = self.objet
        nom_evt = supprimer_accents(msg).lower()
        if nom_evt in script.evenements or script.creer_evenement_dynamique(
                msg):
            evenement = script.evenements[nom_evt]
            enveloppe = EnveloppeObjet(EdtEvenement, evenement)
            enveloppe.parent = self
            contexte = enveloppe.construire(self.pere)

            self.migrer_contexte(contexte)
        elif nom_evt in script.blocs:
            bloc = script.blocs[nom_evt]
            enveloppe = EnveloppeObjet(EdtInstructions, bloc.test)
            enveloppe.parent = self
            contexte = enveloppe.construire(self.pere)

            self.migrer_contexte(contexte)
        else:
            self.pere << "|err|Ce bloc ou évènement n'existe pas.|ff|"
