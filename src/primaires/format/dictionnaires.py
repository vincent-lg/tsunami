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


"""Ce fichier définit plusieurs classes envelopes de dictionnaires.

Notez qu'aucune d'elle n'est destinée à être enregistrée, directement
ou indirectement, en fichier. Ce sont des classes ayant n usage temporaire.

"""

from primaires.format.fonctions import supprimer_accents

class DictSansAccent:
    
    """Dictionnaire sans accent.
    
    Les clés sont des chaînes de caractères.
    Les valeurs peuvent être n'importe quoi.
    
    Les clés sans accents sont stockées à part et on sy' réfère pour lire
    ou écrire dans ce dictionnaire.
    
    Cela signifie que si vous faites :
    >>> d = DictSansAccent()
    >>> d["forêt"] = 58
    >>> d["foret"]
    58
    >>>
    
    """
    
    def __init__(self, iterable_ou_mapping, **kwargs):
        """Constructeur du dictionnaire.
        
        A l'instar d'un dictionnaire, il peut prendre en paramètre :
            un itérateur
            une table comme un autre dictionnaire
        
        D'autres clés / valeurs peuvent être spécifiés grâce aux arguments
        nommés.
        
        """
        self.__dict = dict(iterable_ou_mapping, **kwargs)
        self.__cles_sans_accent = dict((supprimer_accents(cle), cle) for \
                cle in self.__dict.keys())
    
    def keys(self):
        """Retourne les clés avec accents."""
        return self.__cles_sans_accent.values()
    
    def cles_sa(self):
        """Retourne les clés sans accent."""
        return self.__cles_sans_accent.keys()
    
    def values(self):
        """Retourne les valeurs du dictionnaire."""
        return self.__dict.values()
    
    def items(self):
        """Retourne les couples clés / valeurs."""
        return self.__dict.items()
    
    def __contains__(self, cle):
        """Retourne True si contient la clé."""
        cle = supprimer_accents(cle)
        return cle in self.__cles_sans_accent.keys()
    
    def __getitem__(self, cle):
        """Retourne la valeur si la clé existe."""
        cle = supprimer_accents(cle)
        if cle in self.__cles_sans_accent:
            return self.__dict[self.__cles_sans_accent[cle]]
        else:
            raise KeyError(cle)
    
    def __setitem__(self, cle, valeur):
        """Ecrit la valeur dans la clé."""
        cle_sa = supprimer_accents(cle)
        if cle_sa in self.__cles_sans_accent:
            self.__dict[self.__cles_sans_accent[cle_sa]] = valeur
            self.__cles_sans_accent[cle_sa] = cle
        else:
           self.__dict[cle] = valeur
           self.__cles_sans_accent[cle_sa] = cle
       
    def __str__(self):
        return str(self.__dict)
    
    def __repr__(self):
        return repr(self.__dict)
