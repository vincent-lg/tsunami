# -*-coding:Utf-8 -*

# Copyright (c) 2014 LE GOFF Vincent
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


"""Fichier contenant la fonction combinaison."""



from random import randint, random
from fractions import Fraction

from primaires.scripting.fonction import Fonction

class ClasseFonction(Fonction):

    """Crée une liste comportant une combinaison générée d'après des paramètres précis.

    Cette fonction reçoit en entrée:
    - la taille de la liste
    - la valeur minimale 
    - la valeur maximale
    - 0 ou 1 pour définir avec ou sans doublons
    
    Elle renvoie une liste contenant la combinaison.
    """

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.combinaison, "Fraction", "Fraction", "Fraction", "Fraction")

    @staticmethod
    def combinaison(tailleListe, valMin, valMax, doublon):
        """Retourne une liste contenant une combinaison générée d'après des paramètres précis.

    Cette fonction reçoit en entrée:
    - la taille de la liste
    - la valeur minimale 
    - la valeur maximale
    - 0 ou 1 pour définir avec ou sans doublons
    
    Elle renvoie une liste contenant la combinaison.
    """
        listeRetour = [];
        
        #Tant que la liste n'a pas la taille requise:
        while len(listeRetour) < tailleListe:
            #Calculer une nouvelle valeur
            valeur = Fraction(randint(int(valMin), int(valMax)))
            
            #Si besoin de vérifier les doublons et qu'une occurence de cette valeur existe déjà, on recommence
            if doublon == 1 and listeRetour.count(valeur) != 0:
                continue
            
            #Ajouter la nouvelle valeur
            listeRetour.append(valeur)
        
        return listeRetour
