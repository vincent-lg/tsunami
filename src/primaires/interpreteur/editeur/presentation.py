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


"""Ce fichier définit le contexte-éditeur 'présentation'."""

from collections import OrderedDict
from . import Editeur
from .quitter import Quitter
from .env_objet import EnveloppeObjet

class Presentation(Editeur):
    
    """Contexte-éditeur présentation.
    Ce contexte présente un objet, c'est-à-dire qu'il va être à la racine
    des différentes manipulations de l'objet. C'est cet objet que l'on
    manipule si on souhaite ajouter des configurations possibles.
    
    """
    
    nom = "editeur:base:presentation"
    def __init__(self, pere, objet=None, attribut=None):
        """Constructeur de l'éditeur"""
        Editeur.__init__(self, pere, objet, attribut)
        self.choix = OrderedDict()
        self.raccourcis = {}
        self.nom_quitter = "quitter la fenêtre"
        self.ajouter_choix(self.nom_quitter, "q", Quitter)
    
    def get_raccourci_depuis_nom(self, recherche):
        """Retourne le raccourci grâce au nom"""
        for raccourci, nom in self.raccourcis.items():
            if nom == recherche:
                return raccourci
        
        raise KeyError("le raccourci du nom {} est introuvable".format(
                recherche))
    
    def ajouter_choix(self, nom, raccourci, objet_editeur,
            objet_edite=None, attribut=None):
        """Ajoute un choix possible :
        -   nom : le nom affiché dans la présentation (exemple 'description')
        -   raccourci : le raccourci pour entrer dans le sous éditeur ('d')
        -   objet_editeur : l'objet contexte-édieur (ex. zone de texte)
        -   objet édité : l'objet à éditer (par défaut self.objet)
        -   l'attribut à éditer : par défaut aucun
        
        """
        return self.ajouter_choix_avant(self.nom_quitter, nom, raccourci,
                objet_editeur, objet_edite, attribut)
        
    def ajouter_choix_apres(self, apres, nom, raccourci, objet_editeur,
            objet_edite=None, attribut=None):
        """Ajout le choix après 'apres'.
        Pour les autres arguments, voir la méthode 'ajouter_choix'.
        
        """
        if raccourci in self.raccourcis.keys():
            raise ValueError(
                "Le raccourci {} est déjà utilisé dans cet éditeur".format(
                raccourci))
        
        enveloppe = EnveloppeObjet(objet_editeur, objet_edite, attribut)
        self.choix[nom] = enveloppe
        passage_apres = False
        for cle in tuple(self.choix.keys()):
            if passage_apres and cle != nom:
                self.choix.move_to_end(cle)
            if cle == apres:
                passage_apres = True
        
        self.raccourcis[raccourci] = nom
        return enveloppe

    def ajouter_choix_avant(self, avant, nom, raccourci, objet_editeur,
            objet_edite=None, attribut=None):
        """Ajoute le choix avant 'avant''.
        Pour les autres arguments, voir la méthode 'ajouter_choix'.
        
        """
        if raccourci in self.raccourcis.keys():
            raise ValueError(
                "Le raccourci {} est déjà utilisé dans cet éditeur".format(
                raccourci))
        
        enveloppe = EnveloppeObjet(objet_editeur, objet_edite, attribut)
        self.choix[nom] = enveloppe
        passage_apres = False
        for cle in tuple(self.choix.keys()):
            if cle == avant:
                passage_apres = True
            if passage_apres and cle != nom:
                self.choix.move_to_end(cle)
        
        self.raccourcis[raccourci] = nom
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
            pos = nom.find(raccourci)
            raccourci = ((pos == 0) and raccourci.capitalize()) or raccourci
            nom_maj = nom.capitalize()
            nom_m = nom_maj[:pos] + "[|cmd|" + raccourci + "|ff|]" + \
                    nom_maj[pos + len(raccourci):]
            msg += "\n " + nom_m
            enveloppe = self.choix[nom]
            apercu = enveloppe.get_apercu()
            if apercu:
                msg += " : " + apercu
        
        return msg
    
    def interpreter(self, msg):
        """Interprétation de la présentation"""
        try:
            nom = self.raccourcis[msg.rstrip().lower()]
        except KeyError:
            if msg:
                self.pere << "|err|Raccourci inconnu ({}).|ff|".format(msg)
        else:
            contexte = self.choix[nom].construire(self.pere)
            self.migrer_contexte(contexte)
