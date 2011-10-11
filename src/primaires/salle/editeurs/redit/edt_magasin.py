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


"""Ce fichier définit le contexte-éditeur 'edt_magasin'."""

from primaires.interpreteur.editeur import Editeur
from primaires.commerce.magasin import Magasin

class EdtMagasin(Editeur):
    
    """Contexte-éditeur d'édition du magasin d'une salle.
    
    """
    
    def __init__(self, pere, objet=None, attribut=None):
        """Constructeur de l'éditeur"""
        Editeur.__init__(self, pere, objet, attribut)
        self.ajouter_option("v", self.opt_changer_vendeur)
        self.ajouter_option("m", self.opt_monnaie)
        self.ajouter_option("c", self.opt_modifier_caisse)
        self.ajouter_option("o", self.opt_objet)
    
    def accueil(self):
        """Message d'accueil du contexte"""
        salle = self.objet
        msg = "| |tit|" + "Edition du magasin de {}".format(salle).ljust(76)
        msg += "|ff||\n" + self.opts.separateur + "\n"
        msg += self.aide_courte + "\n"
        if salle.magasin is not None:
            msg += "\nNom du magasin : " + salle.magasin.nom
            msg += "\nVendeur actuel : " + salle.magasin.nom_vendeur
            if len(salle.magasin.monnaies) != 1:
                msg += "\nMonnaies acceptées : "
            else:
                msg += "\nMonnaie acceptée : "
            msg += salle.magasin.liste_monnaies
            msg += "\nEtat de la caisse : |bc|" + str(salle.magasin.caisse)
            msg += "|ff|\n\n" + str(salle.magasin)
        
        return msg
    
    def opt_changer_vendeur(self, arguments):
        """Change le vendeur du magasin.
        Syntaxe : /v <prototype de bot>
        
        """
        salle = self.objet
        if not salle.magasin:
            self.pere << "|err|Il n'y a pas de magasin dans cette salle.|ff|"
            return
        if not arguments:
            self.pere << "|err|Précisez un prototype de PNJ.|ff|"
            return
        proto = arguments.split(" ")[0].lower()
        if not proto in type(self).importeur.pnj.prototypes:
            self.pere << "|err|Ce prototype est introuvable.|ff|"
            return
        proto = type(self).importeur.pnj.prototypes[proto]
        salle.magasin.vendeur = proto
        self.actualiser()
    
    def opt_monnaie(self, arguments):
        """Ajoute ou supprime une monnaie.
        Syntaxe : /m <objet de type argent>
        
        """
        salle = self.objet
        if not salle.magasin:
            self.pere << "|err|Il n'y a pas de magasin dans cette salle.|ff|"
            return
        if not arguments:
            self.pere << "|err|Précisez un prototype d'objet.|ff|"
            return
        monnaie = arguments.split(" ")[0].lower()
        if not monnaie in type(self).importeur.objet.prototypes:
            self.pere << "|err|Ce prototype est introuvable.|ff|"
            return
        monnaie = type(self).importeur.objet.prototypes[monnaie]
        if monnaie in salle.magasin.monnaies:
            salle.magasin.monnaies.remove(monnaie)
        else:
            salle.magasin.monnaies.append(monnaie)
        self.actualiser()
    
    def opt_modifier_caisse(self, arguments):
        """Modifie le contenu de la caisse.
        Syntaxe : /c <nombre>
        
        """
        salle = self.objet
        if not salle.magasin:
            self.pere << "|err|Il n'y a pas de magasin dans cette salle.|ff|"
            return
        if not arguments:
            self.pere << "|err|Précisez une valeur.|ff|"
            return
        try:
            valeur = int(arguments.split(" ")[0])
            assert valeur > 0
        except (ValueError, AssertionError):
            self.pere << "|err|Entrez un nombre valide et positif.|ff|"
            return
        else:
            salle.magasin.caisse = valeur
            self.actualiser()
    
    def opt_objet(self, arguments):
        """Ajoute ou supprime un objet.
        Syntaxe : /o <prototype d'objet> (<quantité>)
        
        """
        salle = self.objet
        if not salle.magasin:
            self.pere << "|err|Il n'y a pas de magasin dans cette salle.|ff|"
            return
        if not arguments:
            self.pere << "|err|Précisez un prototype d'objet.|ff|"
            return
        try:
            objet = arguments.split(" ")[0].lower()
            quantite = arguments.split(" ")[1].lower()
        except IndexError:
            objet = arguments.split(" ")[0].lower()
            if not salle.magasin.est_en_vente(objet):
                self.pere << "|err|Précisez une quantité pour cet objet.|ff|"
                return
            salle.magasin.retirer(objet)
        else:
            try:
                quantite = int(quantite)
                assert quantite > 0
            except (ValueError, AssertionError):
                self.pere << "|err|Précisez une quantité valide et " \
                        "positive.|ff|"
                return
            else:
                if not objet in type(self).importeur.objet.prototypes:
                    self.pere << "|err|Ce prototype est introuvable.|ff|"
                    return
                salle.magasin.ajouter_ou_modifier(objet, quantite)
        self.actualiser()
    
    def interpreter(self, msg):
        """Interprétation de la présentation"""
        salle = self.objet
        if msg == "supprimer" and salle.magasin is not None:
            salle.magasin = None
            self.migrer_contexte(rci_ctx_prec)
        else:
            if salle.magasin is None:
                salle.magasin = Magasin(msg, parent=salle)
                self.actualiser()
            else:
                salle.magasin.nom = msg
                self.actualiser()
