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

import re

from abstraits.obase import *
from primaires.format.constantes import COULEURS
from primaires.format.tableau import Tableau, GAUCHE, DROITE
from primaires.objet.objet import Objet
from primaires.objet.vente_unique import VenteUnique

class Magasin(BaseObj):

    """Cette classe représente un magasin.

    Un magasin possède plusieurs informations :
    -   Un inventaire des services [1] en vente actuellement
    -   Une liste de services en stock [2]
    -   Des taux d'achats et taux d'intérêts

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

    _nom = "magasin"
    _version = 1
    def __init__(self, nom, parent=None):
        """Constructeur de la classe."""
        BaseObj.__init__(self)
        self.nom = nom
        self.parent = parent
        self.prototype_vendeur = None
        self.inventaire = []
        self.stock = []
        self.renouvellement_jours = 1
        self.nb_jours = 0 # nombre de jours sans renouvellement
        self.renouveler_ouverture = True
        self.renouveler_fermeture = False
        self.ouverture = (8, 0)
        self.fermeture = (22, 0)
        self.vente_stock = True
        self.types_vente = []
        self.max_vente_unitaire = -1
        self.max_vente_total = 1000
        self._construire()

    def __getnewargs__(self):
        return ("", )

    def __str__(self):
        """Affichage du magasin en éditeur."""
        services = sorted(self.stock, key=lambda s: s[0].m_valeur)
        if services:
            ret = "+" + "-" * 12 + "+" + "-" * 42 + "+" + "-" * 10 + "+" + \
                    "-" * 10 + "+\n"
            ret += "| |tit|" + "Type".ljust(10) + "|ff|"
            ret += " | |tit|" + "Nom".ljust(40) + "|ff|"
            ret += " |     |tit|Prix|ff| | |tit|Quantité|ff| |\n"
            ret += "+" + "-" * 12 + "+" + "-" * 42 + "+" + "-" * 10 + "+" + \
                    "-" * 10 + "+"
            for ligne in services:
                service, quantite, flags = ligne
                nom_service = str(service)
                i = 0
                while len(nom_service) > 0:
                    if i == 0:
                        ret += "\n| " + service.type_achat.ljust(10) + " "
                        ret += "| " + nom_service[:40].ljust(40)
                        ret += " | {:>8} | {:>8} |".format(service.m_valeur,
                            quantite)
                        nom_service = nom_service[40:]
                    else:
                        ret += "\n|" + " " * 12 + "| ..."
                        ret += nom_service[:37].ljust(37)
                        ret += " |" + " " * 10 + "|" + " " * 10 + "|"
                        nom_service = nom_service[37:]
                    i += 1
            ret += "\n+" + "-" * 12 + "+" + "-" * 42 + "+" + "-" * 10 + "+" + \
                    "-" * 10 + "+"
        else:
            ret = "|att|Aucun service en vente.|ff|"
        return ret

    @property
    def vendeur(self):
        """Retourne, si trouvé, le PNJ représentant le vendeur."""
        if self.parent is None or self.prototype_vendeur is None:
            return None

        for pnj in self.parent.PNJ:
            if pnj.prototype is self.prototype_vendeur:
                return pnj

        return None

    @property
    def cle_vendeur(self):
        """Retourne la clé du vendeur."""
        return ("|vrc|" + self.prototype_vendeur.cle + "|ff|") if \
                self.prototype_vendeur else "|rgc|aucun|ff|"

    @property
    def aff_max_vente_unitaire(self):
        if self.max_vente_unitaire < 0:
            return "[infinie]"

        return self.max_vente_unitaire

    @property
    def aff_max_vente_total(self):
        if self.max_vente_total < 0:
            return "[infinie]"

        return self.max_vente_total

    @property
    def valeur_inventaire(self):
        return sum(s[0].m_valeur for s in self.inventaire)

    def afficher(self, personnage):
        """Affichage du magasin en jeu"""
        services = sorted(self.inventaire, key=lambda s: s[0].m_valeur)
        tableau = Tableau("|cy|" + self.nom + "|ff|")
        tableau.ajouter_colonne("|tit|ID|ff|")
        tableau.ajouter_colonne("|tit|Nom|ff|")
        tableau.ajouter_colonne("|tit|Prix|ff|")
        tableau.ajouter_colonne("|tit|Quantité|ff|")
        if services:
            i = 1
            for ligne in services:
                service, quantite = ligne
                nom = service.nom_achat
                prix = service.m_valeur
                tableau.ajouter_ligne("#" + str(i), nom, prix, quantite)
                i += 1
        else:
            msg = str(tableau)
            lignes = msg.splitlines()
            largeur = tableau.calculer_largeur()
            lignes.insert(-2, "| |att|" + "Aucun produit n'est en " \
                    "vente actuellement.".ljust(largeur - 4) + "|ff| |")
            return "\n".join(lignes)

        return tableau.afficher()

    def ajouter_stock(self, service, quantite=1):
        """Ajoute un service dans le stock."""
        # D'abord on vérifie que le service n'est pas déjà présent
        # Si c'est le cas, on modifie simplement sa quantité
        for i, ligne in enumerate(self.stock):
            if ligne[0].type_achat == service.type_achat and \
                    ligne[0].cle == service.cle:
                self.stock[i] = (ligne[0], quantite, ligne[2])
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

        Si service est de type objet, on applique la règle
        d'unicité : si l'objet semble unique (son nom est différent
        de celui de son prototype), on l'ajoute dans un service à
        part.

        Si inc_qtt est à True, la quantité spécifiée est ajoutée à celle
        du service de l'inventaire, si présent. Sinon, la quantité du
        service, si présent, est remplacée par la nouvelle.

        """
        services = list(self.inventaire)
        trouve = unique = False
        if isinstance(service, Objet):
            if service.nom_singulier != service.prototype.nom_singulier:
                service = VenteUnique(service)
                unique = True
            else:
                importeur.objet.supprimer_objet(service.identifiant)
                service = service.prototype

        if not unique:
            for i, (t_service, t_qtt) in enumerate(services):
                if t_service is service:
                    qtt = qtt if not inc_qtt else qtt + t_qtt
                    services[i] = (t_service, qtt)
                    trouve = True
                    break

        if not trouve:
            services.append((service, qtt))
            services = sorted(services, key=lambda l: l[0].m_valeur)

        self.inventaire[:] = services

    def retirer_inventaire(self, service, qtt):
        """Retire le service indiqué."""
        for i, (t_service, t_qtt) in enumerate(self.inventaire):
            if t_service is service:
                if qtt >= t_qtt:
                    del self.inventaire[i]
                else:
                    self.inventaire[i] = (t_service, t_qtt - qtt)
                return

        raise ValueError("service introuvable")

    def peut_acheter(self, vendeur, objet, qtt=1):
        """Retourne la valeur si le magasin peut acheter l'objet, False sinon.

        Un message peut être envoyé au vendeur si le magasin ne peut
        acheter l'objet.

        """
        acheteur = self.vendeur
        if acheteur is None:
            vendeur << "|err|Aucun marchand n'est présent pour le moment.|ff|"
            return False

        bon_type = False
        for type_vente in self.types_vente:
            if objet.est_de_type(type_vente):
                bon_type = True
                break

        if not bon_type:
            vendeur.envoyer("{} vous dit : je n'achète pas cela.", acheteur)
            return False

        if not objet.peut_vendre(vendeur):
            return False

        d_qtt = 0
        for service, t_qtt in self.inventaire:
            if service is objet.prototype:
                d_qtt = t_qtt
                break

        if d_qtt > 5:
            vendeur.envoyer("{} vous dit : j'en ai bien assez, merci !",
                    acheteur)
            return False

        valeur_achat = int(objet.estimer_valeur(self, vendeur))
        if self.max_vente_unitaire >= 0 and valeur_achat * qtt > \
                self.max_vente_unitaire:
            vendeur.envoyer("{} vous dit : c'est bien trop cher pour moi !",
                    acheteur)
            return False

        if self.max_vente_total >= 0 and self.valeur_inventaire + \
                valeur_achat * qtt > self.max_vente_total:
            vendeur.envoyer("{} vous dit : je n'ai besoin de rien de plus, " \
                    "merci.", acheteur)
            return False

        return valeur_achat * qtt

    def renouveler(self, vider=False):
        """Renouvelle l'inventaire depuis le stock."""
        if vider:
            self.inventaire[:] = []

        for service, qtt, flags in self.stock:
            self.ajouter_inventaire(service, qtt, inc_qtt=False)

    def ouvrir(self):
        """Ouverture du magasin."""
        vendeur = self.vendeur
        if vendeur is None and self.prototype_vendeur and \
                self.prototype_vendeur.pnj:
            vendeur = self.prototype_vendeur.pnj[0]

        if vendeur:
            vendeur.script["marchand"]["ouvre"].executer(pnj=vendeur)

    def fermer(self):
        """Fermeture du magasin."""
        vendeur = self.vendeur
        if vendeur:
            vendeur.script["marchand"]["ferme"].executer(pnj=vendeur)
