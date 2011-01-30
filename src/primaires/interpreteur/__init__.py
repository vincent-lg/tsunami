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

from abstraits.module import *
from primaires.interpreteur.contexte import Contexte
from primaires.interpreteur.masque.noeuds.fonctions import *
from primaires.interpreteur.masque.noeuds.base_noeud import BaseNoeud
from primaires.interpreteur.masque.noeuds.noeud_commande import NoeudCommande
from primaires.interpreteur.masque.fonctions import *
from primaires.interpreteur.commande.commande import Commande
from primaires.interpreteur.masque.masque import Masque
from primaires.interpreteur.masque.exceptions.erreur_validation \
        import ErreurValidation
from primaires.interpreteur.groupe import ConteneurGroupes

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
        
        # On passe l'interpréteur à certaines classes
        Contexte.importeur = importeur
        Commande.importeur = importeur
        BaseNoeud.importeur = importeur
        Masque.importeur = importeur
        
        # Attributs
        self.contextes = {} # Dictionnaire des contextes
        self.commandes = []
        self.commandes_francais = []
        self.commandes_anglais = []
        self.masques = {}
        
        # Groupes d'utilisateur
        self.groupes = None
    
    def init(self):
        """Initialisation du module"""
        # On récupère ou crée puis configure les groupes d'utilisateur
        groupes = self.importeur.supenr.charger("groupes", "groupes.sav")
        if groupes is None:
            groupes = ConteneurGroupes()
            self.logger.info("Aucun groupe d'utilisateur récupéré.")
        else:
            nb_groupes = len(groupes)
            self.logger.info("{} groupe(s) d'utilisateur récupéré(s)".format(
                    nb_groupes))
        
        self.groupes = groupes
        
        # On vérifie que les groupes "essentiels" existent
        essentiels = ("npc", "joueur", "administrateur")
        
        # On crée ceux qui n'existent pas
        groupe_precedent = ""
        for nom_groupe in essentiels:
            if nom_groupe not in self.groupes:
                groupe = self.groupes.ajouter_groupe(nom_groupe)
                if groupe_precedent:
                    groupe.ajouter_groupe_inclus(groupe_precedent)
                self.logger.info("On ajoute le groupe d'utilisateur {}".format( 
                        nom_groupe))
            groupe_precedent = nom_groupe
        
        BaseModule.init(self)
    
    def ajouter_contexte(self, nouv_contexte):
        """Ajoute le contexte dans le dictionnaire self.contextes.
        On se sert du nom comme identifiant du contexte.
        
        """
        self.contextes[nouv_contexte.nom] = nouv_contexte
    
    def ajouter_commande(self, commande):
        """Ajoute une commande à l'embranchement"""
        noeud_cmd = NoeudCommande(commande)
        self.commandes.append(noeud_cmd)
        
        # On ajoute la commande dans son groupe
        self.groupes.ajouter_commande(commande)
        
        # On construit ses paramètres
        commande.ajouter_parametres()
        
        # Tri la liste des commandes, une première fois par ordre alphabétique
        # français la seconde par ordre alphabétique anglais
        self.commandes_francais = sorted(self.commandes, \
            key=lambda noeud: noeud.commande.nom_francais)
        self.commandes_anglais = sorted(self.commandes, \
            key=lambda noeud: noeud.commande.nom_anglais)
    
    def ajouter_masque(self, masque):
        """Méthode d'ajout d'un masque"""
        self.masques[masque.nom] = masque
    
    def get_masque(self, nom_masque):
        """Retourne le masque portant le nom correspondant
        On retourne une nouvelle instance du masque.
        
        """
        print("On crée le masque", nom_masque)
        return self.masques[nom_masque]()
    
    def valider(self, personnage, dic_masques, lst_commande):
        """Commande de validation"""
        trouve = False
        commandes = []
        if personnage.langue_cmd == "francais":
            commandes = self.commandes_francais
        elif personnage.langue_cmd == "anglais":
            commandes = self.commandes_anglais
        
        for cmd in commandes:
            if cmd.valider(personnage, dic_masques, lst_commande):
                trouve = True
                break
        
        if not trouve:
            raise ErreurValidation("|err|Commande inconnue.|ff|")
    
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
