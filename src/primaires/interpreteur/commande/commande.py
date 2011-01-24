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


"""Fichier contenant la classe Commande, détaillée plus bas."""

import textwrap

from primaires.interpreteur.masque.noeuds.noeud_commande import NoeudCommande
from primaires.interpreteur.masque.noeuds.fonctions import *
from primaires.interpreteur.masque.fonctions import *
from primaires.interpreteur.masque.masque import Masque
from primaires.format.constantes import *
from primaires.format.fonctions import *

# Constantes
NB_MAX_CAR_AIDE_COURTE = 40
SEP = ":"

class Commande(Masque):
    
    """Classe-mère de toutes les commandes.
    Elle contient :
    -   un nom, en français et en anglais
    -   un flag pour savoir si l'on peut tronquer la commande
    -   une arborescence de noeuds symbolisant les possibilités au départ
        de la commande
    -   une aide courte (40 caractères max)
    -   une aide plus longue expliquant le moyen de former la commande
    
    Note: si des paramètres sont contenus dans l'arborescence des noeuds,
    chacun est une commande qui possède sa sous-arborescence, son aide courte
    et longue.
    
    """
    
    def __init__(self, francais, anglais):
        """Constructeur de la commande"""
        Masque.__init__(self, francais)
        self.nom_francais = francais
        self.nom_anglais = anglais
        self.adresse = francais
        
        self.racine = None
        self.noeud = None # le noeud commande lié
        self.schema = ""
        self.tronquer = True
        self.parametres = {}
        self.aide_courte = ""
        self.aide_longue = ""
        
        # Groupe
        self.groupe = "npc"
    
    def _get_aide_courte(self):
        """Retourne l'aide courte"""
        return self._aide_courte
    
    def _set_aide_courte(self, aide):
        """Change l'aide courte"""
        if len(aide) > NB_MAX_CAR_AIDE_COURTE:
            raise ValueError("la chaîne d'aide entrée pour cette commande " \
                    "est trop longue")
        
        self._aide_courte = aide
    
    aide_courte = property(_get_aide_courte, _set_aide_courte)
    
    def __str__(self):
        """Fonction d'affichage"""
        res = "(" + self.nom_francais + "/" + self.nom_anglais + ")"
        return res
    
    def get_nom_pour(self, personnage):
        """Retourne le nom de la commande en fonction de la langue du
        personnage
        
        """
        if personnage.langue_cmd == "francais":
            nom = self.nom_francais
        elif personnage.langue_cmd == "anglais":
            nom = self.nom_anglais
        
        return nom
    
    def ajouter_parametre(self, parametre):
        """Ajoute un paramètre à la commande"""
        noeud_cmd = NoeudCommande(parametre)
        self.parametres[parametre.nom] = noeud_cmd
        parametre.adresse = self.adresse + SEP + parametre.nom_francais
        if not parametre.groupe:
            parametre.groupe = self.groupe
        
        type(self).importeur.interpreteur.groupes.ajouter_commande(parametre)
    
    def construire_arborescence(self, schema):
        """Interprétation du schéma"""
        schema = chaine_vers_liste(schema)
        return creer_noeud(self, schema)
    
    def _get_noms_commandes(self):
        """Retourne les différents noms possibles des commandes.
        
        """
        return (self.nom_francais, self.nom_anglais)
    
    noms_commandes = property(_get_noms_commandes)
    
    def valider(self, personnage, dic_masques, commande):
        """Fonctiond de validation.
        Elle retourne True si la commande entrée par le joueur correspond à
        son nom, False sinon.
        
        """
        # Si le personnage n'a pas le droit d'appeler la commande, on s'arrête
        if not type(self).importeur.interpreteur.groupes.personnage_a_le_droit(
                personnage, self):
            return False
        
        str_commande = liste_vers_chaine(commande)
        str_commande = supprimer_accents(str_commande).lower()
        
        # On fait la césure au premier espace
        fin_pos = str_commande.find(" ")
        if fin_pos == -1:
            fin_pos = len(str_commande)
        
        str_commande = str_commande[:fin_pos]
        if personnage.langue_cmd == "francais":
            nom_com = self.nom_francais
        elif personnage.langue_cmd == "anglais":
            nom_com = self.nom_anglais
        else:
            raise ValueError("la langue {0} est inconnue".format( \
                    personnage.langue_cmd))
        
        if self.tronquer and nom_com.startswith(str_commande):
            commande[:] = commande[fin_pos:]
            valide = True
        elif nom_com == str_commande:
            commande[:] = commande[fin_pos:]
            valide = True
        else:
            valide = False
        
        return valide
    
    def interpreter(self, personnage, dic_masques):
        """Fonction d'interprétation.
        
        """
        personnage.envoyer(
            self.erreur_validation(personnage, dic_masques))
    
    def est_parametre(self):
        """La commande est une forme de paramètre"""
        return True
    
    def afficher(self, personnage):
        """Retourne un affichage de la commande pour le personnage passé en
        paramètre
        
        """
        return self.noeud.afficher(personnage)
    
    def remplacer_mots_cles(self, personnage, aide):
        """Sert à remplacer les mots clés d'un fichier d'aide.
        Dans un fichier d'aide, on trouve du texte standard et certains mots
        entourés du symbole %.
        Ces mots sont des noms de commande, des chemins menant éventuellement
        à des paramètres.
        
        Voici un exemple de texte d'aide :
        '''Ceci est l'aide de la commande %qui%.'''
        
        Le texte précédent doit être conservé tel quel. En revanche, %qui%
        doit être remplacé par le nom de la commande (en français si
        le personnage a choisi le français, en anglais si le personnage a
        choisi l'anglais).
        
        """
        # On commence par découper la chaîne en fonction du symbole %
        decoupe = aide.split("%")
        
        # On sait que dans la liste obtenue, tous nos codes commande se
        # trouvent en chaque index impair
        for i, mot in enumerate(decoupe):
            if i % 2 == 1: # index impair
                decoupe[i] = "|ent|" + \
                    type(self).importeur.interpreteur.trouver_commande( \
                    mot).get_nom_pour(personnage) + "|ff|"
        
        return "".join(decoupe)
    
    def aide_longue_pour(self, personnage):
        """Retourne l'aide longue de la commande.
        Elle se compose :
        -   du nom de la commande
        -   de son masque (optionnel)
        -   de son synopsis (aide courte)
        -   de son aide longue
        -   des aides courtes et longues de ses sous-commandes
    
        """
        # On constitue notre chaîne d'aide
        aide = "Commande |ent|"
        aide += self.afficher(personnage)
        aide += "|ff|\n\n"
        synop = "Synopsis : "
        aide += synop
        synopsis = self.remplacer_mots_cles(personnage, self.aide_courte)
        synopsis = textwrap.wrap(synopsis, 
                longueur_ligne - len(synop))
        aide += ("\n" + " " * len(synop)).join(synopsis)
        
        aide += "\n\n"
        
        aide_longue = self.remplacer_mots_cles(personnage, self.aide_longue)
        aide += textwrap.fill(aide_longue, longueur_ligne)
        
        # Paramètres
        parametres = [noeud.commande for noeud in self.parametres.values()]
        # Tri en fonction de la langue
        parametres = sorted(parametres,
                key=lambda parametre: parametre.get_nom_pour(personnage))
        
        # On calcule la taille max du nom des paramètres
        taille = 0
        for parametre in parametres:
            nom = parametre.get_nom_pour(personnage)
            if len(nom) > taille:
                taille = len(nom)
        
        if len(parametres) > 0:
            aligner = longueur_ligne - taille - 5
            aide += "\n\n"
            aide += "Sous-commandes disponibles :"
            for parametre in parametres:
                if type(self).importeur.interpreteur.groupes. \
                        personnage_a_le_droit(personnage, parametre):
                    nom = parametre.get_nom_pour(personnage)
                    aide += "\n  |ent|" + nom.ljust(taille) + "|ff|"
                    aide += " - "
                    aide_courte = self.remplacer_mots_cles(personnage, 
                            parametre.aide_courte)
                    aide_courte = textwrap.wrap(aide_courte, aligner)
                    aide += ("\n" + (taille + 5) * " ").join(aide_courte)
                    aide += "\n" + "     " + taille * " "
                    aide_longue = self.remplacer_mots_cles(personnage,
                            parametre.aide_longue)
                    aide_longue = textwrap.wrap(aide_longue, aligner)
                    aide += ("\n" + (taille + 5) * " ").join(aide_longue)

        return aide
    
    def erreur_validation(self, personnage, dic_masques):
        """Que faire lors d'une erreur de validation ?
        Par défaut, on affiche l'aide courte de la commande.
        
        """
        premier_masque = list(dic_masques.keys())[0]
        dernier_masque = list(dic_masques.keys())[-1]
        syntaxe = self.afficher(personnage)
        
        aide = "|ent|" + syntaxe + "|ff| : "
        synopsis = self.remplacer_mots_cles(personnage, self.aide_courte)
        synopsis = textwrap.wrap(synopsis, longueur_ligne - len(syntaxe) - 2)
        aide += ("\n" + " " * (longueur_ligne - len(syntaxe) - 2)).join(
                synopsis)
        
        # Paramètres
        parametres = [noeud.commande for noeud in self.parametres.values()]
        # Tri en fonction de la langue
        parametres = sorted(parametres,
                key=lambda parametre: parametre.get_nom_pour(personnage))
        
        # On calcule la taille max du nom des paramètres
        taille = 0
        for parametre in parametres:
            nom = parametre.get_nom_pour(personnage)
            if len(nom) > taille:
                taille = len(nom)
        
        if len(parametres) > 0:
            aligner = longueur_ligne - taille - 5
            aide += "\n"
            for parametre in parametres:
                if type(self).importeur.interpreteur.groupes. \
                        personnage_a_le_droit(personnage, parametre):
                    nom = parametre.get_nom_pour(personnage)
                    aide += "\n  |ent|" + nom.ljust(taille) + "|ff|"
                    aide += " - "
                    aide_courte = self.remplacer_mots_cles(personnage, 
                            parametre.aide_courte)
                    aide_courte = textwrap.wrap(aide_courte, aligner)
                    aide += ("\n" + (taille + 5) * " ").join(aide_courte)
        
        aide = self.remplacer_mots_cles(personnage, aide)
        return aide
