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


"""Fichier contenant la class DicMax détaillée plus bas."""

class DicMax(dict):
    
    """Cette classe permet de créer un dictionnaire un peu particulier,
    possédant en clé des entiers (ou flottants) et n'acceptant qu'un nombre
    maximum de clés. Quand le nombre maximum de clés est atteint, ajouter une
    nouvelle clé supprime la clé la moins forte de la liste.
    
    Exemple : on crée un dictionnaire max (DicMax) de taille_max = 3.
    >>> dic_max = DicMax(3)
    >>> # on insère trois clés & valeurs dans ce dictionnaire
    ... dic_max[5] = "valeur 1"
    >>> dic_max[31] = "valeur 2"
    >>> dic_max[2] = "valeur 3"
    >>> # on cherche maintenant à insérer une nouvelle clé
    ... # le nombre maximum de clés est atteint
    ... # si on insère une nouvelle clé, la clé la moins forte est supprimée
    ... dic_max[22] = "valeur 4"
    >>> # après cette instruction, la clé la moins forte (2 => 'valeur 3') a
    ... # été supprimée du dictionnaire.
    
    Note : si on cherche à ajouter une clé moins forte que les autres, elle ne
    sera pas ajoutée (voir __setitem__ pour plus d'informations).
    
    """
    
    def __init__(self, taille_max):
        """Construction du dictionnaire"""
        self.taille_max = taille_max
    
    def __setitem__(self, cle, valeur):
        """Ajout de clé dans le dictionnaire"""
        if hasattr(self, "taille_max"):
            taille_max = self.taille_max
        else:
            taille_max = -1
        dict.__setitem__(self, cle, valeur)
        while len(self) > taille_max and taille_max >= 0:
            # on cherche la clé la plus faible
            petite_cle = min(tuple(self.keys()))
            del self[petite_cle]
