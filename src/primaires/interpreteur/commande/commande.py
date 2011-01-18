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

from primaires.interpreteur.masque.noeuds.noeud_commande import NoeudCommande
from primaires.interpreteur.masque.noeuds.fonctions import *
from primaires.interpreteur.masque.fonctions import *
from primaires.interpreteur.masque.masque import Masque
from primaires.format.fonctions import *
from primaires.interpreteur.masque.aide import afficher_aide

NB_MAX_CAR_AIDE_COURTE = 40

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
        
        self.racine = None
        self.schema = ""
        self.tronquer = True
        self.parametres = {}
        self.aide_courte = ""
        self.aide_longue = ""
    
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
        """Fonctiond e validation.
        Elle retourne True si la commande entrée par le joueur correspond à
        son nom, False sinon.
        
        """
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
        dernier_masque = list(dic_masques.values())[-1]
        personnage.envoyer(
            afficher_aide(personnage, dernier_masque, self, 1, dic_masques))
    
    def est_parametre(self):
        """La commande est une forme de paramètre"""
        return True
    
    def afficher(self, personnage):
        """Retourne un affichage de la commande pour le personnage passé en
        paramètre
        
        """
        return self.nom_francais
