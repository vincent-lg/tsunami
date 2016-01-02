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
# POSSIBILITY OF SUCH DAMAGE.


"""Fichier contenant le module primaire commerce."""

from abstraits.module import *
from primaires.objet.vente_unique import VenteUnique
from . import masques
from . import commandes
from . import types
from .questeur import Questeur

class Module(BaseModule):

    """Cette classe contient les informations du module primaire commerce.

    Ce module gère le commerce, c'est-à-dire les transactions, les magasins,
    les monnaies.

    Note : on peut étendre ce module en proposant de nouveaux objets pouvant
    être vendus. Pour cela, il faut :
    1.  Lors de la configuration du module contenant les nouveaux
        objets, on doit signaler au module commerce qu'un nouveau type
        d'objet sera susceptible d'être vendu. Pour cela, il faut ajouter
        une entrée dans le dictionnaire types_services avec en clé le
        nom du nouveau service et en valeur, un dictionnaire permettant
        de trouver l'objet grâce à sa clé. Pour des exemples, regardez
        le module primaire objet
    2.  La classe produisant des objets pouvant être vendus en magasin
        doit posséder :
        A.  Un attribut de classe type_achat (str)
        B.  Un attribut de classe aide_achat (str)
        B.  Une propriété ou un attribut d'objet m_valeur (float)
        C.  Une propriété ou un attribut d'objet nom_achat (str)
        D.  Un attribut d'objet cle (str) correspondant à sa clé dans le
            dictionnaire
        E.  Une méthode acheter réalisant l'achat

    """

    def __init__(self, importeur):
        """Constructeur du module"""
        BaseModule.__init__(self, importeur, "commerce", "primaire")
        self.commandes = []
        self.types_services = {}
        self.aides_types = {}
        self.questeurs = {}
        type(importeur).espace["questeurs"] = self.questeurs

    def init(self):
        """Initialisation du module."""
        self.importeur.hook["temps:minute"].ajouter_evenement(
                self.renouveler_magasins)
        self.importeur.hook["objet:doit_garder"].ajouter_evenement(
                self.doit_garder_objets)

        # On récupère les questeurs
        questeurs = self.importeur.supenr.charger_groupe(Questeur)
        for questeur in questeurs:
            self.ajouter_questeur(questeur)

        BaseModule.init(self)

    def ajouter_commandes(self):
        """Ajout des commandes"""
        self.commandes = [
            commandes.acheter.CmdAcheter(),
            commandes.info.CmdInfo(),
            commandes.lister.CmdLister(),
            commandes.questeur.CmdQuesteur(),
            commandes.vendre.CmdVendre(),
        ]

        for cmd in self.commandes:
            importeur.interpreteur.ajouter_commande(cmd)

    def preparer(self):
        """Préparation du module."""
        for cle, questeur in tuple(self.questeurs.items()):
            if not cle.e_existe:
                del self.questeurs[cle]

    def creer_questeur(self, salle):
        """Crée un questeur et l'ajout dans le dictionnaire."""
        questeur = Questeur(salle)
        self.ajouter_questeur(questeur)
        return questeur

    def ajouter_questeur(self, questeur):
        """Ajoute le questeur dans le dictionnaire."""
        self.questeurs[questeur.salle] = questeur

    def questeur_existe(self, salle):
        """Retourne True ou False si le questeur existe dans la salle."""
        return self.questeurs.get(salle) is not None

    def supprimer_questeur(self, salle):
        """Supprime le questeur."""
        questeur = self.questeurs[salle]
        questeur.detruire()
        del self.questeurs[salle]

    def renouveler_magasins(self, temps):
        """Renouvelle les magasins."""
        magasins = importeur.salle.a_renouveler.get(temps.heure_minute,
                [])
        for magasin in magasins:
            magasin.inventaire[:] = []
            magasin.renouveler()

        magasins = importeur.salle.magasins_a_ouvrir.get(
                temps.heure_minute, [])
        for magasin in magasins:
            magasin.ouvrir()

        magasins = importeur.salle.magasins_a_fermer.get(
                temps.heure_minute, [])
        for magasin in magasins:
            magasin.fermer()

    def doit_garder_objets(self):
        """Retourne les objets à ne pas détruire."""
        a_garder = []
        for salle in importeur.salle.salles.values():
            if salle.magasin:
                for service, qtt in salle.magasin.inventaire:
                    if isinstance(service, VenteUnique) and service.objet:
                        a_garder.append(service.objet)

        return a_garder
