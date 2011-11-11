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


"""Ce fichier définit le contexte-éditeur 'edt_membres'."""

from primaires.interpreteur.editeur import Editeur
from primaires.interpreteur.editeur.env_objet import EnveloppeObjet
from primaires.format.fonctions import supprimer_accents
from .edt_membre import EdtMembre

class EdtMembres(Editeur):
    
    """Contexte-éditeur d'édition des membres.
    
    """
    
    def __init__(self, pere, objet=None, attribut=None):
        """Constructeur de l'éditeur"""
        Editeur.__init__(self, pere, objet, attribut)
        self.ajouter_option("d", self.opt_suppr_membre)
    
    def accueil(self):
        """Message d'accueil du contexte"""
        squelette = self.objet
        msg = "| |tit|" + "Edition des membres de {}".format(
                squelette.cle).ljust(76)
        msg += "|ff||\n" + self.opts.separateur + "\n"
        msg += self.aide_courte
        msg += "Membres courants :\n"
        
        # Parcours des membres
        membres = squelette.membres
        liste_membres = ""
        for membre in membres:
            ligne = "\n |ent|" + membre.nom.ljust(10) + "|ff|"
            liste_membres += ligne
        
        if not liste_membres:
            liste_membres += "\n |att|Aucun membre pour l'instant.|ff|"
        msg += liste_membres
        
        return msg
    
    def opt_suppr_membre(self, arguments):
        """Supprime un membre
        Syntaxe : /d nom
        
        """
        squelette = self.objet
        try:
            membre = squelette.get_membre(arguments)
        except KeyError:
            self.pere << "|err|Ce membre est introuvable.|ff|"
        else:
            squelette.supprimer_membre(membre.nom)
            self.actualiser()
    
    def interpreter(self, msg):
        """Interprétation de la présentation"""
        squelette = self.objet
        membres = squelette.membres
        nom = supprimer_accents(msg).lower()
       
        try: 
            membre = squelette.get_membre(nom)
        except KeyError:
            try:
                membre = squelette.ajouter_membre(msg)
            except ValueError:
                self.pere << "|err|Ce nom de membre est invalide.|ff|"
                return
        
        enveloppe = EnveloppeObjet(EdtMembre, membre, None)
        enveloppe.parent = self
        enveloppe.aide_courte = \
            "Entrez |ent|/|ff| pour revenir à la fenêtre parente.\n" \
            "Options :\n" \
            " - |ent|/n <nouveau nom>|ff| : modifie le nom du membre\n" \
            " - |ent|/g <groupe>|ff| : permet de regrouper plusieurs " \
            "membres\n" \
            " - |ent|/p <probabilité>|ff| : change la probabilité de " \
            "toucher le membre en combat\n" \
            " - |ent|/f <flag>|ff| : change l'état d'un flag\n"
        contexte = enveloppe.construire(self.pere)
        self.migrer_contexte(contexte)
