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


"""Ce fichier définit le contexte-éditeur 'présentation'."""

from collections import OrderedDict

from corps.math import aff_flottant
from primaires.format.fonctions import oui_ou_non, supprimer_accents
from . import Editeur
from .quitter import Quitter
from .env_objet import EnveloppeObjet
from .flag import Flag
from .flottant import Flottant

class Presentation(Editeur):

    """Contexte-éditeur présentation.

    Ce contexte présente un objet, c'est-à-dire qu'il va être à la racine
    des différentes manipulations de l'objet. C'est cet objet que l'on
    manipule si on souhaite ajouter des configurations possibles.

    """

    nom = "editeur:base:presentation"
    def __init__(self, pere, objet=None, attribut=None, peut_quitter=True):
        """Constructeur de l'éditeur"""
        Editeur.__init__(self, pere, objet, attribut)
        self.choix = OrderedDict()
        self.raccourcis = {}
        self.nom_quitter = "quitter la fenêtre" if peut_quitter else ""
        if peut_quitter:
            self.ajouter_choix(self.nom_quitter, "q", Quitter)

    def get_raccourci_depuis_nom(self, recherche):
        """Retourne le raccourci grâce au nom"""
        for raccourci, nom in self.raccourcis.items():
            if nom == recherche:
                return raccourci

        raise KeyError("le raccourci du nom {} est introuvable".format(
                recherche))

    def ajouter_choix(self, nom, raccourci, objet_editeur,
            objet_edite=None, attribut=None, *sup):
        """Ajoute un choix possible :

        -   nom : le nom affiché dans la présentation (exemple 'description')
        -   raccourci : le raccourci pour entrer dans le sous éditeur ('d')
        -   objet_editeur : l'objet contexte-édieur (ex. zone de texte)
        -   objet édité : l'objet à éditer (par défaut self.objet)
        -   l'attribut à éditer : par défaut aucun

        """
        if raccourci is None:
            titre = supprimer_accents(nom).lower()
            nb = 1
            while nb < len(titre):
                i = 0
                while i + nb <= len(titre):
                    morceau = titre[i:i + nb]
                    if morceau not in self.raccourcis:
                        raccourci = morceau
                        break

                    i += 1

                if raccourci:
                    break

                nb += 1

            if raccourci is None:
                raise ValueError("Impossible de trouver " \
                    "le raccourci pour {}".format(self))

        return self.ajouter_choix_avant(self.nom_quitter, nom, raccourci,
                objet_editeur, objet_edite, attribut, *sup)

    def ajouter_choix_apres(self, apres, nom, raccourci, objet_editeur,
            objet_edite=None, attribut=None, *sup):
        """Ajout le choix après 'apres'.

        Pour les autres arguments, voir la méthode 'ajouter_choix'.

        """
        if raccourci in self.raccourcis.keys():
            raise ValueError(
                "Le raccourci {} est déjà utilisé dans cet éditeur".format(
                raccourci))

        enveloppe = EnveloppeObjet(objet_editeur, objet_edite, attribut, *sup)
        self.choix[nom] = enveloppe
        passage_apres = False
        if apres:
            for cle in tuple(self.choix.keys()):
                if passage_apres and cle != nom:
                    self.choix.move_to_end(cle)
                if cle == apres:
                    passage_apres = True

        self.raccourcis[raccourci] = nom
        enveloppe.parent = self
        enveloppe.apercu = "{valeur}"
        return enveloppe

    def ajouter_choix_avant(self, avant, nom, raccourci, objet_editeur,
            objet_edite=None, attribut=None, *sup):
        """Ajoute le choix avant 'avant''.
        Pour les autres arguments, voir la méthode 'ajouter_choix'.

        """
        if raccourci in self.raccourcis.keys():
            raise ValueError(
                "Le raccourci {} est déjà utilisé dans cet éditeur".format(
                raccourci))

        enveloppe = EnveloppeObjet(objet_editeur, objet_edite, attribut, *sup)
        self.choix[nom] = enveloppe
        passage_apres = False
        if avant:
            for cle in tuple(self.choix.keys()):
                if cle == avant:
                    passage_apres = True
                if passage_apres and cle != nom:
                    self.choix.move_to_end(cle)

        self.raccourcis[raccourci] = nom
        enveloppe.parent = self
        enveloppe.apercu = "{valeur}"
        return enveloppe

    def supprimer_choix(self, nom):
        """Supprime le choix possible 'nom'"""
        # On recherche le raccourci pour le supprimer
        for cle, valeur in tuple(self.raccourcis.items()):
            if valeur == nom:
                del self.raccourcis[cle]

        del self.choix[nom]

    def accueil(self):
        """Message d'accueil du contexte"""
        msg = "| |tit|Edition de {}|ff|".format(self.objet).ljust(87) + "|\n"
        msg += self.opts.separateur + "\n"

        # Parcourt des choix possibles
        for nom, objet in self.choix.items():
            raccourci = self.get_raccourci_depuis_nom(nom)

            # On constitue le nom final
            # Si le nom d'origine est 'description' et le raccourci est 'd',
            # le nom final doit être '[D]escription'
            nom_maj = nom
            if objet.lecture_seule:
                nom_m = "[-] " + nom_maj.capitalize()
            else:
                pos = supprimer_accents(nom).lower().find(raccourci)
                if pos >= 0:
                    raccourci = nom[pos:pos + len(raccourci)]
                    raccourci = raccourci[0].upper() + raccourci[1:]
                nom_m = nom_maj[:pos] + "[|cmd|" + raccourci + "|ff|]" + \
                        nom_maj[pos + len(raccourci):]
            msg += "\n " + nom_m
            if issubclass(objet.editeur, Flag):
                apercu = oui_ou_non(getattr(objet.objet,
                        objet.attribut))
            else:
                apercu = objet.get_apercu()
            if apercu:
                msg += " : " + apercu

        return msg

    def interpreter(self, msg):
        """Interprétation de la présentation"""
        msg = supprimer_accents(msg.rstrip().lower())
        try:
            nom = self.raccourcis[msg]
        except KeyError:
            if msg:
                self.autre_interpretation(msg)
        else:
            enveloppe = self.choix[nom]
            if enveloppe.lecture_seule:
                self.pere << "|err|Vous ne pouvez pas éditer ce champ.|ff|"
                return

            contexte = enveloppe.construire(self.pere)
            self.migrer_contexte(contexte)

    def autre_interpretation(self, msg):
        """Cette méthode peut être redéfini par les filles de presentation.

        Elle permet de rendre l'éditeur capable d'interpréter d'autres
        choses que des options et des raccourcis.
        Par défaut, envoie un message d'erreur à l'utilisateur.

        """
        self.pere << "|err|Raccourci inconnu ({}).|ff|".format(msg)
