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


"""Ce fichier définit la classe BaseObj définie plus bas."""

class BaseObj:
    """Cette classe définit la base d'un objet destiné à être enregistré,
    directement ou indirectement dans un fichier.
    
    Rappelons que :
    *   Les objets destinés à être DIRECTEMENT enregistré dans des fichiers
        doivent être hérités de 'ObjetID' (voir abstraits/id/__init__.py)
        La clases ObjetID hérite elle-même de BaseObj.
    *   Les objets destinés à être INDIRECTEMENT enregistré dans des fichiers
        doivent être hérités de BaseObj.
        Ces objets sont ceux destinés à être enregistrés dans des fichiers
        sous la forme d'attributs d'autres objets par exemple.
    
    On se base sur un dictionnaire représentant les attributs, lui-même étant
    un attribut de classe :
    -   les clés sont constitués des noms des attributs
    -   les valeurs sont les valeurs par défaut des attributs correspondant
    
    Exemple d'utilisation :
    >>> from abstraits.obase import BaseObj
    >>> dic_attributs = {
    ...     "nom": "inconnu",
    ...     "race": RACE_INCONNU,
    ...     "talents": [],
    ... }
    >>> class Joueur(BaseObj):
    ...     attributs = dic_attributs
    
    Ce dictionnaire est utilisé :
    *   A la création du personnage : on va tout simplement copier
        chaque attribut et valeur par défaut dans l'objet à créer
    *   A la récupération de l'objet (méthode '__setstate__') :
        On écrit dans ce cas les valeurs par défaut des attributs
        sans écraser ceux déjà présents dans l'objet
        Ainsi, on peut rajouter des attributs dans des objets d'une session du
        module à l'autre.
    
    """
    attributs = {} # dictionnaire des attributs
    def __init__(self):
        """Constructeur. On copie tous les attributs dans self"""
        self.__dict__.update(type(self).attributs)
    
    def __setstate__(self, dico_attrs):
        """Méthode appelée lors de la dé-sérialisation de l'objet"""
        dico_attrs.update(type(self).attributs)
        self.__dict__.update(dico_attrs)
