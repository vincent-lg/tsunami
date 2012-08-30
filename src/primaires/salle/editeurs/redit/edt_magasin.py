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
        #self.ajouter_option("v", self.opt_changer_vendeur)
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
            msg += "\n\nNom du magasin : " + salle.magasin.nom
            msg += "|ff|\n\n" + str(salle.magasin)
        
        return msg
    
    def opt_renouveler_inventaire(self, arguments):
        """Met à jour l'inventaire du magasin depuis le stock.
        
        Syntaxe : /ren
        
        """
        salle = self.objet
        if not salle.magasin:
            self.pere << "|err|Il n'y a pas de magasin dans cette salle.|ff|"
            return
        
        magasin = salle.magasin
        for service, qtt, flags in magasin.stock:
            magasin.ajouter_inventaire(service, qtt, inc_qtt=False)
        
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
