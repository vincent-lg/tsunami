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
# POSSIBILITY OF SUCH DAMAGE.


"""Fichier contenant la classe Magasin, détaillée plus bas."""

from abstraits.obase import *

class Magasin(BaseObj):
    
    """Cette classe représente un magasin.
    
    Un magasin possède plusieurs informations :
    -   Un inventaire des services [1] en vente actuellement
    -   Une liste de services en stock [2]
    -   Des taux d'achats et taux d'intérêts
    -   Une caisse représentant la liquidité du magasin
    
    [1] Les services nommés peuvent être de plusieurs types :
        l'obtension d'un objet en l'échange d'une somme est le service
        le plus évident, mais des PNJ peuvent également être achetés
        ainsi que d'autres types de services sur d'autres branches du moteur.
        Ainsi, l'implémentation d'un magasin est générique au possible.
    
    [2] Les services en stock sont ceux devant être renouvelés au moment
        opportun. Tous les services ne sont pas remplaçables et pas
        à la même vitesse. Les produits renouvelés passent du stock
        dans l'inventaire actuel du magasin mais ne disparaissent
        pas du stock.
    
    """
    
    def __init__(self, nom, parent=None):
        """Constructeur de la classe."""
        BaseObj.__init__(self)
        self.nom = nom
        self.parent = parent
        self._vendeur = ""
        self._monnaies = []
        self.caisse = 0
        self.inventaire = []
        self.stock = []
        self._construire()
    
    def __getnewargs__(self):
        return ("", )
    
    def __str__(self):
        """Affichage du magasin en éditeur."""
        services = sorted(self.stock, key=lambda s: s[0].valeur)
        if services:
            ret = "+" + "-" * 10 + "+" + "-" * 42 + "+" + "-" * 11 + "+" + \
                    "-" * 10 + "+\n"
            ret += "| |tit|" + "Type".ljust(8) + "|ff|"
            ret += " | |tit|" + "Nom".ljust(40) + "|ff|"
            ret += " |      |tit|Prix|ff| | |tit|Quantité|ff| |\n"
            ret += "+" + "-" * 10 + "+" + "-" * 42 + "+" + "-" * 11 + "+" + \
                    "-" * 10 + "+"
            for ligne in services:
                service, quantite, flags = ligne
                ret += "\n| " + service.type_achat.ljust(8) + " "
                ret += "| " + str(service).ljust(40) 
                ret += " | {:>9} | {:>8} |".format(service.valeur, quantite)
        else:
            ret = "|att|Aucun service en vente.|ff|"
        return ret
    
    def _get_vendeur(self):
        """Retourne le prototype vendeur"""
        if self._vendeur in type(self).importeur.pnj.prototypes:
            return type(self).importeur.pnj.prototypes[self._vendeur]
        else:
            self._vendeur = ""
            return None
    def _set_vendeur(self, cle):
        self._vendeur = cle
    vendeur = property(_get_vendeur, _set_vendeur)
    
    @property
    def cle_vendeur(self):
        """Retourne le nom du vendeur"""
        return ("|vrc|" + self._vendeur + "|ff|") if self._vendeur else \
                "|rgc|aucun|ff|"
    
    def afficher(self, personnage):
        """Affichage du magasin en jeu"""
        services = sorted(self.inventaire, key=lambda s: s[0].valeur)
        ret = self.nom + "\n\n"
        if services:
            ret = "+" + "-" * 6 + "+" + "-" * 42 + "+" + "-" * 11 + "+" + \
                    "-" * 10 + "+\n"
            ret += "| |tit|" + "ID".ljust(4) + "|ff|"
            ret += "| |tit|" + "Nom".ljust(42) + "|ff|"
            ret += "|       |tit|Prix|ff| | |tit|Quantité|ff| |\n"
            ret += "+" + "-" * 6 + "+" + "-" * 42 + "+" + "-" * 11 + "+" + \
                    "-" * 10 + "+"
            i = 1
            for ligne in services:
                service, quantite, flags = ligne
                ret += "\n| " + ("#" + str(i)).ljust(4) + " "
                res += "| " + service.nom_achat.ljust(40) 
                ret += "| {:<9} | {:<8} |".format(service.valeur, quantite)
        else:
            ret = "|att|Aucun produit n'est en vente actuellement.|ff|"
        return ret
    
    def ajouter_stock(self, service, quantite=1):
        """Ajoute un service dans le stock."""
        # D'abord on vérifie que le service n'est pas déjà présent
        # Si c'est le cas, on modifie simplement sa quantité
        for ligne in self.stock:
            if ligne[0].type_achat == service.type_achat and \
                    ligne[0].cle == service.cle:
                ligne[1] = quantite
                return
        
        self.stock.append((service, quantite, 0))
    
    def retirer_stock(self, type, cle):
        """Retire le service du stock."""
        for i, ligne in enumerate(list(self.stock)):
            service = ligne[0]
            if service.type_achat == type and service.cle == cle:
                del self.stock[i]
                return
        
        raise ValueError("le service {} {} n'existe pas".format(type, cle))
    
    def ajouter_inventaire(self, service, qtt, inc_qtt=True):
        """Ajoute des services dans l'inventaire.
        
        Si inc_qtt est à True, la quantité spécifiée est ajoutée à celle
        du service de l'inventaire, si présent. Sinon, la quantité du
        service, si présent, est remplacée par la nouvelle.
        
        """
        services = list(self.services)
        trouve = False
        for i, (t_service, t_qtt) in enumerate(services):
            if t_service is service:
                qtt = t_qtt if not inc_qtt else qtt
                services[i] = (t_service, qtt)
                trouve = True
                break
        
        if not trouve:
            services.append((service, qtt))
            services = sorted(services, key=lambda l: l[0].m_valeur)
        
        self.inventaire[:] = services
