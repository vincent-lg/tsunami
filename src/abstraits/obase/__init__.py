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

import sys
import time


INIT, CONSTRUIT = 0, 1

class BaseObj:
    
    """Cette classe définit la base d'un objet destiné à être enregistré,
    directement ou indirectement dans un fichier.
    
    Rappelons que :
    *   Les objets destinés à être DIRECTEMENT enregistrés dans des fichiers
        doivent être hérités de 'ObjetID' (voir abstraits/id/__init__.py)
        La classe ObjetID hérite elle-même de BaseObj.
    *   Les objets destinés à être INDIRECTEMENT enregistrés dans des fichiers
        doivent être hérités de BaseObj.
        Ces objets sont ceux destinés à être enregistrés dans des fichiers
        sous la forme d'attributs d'autres objets par exemple.
    
    La récupération d'objets hérités de 'BaseObj' se fait assez simplement :
    *   on récupère la classe de l'objet (objet.__class__)
    *   on appelle son constructeur en lui passant 'self'
    *   on met à jour cet objet créé grâce au dictionnaire des attributs
        sauvegardé
    
    Cela signifie que vous pouvez ajouter, d'une session à l'autre, de
    nouveaux attributs dans vos objets. A leur récupération, les objets seront
    recréé et auront bien les valeurs par défaut des nouveaux attributs.
    
    """
    
    importeur = None
    
    def __init__(self):
        """Instancie un simple statut"""
        self._status = INIT
    
    @property
    def construit(self):
        return hasattr(self, "_statut") and self._statut is CONSTRUIT
    
    def __getstate__(self):
        """Au moment de l'enregistrement, on met à jour le timestamp"""
        self._ts = time.time()
        return self.__dict__
    
    def __setstate__(self, dico_attrs):
        """Méthode appelée lors de la désérialisation de l'objet"""
        # On recherche la classe
        classe = type(self)
        # A passer au constructeur
        args = classe.__getinitargs__(self)
        classe.__init__(self, *args)
        self.__dict__.update(dico_attrs)
    
    def __getattribute__(self, nom_attr):
        """Méthode appelé quand on cherche à récupérer l'attribut nom_attr
        Si l'attribut qu'on cherche à récupérer est un type ID, on retourne
        l'objet correspondant à l'ID.
        Pour ce faire, on demande à parid l'objet correspondant à notre ID.
        
        """
        objet = object.__getattribute__(self, nom_attr)
        if nom_attr != "id" and est_id(objet):
            # On cherche l'objet correspondant à cet ID
            objet = objet.get_objet()
        
        return objet
    
    def __setattr__(self, nom_attr, val_attr):
        """Méthode appelée quand on cherche à écrire l'objet val_attr dans
        l'attribut nom_attr.
        
        Si val_attr est un ObjetID (il possède l'attribut id), on écrit
        dans l'attribut nom_attr non pas val_attr mais l'ID de val_attr.
        
        """
        if nom_attr != "id" and hasattr(val_attr, "id"):
            # val_attr est un ObjetID
            val_attr = val_attr.id
        
        object.__setattr__(self, nom_attr, val_attr)

def est_id(objet):
    """Retourne True si objet est un ID"""
    return hasattr(type(objet), "_objetid_")
