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


"""Package contenant la commande 'canaux'.

"""

import textwrap

from primaires.interpreteur.commande.commande import Commande
from primaires.format.constantes import *
from .lister import PrmLister
from .infos import PrmInfos
from .rejoindre import PrmRejoindre
from .quitter import PrmQuitter
from .immerger import PrmImmerger
from .inviter import PrmInviter
from .ejecter import PrmEjecter
from .bannir import PrmBannir
from .annoncer import PrmAnnoncer
from .promouvoir import PrmPromouvoir
from .editer import PrmEditer
from .dissoudre import PrmDissoudre

class CmdCanaux(Commande):
    
    """Commande 'canaux'.
    
    """
    
    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "canaux", "channels")
        self.groupe = "joueur"
        self.nom_categorie = "parler"
        self.aide_courte = "gestion des canaux de communication"
        self.aide_longue = \
                "Cette commande permet de gérer les canaux de communication " \
                "de l'univers. Diverses options sont disponibles : entrez " \
                "%canaux% sans arguments pour en voir un aperçu, ou lisez " \
                "l'aide plus bas."
    
    def ajouter_parametres(self):
        """Ajout des paramètres"""
        prm_lister = PrmLister()
        prm_infos = PrmInfos()
        prm_rejoindre = PrmRejoindre()
        prm_quitter = PrmQuitter()
        prm_immerger = PrmImmerger()
        prm_inviter = PrmInviter()
        prm_ejecter = PrmEjecter()
        prm_bannir = PrmBannir()
        prm_annoncer = PrmAnnoncer()
        prm_promouvoir = PrmPromouvoir()
        prm_editer = PrmEditer()
        prm_dissoudre = PrmDissoudre()
        
        self.ajouter_parametre(prm_lister)
        self.ajouter_parametre(prm_infos)
        self.ajouter_parametre(prm_rejoindre)
        self.ajouter_parametre(prm_quitter)
        self.ajouter_parametre(prm_immerger)
        self.ajouter_parametre(prm_inviter)
        self.ajouter_parametre(prm_ejecter)
        self.ajouter_parametre(prm_bannir)
        self.ajouter_parametre(prm_annoncer)
        self.ajouter_parametre(prm_promouvoir)
        self.ajouter_parametre(prm_editer)
        self.ajouter_parametre(prm_dissoudre)
    
    def aide_longue_pour(self, personnage):
        """Retourne l'aide longue de la commande.
        Elle se compose :
        -   du nom de la commande
        -   de sa catégorie
        -   de son synopsis (aide courte)
        -   de son aide longue
        -   des aides courtes et longues de ses sous-commandes
    
        """
        # On constitue notre chaîne d'aide
        aide = "Commande |ent|"
        aide += self.afficher(personnage)
        aide += "|ff|\n\n"
        aide += "Catégorie : " + self.categorie.nom.lower() + "\n\n"
        synop = "Synopsis : "
        aide += synop
        synopsis = self.remplacer_mots_cles(personnage, self.aide_courte)
        synopsis = textwrap.wrap(synopsis, 
                longueur_ligne - len(synop))
        aide += ("\n" + " " * len(synop)).join(synopsis)
        
        aide += "\n\n"
        
        aide_longue = self.remplacer_mots_cles(personnage, self.aide_longue)
        aide += textwrap.fill(aide_longue, longueur_ligne)
        
        # On récupère le statut de personnage
        statut_perso = type(self).importeur.communication.canaux.get_statut(
                personnage)
        
        # On récupère les paramètres
        parametres = [noeud.commande for noeud in self.parametres.values()]
        dic_parametres = {}
        taille = 0
        for parametre in parametres:
            dic_parametres[parametre.nom_anglais] = parametre
            if len(parametre.get_nom_pour(personnage)) > taille:
                taille = len(parametre.get_nom_pour(personnage))
        
        aligner = longueur_ligne - taille - 5
        aide += "\n\n"
        aide += "Sous-commandes disponibles :"
        
        # Fonction d'affichage
        def afficher_param(parametre):
            nom = parametre.get_nom_pour(personnage)
            aide_courte = self.remplacer_mots_cles(personnage,
                    parametre.aide_courte)
            aide_longue = self.remplacer_mots_cles(personnage,
                    parametre.aide_longue)
            aide_longue = textwrap.wrap(aide_longue, aligner)
            ret = "\n  |ent|" + nom.ljust(taille) + "|ff| - " + aide_courte
            ret += "\n" + "     " + taille * " "
            ret += ("\n" + (taille + 5) * " ").join(aide_longue)
            return ret
        
        # Affichage
        aide += "\n\n  Paramètres de base :"
        aide += afficher_param(dic_parametres["list"])
        aide += afficher_param(dic_parametres["infos"])
        aide += afficher_param(dic_parametres["join"])
        aide += afficher_param(dic_parametres["immerge"])
        aide += afficher_param(dic_parametres["quit"])
        aide += afficher_param(dic_parametres["invite"])
        if statut_perso in ("modo", "admin") or personnage.est_immortel():
            aide += "\n\n  Paramètres de modération :"
            aide += afficher_param(dic_parametres["eject"])
            aide += afficher_param(dic_parametres["ban"])
            aide += afficher_param(dic_parametres["announce"])
        if statut_perso == "admin" or personnage.est_immortel():
            aide += "\n\n  Paramètres d'administration :"
            aide += afficher_param(dic_parametres["promote"])
            aide += afficher_param(dic_parametres["edit"])
            aide += afficher_param(dic_parametres["dissolve"])
        
        aide += \
            "\n\nNote : une fois connecte, entrez |cmd|<canal> <message>|ff| " \
            "pour utiliser un canal (par\nexemple : |ent|hrp Bonjour|ff|). La " \
            "syntaxe |cmd|. <message>|ff| permet de parler dans le\ndernier " \
            "canal que vous avez utilisé. En immersion, il suffit d'envoyer " \
            "ce que\nvous souhaitez dire.\n" \
            "En outre, des alias sont disponibles pour plusieurs commandes. " \
            "Pour rejoindre\nun canal, le quitter ou vous y immerger, les " \
            "raccourcis sont |cmd|+<canal>|ff|, |cmd|-<canal>|ff|\net " \
            "|cmd|:<canal>|ff|."

        return aide
    
    def erreur_validation(self, personnage, dic_masques):
        """Définit la réaction de la commande lors d'une erreur"""        
        aide = "|ent|" + self.get_nom_pour(personnage) + "|ff| : "
        synopsis = self.remplacer_mots_cles(personnage, self.aide_courte)
        aide += synopsis
        
        # On récupère le statut de personnage
        statut_perso = type(self).importeur.communication.canaux.get_statut(
                personnage)
        
        # On récupère les paramètres
        parametres = [noeud.commande for noeud in self.parametres.values()]
        dic_parametres = {}
        taille = 0
        for parametre in parametres:
            dic_parametres[parametre.nom_anglais] = parametre
            if len(parametre.get_nom_pour(personnage)) > taille:
                taille = len(parametre.get_nom_pour(personnage))
        
        # Fonction d'affichage d'un paramètre
        def afficher_param(parametre):
            nom = parametre.get_nom_pour(personnage)
            aide_courte = self.remplacer_mots_cles(personnage, 
                parametre.aide_courte)
            return "\n  |ent|" + nom.ljust(taille) + "|ff| - " + aide_courte
        
        # Affichage
        aide += "\n\n  Paramètres de base :"
        aide += afficher_param(dic_parametres["list"])
        aide += afficher_param(dic_parametres["infos"])
        aide += afficher_param(dic_parametres["join"])
        aide += afficher_param(dic_parametres["immerge"])
        aide += afficher_param(dic_parametres["quit"])
        aide += afficher_param(dic_parametres["invite"])
        if statut_perso in ("modo", "admin") or personnage.est_immortel():
            aide += "\n\n  Paramètres de modération :"
            aide += afficher_param(dic_parametres["eject"])
            aide += afficher_param(dic_parametres["ban"])
            aide += afficher_param(dic_parametres["announce"])
        if statut_perso == "admin" or personnage.est_immortel():
            aide += "\n\n  Paramètres d'administration :"
            aide += afficher_param(dic_parametres["promote"])
            aide += afficher_param(dic_parametres["edit"])
            aide += afficher_param(dic_parametres["dissolve"])
        
        aide = self.remplacer_mots_cles(personnage, aide)
        return aide
