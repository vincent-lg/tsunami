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


"""Fichier contenant le module primaire interpreteur."""

from collections import OrderedDict

from abstraits.module import *
from primaires.interpreteur.contexte import Contexte, contextes
from .editeur import Editeur
from primaires.interpreteur.masque.noeuds.fonctions import *
from primaires.interpreteur.masque.noeuds.base_noeud import BaseNoeud
from primaires.interpreteur.masque.noeuds.noeud_commande import NoeudCommande
from primaires.interpreteur.masque.fonctions import *
from primaires.interpreteur.commande.commande import Commande
from primaires.interpreteur.masque.masque import Masque
from primaires.interpreteur.masque.mot_cle import MotCle
from primaires.interpreteur.masque.exceptions.erreur_validation \
        import ErreurValidation
from primaires.interpreteur.groupe import ConteneurGroupes
from primaires.interpreteur.groupe.groupe import *
from .masque.masque import masques_def
from .options import UOptions

class Module(BaseModule):
    
    """Cette classe est la classe gérant tous les interpréteurs.
    Elle recense les différents contextes, en crée certains et permet
    à chaque module de créer ses propres contextes, commandes, éditeurs...
    
    """
    
    def __init__(self, importeur):
        """Constructeur du module"""
        BaseModule.__init__(self, importeur, "interpreteur", "primaire")
        self.logger = type(self.importeur).man_logs.creer_logger( \
                "interpreteur", "interpreteur")
        self.logger_cmd = type(self.importeur).man_logs.creer_logger( \
                "interpreteur", "commandes")
        
        # On passe l'interpréteur à certaines classes
        Contexte.importeur = importeur
        Commande.importeur = importeur
        BaseNoeud.importeur = importeur
        Masque.importeur = importeur
        
        # Attributs
        self.contextes = contextes # Dictionnaire des contextes
        self.commandes = []
        self.commandes_francais = []
        self.commandes_anglais = []
        self.categories = {}
        self.masques = masques_def
        
        # Editeurs
        self.editeurs = {}
        
        # Groupes d'utilisateurs
        self.groupes = None
        
        # Alias
        self.alias_anglais = {
                "+ooc": "+hrp",
                "-ooc": "-hrp",
                "ooc": "hrp",
                "l": "look",
                "eq": "equipment",
                "s": "sud",
                "s-o": "sud-ouest",
                "so": "sud-ouest",
                "o": "ouest",
                "n-o": "nord-ouest",
                "no": "nord-ouest",
                "n": "nord",
                "n-e": "nord-est",
                "ne": "nord-est",
                "e": "est",
                "s-e": "sud-est",
                "se": "sud-est",
                "h": "haut",
                "b": "bas",
        }
        self.alias_francais = {
                "+ooc": "+hrp",
                "-ooc": "-hrp",
                "ooc": "hrp",
                "r": "regarder",
                "eq": "equipement",
                "s": "sud",
                "s-o": "sud-ouest",
                "so": "sud-ouest",
                "o": "ouest",
                "n-o": "nord-ouest",
                "no": "nord-ouest",
                "n": "nord",
                "n-e": "nord-est",
                "ne": "nord-est",
                "e": "est",
                "s-e": "sud-est",
                "se": "sud-est",
                "h": "haut",
                "b": "bas",
        }
    
    def init(self):
        """Initialisation du module"""
        # On récupère ou crée puis configure les groupes d'utilisateur
        groupes = self.importeur.supenr.charger_unique(ConteneurGroupes)
        if groupes is None:
            groupes = ConteneurGroupes()
            self.logger.info("Aucun groupe d'utilisateurs récupéré")
        else:
            s = ""
            if len(groupes) > 1:
                s = "s"
            self.logger.info("{} groupe{s} d'utilisateurs récupéré{s}".format(
                        len(groupes), s = s))
        
        self.groupes = groupes
        
        # On vérifie que les groupes "essentiels" existent
        essentiels = OrderedDict((
            ("pnj", AUCUN),
            ("joueur", AUCUN),
            ("administrateur", IMMORTELS),
        ))
        
        # On crée ceux qui n'existent pas
        groupe_precedent = ""
        for nom_groupe, flags in essentiels.items():
            if nom_groupe not in self.groupes:
                groupe = self.groupes.ajouter_groupe(nom_groupe, flags)
                if groupe_precedent:
                    groupe.ajouter_groupe_inclus(groupe_precedent)
                self.logger.info("Ajout du groupe d'utilisateurs '{}'".format( 
                        nom_groupe))
            groupe_precedent = nom_groupe
        
        # On crée les catégories de commandes
        self.categories = OrderedDict()
        self.categories["divers"] = "Commandes générales"
        self.categories["info"] = "Information et aide en jeu"
        self.categories["bouger"] = "Mobilité et aide au déplacement"
        self.categories["combat"] = "Commandes de combat"
        self.categories["objets"] = "Gestion des objets et commerce"
        self.categories["parler"] = "Communication"
        self.categories["bugs"] = "Bugs et suggestions"
        self.categories["groupes"] = "Manipulation des groupes et modules"
        self.categories["batisseur"] = "Commandes de création"
        
        # On récupère les options utilisateurs
        options = self.importeur.supenr.charger_unique(UOptions)
        if options is None:
            options = UOptions()
        self.options = options
        
        BaseModule.init(self)
    
    def preparer(self):
        """Préparation du module."""
        for joueur in importeur.joueur.joueurs.values():
            if not joueur.alias_francais:
                joueur.alias_francais.update(self.alias_francais)
            if not joueur.alias_anglais:
                joueur.alias_anglais.update(self.alias_anglais)
    
    def ajouter_commande(self, commande):
        """Ajoute une commande à l'embranchement"""
        noeud_cmd = NoeudCommande(commande)
        self.commandes.append(noeud_cmd)
        
        # On ajoute la commande dans son groupe
        self.groupes.ajouter_commande(commande)
        
        # On construit ses paramètres
        commande.ajouter_parametres()
        
        # Tri de la liste des commandes, une première fois par ordre
        # alphabétique français la seconde par ordre alphabétique anglais
        self.commandes_francais = sorted(self.commandes, \
            key=lambda noeud: noeud.commande.nom_francais)
        self.commandes_anglais = sorted(self.commandes, \
            key=lambda noeud: noeud.commande.nom_anglais)
        
        # On appelle la méthode 'ajouter'
        commande.ajouter()
    
    def get_masque(self, nom_masque):
        """Retourne le masque portant le nom correspondant
        On retourne une nouvelle instance du masque.
        
        """
        return self.masques[nom_masque]()
    
    def repartir(self, personnage, masques, lst_commande):
        """Commande de validation"""
        str_commande = liste_vers_chaine(lst_commande)
        trouve = False
        commandes = self.lister_commandes_pour_groupe(personnage.grp)
        if personnage.langue_cmd == "francais":
            commandes.sort(key=lambda c: c.commande.nom_francais)
        elif personnage.langue_cmd == "anglais":
            commandes.sort(key=lambda c: c.commande.nom_anglais)
        
        for cmd in commandes:
            if cmd.repartir(personnage, masques, lst_commande):
                self.logger_cmd.info("{} envoie {}".format(personnage.nom,
                        str_commande))
                trouve = True
                break
        
        if not trouve:
            if lst_commande:
                raise ErreurValidation("|err|Commande inconnue.|ff|")	
            else:
                raise ErreurValidation()

    def valider(self, personnage, dic_masques):
        """Validation du dic_masques.
        
        On valide d'abord les masques prioritaires.
        
        """
        valides = []
        for masque in dic_masques.values():
            if masque.prioritaire:
                masque.valider(personnage, dic_masques)
                valides.append(masque)
        
        for masque in dic_masques.values():
            if masque not in valides:
                masque.valider(personnage, dic_masques)
    
    def trouver_commande(self, lst_commande, commandes=None):
        """On cherche la commande correspondante.
        
        Ce peut être une commande mais aussi une sous-commande, du premier
        niveau ou plus.
        
        Pour indiquer la position de la commande, on a lst_commande contenant
        une chaîne sous la forme : 'commande:sous_commande:sous_sous_commande'
        
        Ainsi, on appelle récursivement cette fonction.
        
        """
        if commandes is None: # premier appel de la récursivité
            commandes = self.commandes
        
        if type(lst_commande) is str:
            lst_commande = chaine_vers_liste(lst_commande)
        
        str_commande = liste_vers_chaine(lst_commande)
        
        nom_commande = str_commande.split(":")[0]
        # On parcourt la liste des commandes
        for noeud in commandes:
            if noeud.commande.nom_francais == nom_commande:
                lst_commande[:] = lst_commande[len(nom_commande) + 1:]
                if lst_commande:
                    fils = noeud.fils
                    return self.trouver_commande(lst_commande, fils)
                else:
                    return noeud.commande
        
        raise ValueError("la commande {} ne peut être trouvée, " \
            "la recherche de {} a échoué".format(str_commande, nom_commande))
    
    def ajouter_editeur(self, editeur):
        """Ajoute l'éditeur en fonction de son nom"""
        self.editeurs[editeur.nom] = editeur
    
    def supprimer_editeur(self, nom):
        """Supprime l'éditeur"""
        del self.editeurs[nom]
    
    def construire_editeur(self, nom, personnage, objet):
        """Retourne l'éditeur construit"""
        cls_editeur = self.editeurs[nom]
        editeur = cls_editeur(personnage, objet)
        return editeur
    
    def creer_mot_cle(self, francais, anglais):
        """Crée et retourne un mot-clé."""
        return MotCle(francais, anglais)
    
    def lister_commandes_pour_groupe(self, groupe):
        """Liste les commandes que le groupe donné a le droit d'exécuter."""
        groupes = self.groupes.commandes.copy()
        p_groupes = groupe.get_groupes_inclus()
        commandes = []
        for cmd in self.commandes:
            t_groupe = groupes[cmd.commande.adresse]
            if t_groupe in p_groupes:
                commandes.append(cmd)
        
        return commandes
