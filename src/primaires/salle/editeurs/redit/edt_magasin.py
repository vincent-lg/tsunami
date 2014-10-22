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
from primaires.format.fonctions import oui_ou_non

class EdtMagasin(Editeur):
    
    """Contexte-éditeur d'édition du magasin d'une salle.
    
    """
    
    def __init__(self, pere, objet=None, attribut=None):
        """Constructeur de l'éditeur"""
        Editeur.__init__(self, pere, objet, attribut)
        self.ajouter_option("v", self.opt_changer_vendeur)
        self.ajouter_option("o", self.opt_ouverture)
        self.ajouter_option("f", self.opt_fermeture)
        #self.ajouter_option("r", self.opt_renouvelement)
        self.ajouter_option("ro", self.opt_renouveler_ouverture)
        self.ajouter_option("rf", self.opt_renouveler_fermeture)
        #self.ajouter_option("xu", self.opt_max_unitaire)
        #self.ajouter_option("xt", self.opt_max_total)
        self.ajouter_option("ty", self.opt_types_vente)
        self.ajouter_option("s", self.opt_stock)
        self.ajouter_option("ren", self.opt_renouveler_inventaire)
        self.ajouter_option("h", self.opt_aide)
    
    def accueil(self):
        """Message d'accueil du contexte"""
        salle = self.objet
        msg = "| |tit|" + "Edition du magasin de {}".format(salle).ljust(76)
        msg += "|ff||\n" + self.opts.separateur + "\n"
        msg += self.aide_courte
        if salle.magasin is not None:
            magasin = salle.magasin
            cle_vendeur = magasin.prototype_vendeur and \
                    magasin.prototype_vendeur.cle or "|rg|aucun|ff|"
            vendeur = magasin.vendeur and magasin.vendeur.nom_singulier or "aucun"
            msg += "\n\nNom du magasin : " + salle.magasin.nom
            msg += "\nVendeur {} ({})".format(cle_vendeur, vendeur)
            msg += "\nOuverture à {:02}:{:02}   Fermeture à {:02}:" \
                    "{:02}".format(*(magasin.ouverture + magasin.fermeture))
            msg += "\nRenouvellement tous les {} jour(s)".format(
                    magasin.renouvellement_jours)
            msg += " (à l'ouverture {}   à la fermeture {})".format(
                    oui_ou_non(magasin.renouveler_ouverture), oui_ou_non(
                    magasin.renouveler_fermeture))
            msg += "\n\nTypes admis en vente : " + ", ".join(
                    magasin.types_vente)
            msg += "\nVente unitaire maximum {}   Vente totale maximum " \
                    "{}".format(magasin.aff_max_vente_unitaire,
                    magasin.aff_max_vente_total)
            msg += "\n\n" + str(salle.magasin)
        
        return msg
    
    def opt_changer_vendeur(self, arguments):
        """Change le prototype de PNJ du vendeur.
        
        /v <clé_prototype>
        
        """
        salle = self.objet
        if not salle.magasin:
            self.pere << "|err|Il n'y a pas de magasin dans cette salle.|ff|"
            return
        
        try:
            prototype = importeur.pnj.prototypes[arguments.lower().strip()]
        except KeyError:
            self.pere << "|err|Impossible de trouver le prototype de PNJ " \
                    "{}.|ff|".format(arguments)
            return
        
        salle.magasin.prototype_vendeur = prototype
        self.actualiser()
    
    def opt_renouveler_inventaire(self, arguments):
        """Met à jour l'inventaire du magasin depuis le stock.
        
        Syntaxe : /ren
        
        """
        salle = self.objet
        if not salle.magasin:
            self.pere << "|err|Il n'y a pas de magasin dans cette salle.|ff|"
            return
        
        magasin = salle.magasin
        magasin.renouveler()
        self.pere << "L'inventaire du magasin a bien été renouvelé."
    
    def opt_stock(self, arguments):
        """Modifie le stock.
        
        Syntaxe : /s <quantité> <type> <service>
        
        """
        salle = self.objet
        if not salle.magasin:
            self.pere << "|err|Il n'y a pas de magasin dans cette salle.|ff|"
            return
        if not arguments:
            self.pere << "|err|Précisez une quantité, un type et une clé.|ff|"
            return
        try:
            quantite, type, cle = arguments.split(" ")
        except ValueError:
            self.pere << "|err|Précisez une quantité, un type et une clé.|ff|"
            return
        
        # Conversion de la quantité
        try:
            quantite = int(quantite)
            assert quantite >= 0
        except (ValueError, AssertionError):
            self.pere << "|err|Quantité invalide.|ff|"
            return
        if type not in importeur.commerce.types_services:
            self.pere << "|err|Type {} invalide.|ff|".format(type)
            return
        
        objets = importeur.commerce.types_services[type]
        if quantite > 0:
            print(objets)
            if cle not in objets:
                self.pere << "|err|Le produit {} n'a pas pu être " \
                        "trouvé.|ff|".format(cle)
                return
            
            service = objets[cle]
            salle.magasin.ajouter_stock(service, quantite)
        else:
            salle.magasin.retirer_stock(type, cle)
        
        self.actualiser()
    
    def opt_aide(self, arguments):
        """Option d'aide.
        
        Syntaxe : /h (<service>)
        
        """
        if not arguments:
            ret = "Voici une liste des types de services que vous " \
                    "pouvez ajouter à ce magasin.\nPour de l'aide sur un " \
                    "type en particulier, entrez |ent|/h <type>|ff|.\n\n"
            ret += "Services disponibles :\n "
            ret += "\n ".join(importeur.commerce.types_services.keys())
            self.pere << ret
            return
        type = arguments.split(" ")[0]
        if not type in importeur.commerce.types_services:
            self.pere << "|err|Ce type de service n'existe pas.|ff|"
            return
        self.pere << importeur.commerce.aides_types[type]
    
    def opt_types_vente(self, arguments):
        """Ajoute ou supprime des types admis de vente.
        
        /ty <type>
        
        """
        nom_types = arguments.split("/")
        salle = self.objet
        if not salle.magasin:
            self.pere << "|err|Il n'y a pas de magasin dans cette salle.|ff|"
            return
        
        magasin = salle.magasin
        for nom_type in nom_types:
            nom_type = nom_type.strip()
            try:
                type = importeur.objet.get_type(nom_type)
            except KeyError:
                self.pere << "|err|Type inconnu {}.|ff|".format(nom_type)
                return
            else:
                nom_type = type.nom_type
                if nom_type in magasin.types_vente:
                    magasin.types_vente.remove(nom_type)
                else:
                    magasin.types_vente.append(nom_type)
                    magasin.types_vente.sort()
            self.actualiser()
    
    def opt_renouveler_ouverture(self, arguments):
        """Renouvelle à l'ouverture du magasin."""
        salle = self.objet
        if not salle.magasin:
            self.pere << "|err|Il n'y a pas de magasin dans cette salle.|ff|"
            return
        
        magasin = salle.magasin
        magasin.renouveler_ouverture = not magasin.renouveler_ouverture
        self.actualiser()
    
    def opt_renouveler_fermeture(self, arguments):
        """Renouvelle à la fermeture du magasin."""
        salle = self.objet
        if not salle.magasin:
            self.pere << "|err|Il n'y a pas de magasin dans cette salle.|ff|"
            return
        
        magasin = salle.magasin
        magasin.renouveler_fermeture = not magasin.renouveler_fermeture
        self.actualiser()
    
    def opt_ouverture(self, arguments):
        """Change l'heure d'ouverture.
        
        Sytaxe :
            /o <heure:minute>
        
        """
        salle = self.objet
        if not salle.magasin:
            self.pere << "|err|Il n'y a pas de magasin dans cette salle.|ff|"
            return
        
        magasin = salle.magasin
        try:
            heure, minute = arguments.split(":")
        except ValueError:
            self.pere << "|err|Syntaxe invalide. Précisez heure:minute " \
                    "(12:00 par exemple).|ff|"
            return
        
        try:
            heure = int(heure)
            minute = int(minute)
            assert 0 <= heure < 24
            assert 0 <= minute < 60
        except (ValueError, AssertionError):
            self.pere << "|err|Nombre invalide.|ff|"
            return
        
        magasin.ouverture = (heure, minute)
        self.actualiser()
    
    def opt_fermeture(self, arguments):
        """Change l'heure de fermeture.
        
        Sytaxe :
            /f <heure:minute>
        
        """
        salle = self.objet
        if not salle.magasin:
            self.pere << "|err|Il n'y a pas de magasin dans cette salle.|ff|"
            return
        
        magasin = salle.magasin
        try:
            heure, minute = arguments.split(":")
        except ValueError:
            self.pere << "|err|Syntaxe invalide. Précisez heure:minute " \
                    "(12:00 par exemple).|ff|"
            return
        
        try:
            heure = int(heure)
            minute = int(minute)
            assert 0 <= heure < 24
            assert 0 <= minute < 60
        except (ValueError, AssertionError):
            self.pere << "|err|Nombre invalide.|ff|"
            return
        
        magasin.fermeture = (heure, minute)
        self.actualiser()
    
    def interpreter(self, msg):
        """Interprétation de la présentation"""
        salle = self.objet
        if msg == "supprimer" and salle.magasin is not None:
            salle.magasin = None
            self.migrer_contexte(self.opts.rci_ctx_prec)
        else:
            if salle.magasin is None:
                salle.magasin = Magasin(msg, parent=salle)
                self.actualiser()
            else:
                salle.magasin.nom = msg
                self.actualiser()
