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


"""Ce fichier contient l'éditeur EdtChapitres, détaillé plus bas."""

from primaires.format.fonctions import supprimer_accents
from primaires.interpreteur.editeur import Editeur
from primaires.interpreteur.editeur.env_objet import EnveloppeObjet
from primaires.objet.types.editeurs.chapitre import EdtChapitre

class EdtChapitres(Editeur):

    """Contexte-éditeur des chapitres d'un livre."""

    def __init__(self, pere, objet=None, attribut=None):
        """Constructeur de l'éditeur"""
        Editeur.__init__(self, pere, objet, attribut)
        self.ajouter_option("a", self.opt_ajouter_chapitre)
        self.ajouter_option("d", self.opt_supprimer_chapitre)
        self.ajouter_option("h", self.opt_monter_chapitre)
        self.ajouter_option("b", self.opt_descendre_chapitre)

    def accueil(self):
        """Message d'accueil du contexte"""
        prototype = self.objet
        msg = "| |tit|" + "Édition des chapitres de {}".format(
                prototype.cle).ljust(76)
        msg += "|ff||\n" + self.opts.separateur + "\n"
        msg += \
                "Options disponibles :\n\n" \
                " |cmd|/a|ent| <titre du chapitre à ajouter>|ff|\n" \
                " |cmd|/d|ent| <numéro du chapitre à supprimer|ff|\n" \
                " |cmd|/h|ent| <numéro du chapitre à remonter|ff|\n" \
                " |cmd|/b|ent| <numéro du chapitre à descendre|ff|\n" \
                " Ou |ent|<numéro du chapitre à éditer>|ff|.\n\n"
        msg += "Chapitres existants :\n"

        # Parcours des chapitres
        for i, chapitre in enumerate(prototype.chapitres):
            msg += "\n |ent|" + str(i + 1).ljust(2)
            msg += "|ff| - " + chapitre.titre
        if not prototype.chapitres:
            msg += "\n Aucun chapitre pour l'instant."

        return msg

    def opt_ajouter_chapitre(self, arguments):
        """Ajoute le chapitre.

        Syntaxe :
          /a <titre du chapitre>

        """
        prototype = self.objet
        if not arguments.strip():
            self.pere << "|err|Précisez le titre du chapitre à ajouter.|ff|"
            return

        prototype.ajouter_chapitre(arguments)
        self.actualiser()

    def opt_supprimer_chapitre(self, arguments):
        """Supprime un chapitre.

        Syntaxe :
          /d <numéro du chapitre>

        """
        prototype = self.objet
        if not arguments.strip():
            self.pere << "|err|Précisez le numéro du chapitre à supprimer.|ff|"
            return

        try:
            no = int(arguments)
            assert 0 < no <= len(prototype.chapitres)
        except (ValueError, AssertionError):
            self.pere << "|err|Numéro invalide.|ff|"
            return

        prototype.supprimer_chapitre(no - 1)
        self.actualiser()

    def opt_monter_chapitre(self, arguments):
        """Monte un chapitre.

        Syntaxe :
          /h <numéro du chapitre>

        """
        prototype = self.objet
        if not arguments.strip():
            self.pere << "|err|Précisez le numéro du chapitre à remonter.|ff|"
            return

        try:
            no = int(arguments)
            assert 0 < no <= len(prototype.chapitres)
        except (ValueError, AssertionError):
            self.pere << "|err|Numéro invalide.|ff|"
            return

        prototype.monter_chapitre(no - 1)
        self.actualiser()

    def opt_descendre_chapitre(self, arguments):
        """Descend un chapitre.

        Syntaxe :
          /b <numéro du chapitre>

        """
        prototype = self.objet
        if not arguments.strip():
            self.pere << "|err|Précisez le numéro du chapitre à descendre.|ff|"
            return

        try:
            no = int(arguments)
            assert 0 < no <= len(prototype.chapitres)
        except (ValueError, AssertionError):
            self.pere << "|err|Numéro invalide.|ff|"
            return

        prototype.descendre_chapitre(no - 1)
        self.actualiser()

    def interpreter(self, msg):
        """Interprétation de l'éditeur"""
        prototype = self.objet
        try:
            no = int(msg)
            assert 0 < no <= len(prototype.chapitres)
        except (ValueError, AssertionError):
            self.pere << "|err|Numéro invalide.|ff|"
            return

        chapitre = prototype.chapitres[no - 1]
        enveloppe = EnveloppeObjet(EdtChapitre, chapitre, "")
        enveloppe.parent = self
        contexte = enveloppe.construire(self.pere)

        self.migrer_contexte(contexte)
