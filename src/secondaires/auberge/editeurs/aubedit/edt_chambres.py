# -*-coding:Utf-8 -*

# Copyright (c) 2013 LE GOFF Vincent
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


"""Ce fichier contient l'éditeur EdtChambres, détaillé plus bas."""

from primaires.interpreteur.editeur import Editeur
from primaires.interpreteur.editeur.env_objet import EnveloppeObjet
from secondaires.auberge.editeurs.aubedit.edt_chambre import EdtChambre
from primaires.format.fonctions import supprimer_accents

class EdtChambres(Editeur):

    """Contexte-éditeur des chambres d'une auberge."""

    def __init__(self, pere, objet=None, attribut=None):
        """Constructeur de l'éditeur"""
        Editeur.__init__(self, pere, objet, attribut)
        self.ajouter_option("c", self.opt_creer_chambre)
        self.ajouter_option("d", self.opt_supprimer_chambre)

    def accueil(self):
        """Message d'accueil du contexte"""
        auberge = self.objet
        msg = "| |tit|" + "Édition des chambres de l'auberge {}".format(
                auberge.cle).ljust(76)
        msg += "|ff||\n" + self.opts.separateur + "\n"
        msg += "Cet éditeur vous permet d'ajouter ou de supprimer des\n" \
                "chambres dans cette auberge. Entrez simplement son " \
                "numéro pour\nl'éditer.\n\n" \
                "Options disponibles :\n" \
                " |cmd|/c <numéro> <identifiant_de_salle>|ff| pour " \
                "ajouter une chambre\n" \
                " |cmd|/d <numéro>|ff| pour supprimer une chambre\n\n" \
                "Exemplels :\n" \
                "|ent|/c 1 zone:cle|ff|\n" \
                "|ent|/c suite zone:cle|ff|\n" \
                "|ent|/d 1|ff|\n" \
                "(Notez que le numéro n'est pas nécessairement un nombre.\n\n"
        msg += "Chambres définies :\n"
        if len(auberge.chambres) == 0:
            msg += "\n  Aucune"
        else:
            chambres = sorted([c for c in auberge.chambres.values()],
                    key=lambda c: c.numero)
            for chambre in chambres:
                msg += "\n  |ent|" + chambre.numero + "|ff|"
                msg += " vers + " + chambre.ident_salle

        return msg

    def opt_creer_chambre(self, arguments):
        """Ajoute une chambre.

        Syntaxe :
            /a <numéro> <ident_salle>

        """
        arguments = arguments.lower()
        auberge = self.objet
        if arguments.strip() == "":
            self.pere << "|err|Précisez |ent|un numéro|ff| et |ent|un " \
                    "identifiant de salle.|ff|"
            return

        try:
            numero, ident = arguments.split(" ")
        except ValueError:
            self.pere << "|err|Syntaxe invalide : |ent|/a <numéro> " \
                    "<ident_salle>|ff|"
            return

        if numero in auberge.numero_chambres:
            self.pere << "|err|Ce numéro est déjà utilisé.|ff|"
            return

        try:
            salle = importeur.salle[ident]
        except KeyError:
            self.pere << "|err|La salle '{}' est introuvable.|ff|".format(
                    ident)
            return

        auberge.ajouter_chambre(numero, salle)
        self.actualiser()

    def opt_supprimer_chambre(self, arguments):
        """Supprime la chambre passée en paramètre.

        Syntaxe :
            /d <numéro>

        """
        auberge = self.objet
        chambre = auberge.get_chambre_avec_numero(arguments)
        if chambre:
            auberge.supprimer_chambre(chambre.ident_salle)
            self.actualiser()
        else:
            self.pere << "|err|Chambre introuvable.|ff|"

    def interpreter(self, msg):
        """Interprétation de l'éditeur"""
        auberge = self.objet
        chambre = auberge.get_chambre_avec_numero(msg)
        if chambre:
            enveloppe = EnveloppeObjet(EdtChambre, chambre)
            enveloppe.parent = self
            contexte = enveloppe.construire(self.pere)

            self.migrer_contexte(contexte)
        else:
            self.pere << "|err|Chambre {} introuvable.|ff|".format(repr(msg))
