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
    *   on cherche la classe d'origine de l'objet dans sys.modules
    *   on appelle son constructeur en lui passant 'self'
    *   on met à jour cet objet créé grâce au dictionnaire des attributs
        sauvegardé
    
    """
    
    # Dictionnaires à NE PAS redéfinir dans les sous-classes :
    trace_p_ids = {}
    
    def __init__(self):
        """Constructeur. On copie tous les attributs dans self"""
        self.p_id = id(self)
    
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
        # Si l'objet est déjà tracé dans trace_p_ids, on réc upère son __dict__
        # Sinon, on ajoute son __dict__ dans trace_p_ids
        # Note importante: à chaque fois qu'un objet est sauvegardé, il
        # enregistre le timestamp de cette sauvegarde.
        # Si on trouve une référence vers le même objet mais dont le timestamp
        # de son enregistrement est supérieur à celui enregistré dans
        # trace_p_ids, c'est le plus récent qui est conservé.
        # Pour résumer, on considère que c'est le dernier objet enregistré le
        # plus à jour.
        if self.p_id in type(self).trace_p_ids.keys():
            if self._ts > type(self).trace_p_ids[self.p_id]._ts:
                # self est plus récent que celui de trace_p_ids
                type(self).trace_p_ids[self.p_id].__dict__.update( \
                        self.__dict__)
            self.__dict__ = type(self).trace_p_ids[self.p_id].__dict__
        else:
            type(self).trace_p_ids[self.p_id] = self
            self.p_id = id(self)
