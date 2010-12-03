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

from primaires.interpreteur.masque.noeuds.fonctions import *
from primaires.interpreteur.masque.fonctions import *

NB_MAX_CAR_AIDE_COURTE = 40

class Commande:
    
    """Classe-mère de toutes les commandes.
    Elle contient :
    -   un nom, en français et en anglais
    -   une méthode qui sera exécutée si un joueur l'appelle
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
        self.nom_francais = francais
        self.nom_anglais = anglais
        
        self.racine = None
        self.tronquer = True
        self.parametres = []
        self.delimiteurs = []
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
    
    def ajouter_parametre(self, parametre):
        """Ajoute un paramètre à la commande"""
        self.parametres.append(parametre)
    
    def ajouter_delimiteur(self, delimiteur):
        """Ajoute un délimiteur à la commande"""
        self.delimiteurs.append(delimiteur)
    
    def get_delimiteur(self, nom_delimiteur):
        """Retourne le délimiteur ou le paramètre correspondant"""
        res = None
        for delimiteur in list(self.parametres + self.delimiteurs):
            if delimiteur.nom == nom_delimiteur:
                res = delimiteur
                break
        
        if not res:
            raise ValueError("le délimiteur {0} n'a pas été trouvé dans la " \
                "commande {1}".format(nom_delimiteur, self))
        
        return res

    def construire_arborescence(self, schema):
        """Interprétation du schéma"""
        schema = chaine_vers_liste(schema)
        return creer_noeud(self, schema)
    
    def _get_noms_commandes(self):
        """Retourne les différents noms possibles des commandes.
        
        """
        return (self.nom_francais, self.nom_anglais)
    
    noms_commandes = property(_get_noms_commandes)
