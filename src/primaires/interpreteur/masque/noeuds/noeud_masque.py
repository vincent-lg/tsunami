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


"""Fichier définissant la classe NoeudMasque détaillée plus bas;"""

from primaires.interpreteur.masque.noeuds.base_noeud import BaseNoeud
from primaires.interpreteur.masque.fonctions import *

class NoeudMasque(BaseNoeud):
    
    """Noeud masque, noeud contenant un masque.
    Sa validation dépend de la validation de ses masques.
    De part son statut, si il possède un noeud suivant, deux possibilités :
    -   soit c'est un noeud optionnel et le noeud masque que contient ce
        noeud fils est optionnel
    -   soit c'est un noeud masque également et le masque contenu dans ce fils est obligatoire
    
    """
    
    def __init__(self, commande, lst_schema):
        """Constructeur du noeud masque"""
        BaseNoeud.__init__(self)
        self.nom = ""
        self.masques = []  # une liste vide de masques
        self.defaut = None  # valeur par défaut
        
        ## Phase de construction des masques
        # Schéma est sous la forme d'une liste de caractères, on la convertit
        schema = liste_vers_chaine(lst_schema)
        # Si le schéma débute par un chevron ouvrant, on cherche le fermant
        delimiteurs = [' ', ',']
        if schema.startswith("<"):
            chevrons = True
            schema = schema[1:]
            pos_fin = schema.find(">")
            if pos_fin == -1:
                raise ValueError("le chevron fermant n'a pu être trouvé " \
                        "dans le schéma {0}".format(schema))
        
        else:
            chevrons = False
            pos_fin = len(schema)
            for delimiteur in delimiteurs:
                pos = schema.find(delimiteur)
                if pos >= 0 and pos < pos_fin:
                    pos_fin = pos
        
        # On extrait la chaîne représentant notre masque
        str_masque = schema[:pos_fin]
        
        # On cherche le type du masque
        if ":" in str_masque:
            split_masque = str_masque.split(":")
            nom_masque = split_masque[0]
            str_type_masque = split_masque[1]
        else:
            nom_masque = ""  # on déduira le nom quand on aura le type
            str_type_masque = str_masque
        
        # On extrait la valeur par défaut
        if "=" in str_type_masque:
            split_type_masque = str_type_masque.split("=")
            str_type_masque = split_type_masque[0]
            self.defaut = split_type_masque[1]
        
        # On extrait les autres valeurs possibles du noeud masque
        if "|" in str_type_masque:
            liste_types_masques = str_type_masque.split("|")
        else:
            liste_types_masques = [str_type_masque]
        
        # On cherche le type de masque dans l'interpréteur
        # on remplace dans liste_types_masques chaque str par son instance
        # de masque.
        # Note: si entree est à False, on ne cherche pas dans l'interpréteur
        # mais dans la commande.
        # Si le masque n'existe pas, une exception est levée.
        for i, str_type_masque in enumerate(liste_types_masques):
            if chevrons:
                type_masque = type(self).importeur.interpreteur.get_masque( \
                        str_type_masque)
            else:
                type_masque = commande.get_delimiteur(str_type_masque)

            liste_types_masques[i] = type_masque
        
        # Si le nom du masque n'est pas défini, on le déduit du premier
        # type de masque
        if not nom_masque:
            nom_masque = liste_types_masques[0].nom
        
        self.nom = nom_masque
        
        # On s'assure que la valeur par défaut fournie est une valeur valide
        # pour le premier type de masque proposé
        if self.defaut:
            if not liste_types_masques[0].accepte_valeur(self.defaut):
                raise ValueError("la valeur par défaut {0} n'est pas " \
                        "acceptée par le masque {1}".format( \
                        self.defaut, liste_types_masquse[0]))
        
        self.masques = liste_types_masques
        
        while lst_schema:
            lst_schema.pop(0)
        lst_schema += chaine_vers_liste(schema[pos_fin + 1:])
    
    @property
    def masque(self):
        """Retourne le premier masque"""
        return self.masques[0]
    
    def est_parametre(self):
        """Retourne True si le premier masque est un paramètre"""
        return self.masque.est_parametre()
    
    def __str__(self):
        """Méthode d'affichage"""
        msg = "msg "
        msg += self.nom + "["
        msg += ", ".join([str(masque) for masque in self.masques])
        msg += "]"
        if self.suivant:
            msg += " : " + str(self.suivant)
        
        return msg
    
    def valider(self, personnage, dic_masques, commande, tester_fils=True):
        """Validation d'un noeud masque.
        On va essayer de valider successivement chaque masque possible. Si
        aucun masque ne marche, on s'arrête ici.
        La commande est donnée sous la forme d'une liste de caractères.
        
        """
        valide = False
        if commande:
            for masque in self.masques:
                valide = masque.valider(personnage, dic_masques, commande)
                if valide:
                    dic_masques[self.nom] = masque
                    break
        
        if valide and self.suivant and tester_fils:
            valide = self.suivant.valider(personnage, dic_masques, commande)
        
        return valide
