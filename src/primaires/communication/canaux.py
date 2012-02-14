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


"""Ce fichier contient le conteneur des canaux.
C'est un objet unique.

"""

from abstraits.obase import BaseObj

class Canaux(BaseObj):
    
    """Classe contenant les canaux.
    C'est une classe enveloppe de dictionnaire.
    
    """
    
    enregistrer = True
    def __init__(self):
        """Constructeur du conteneur"""
        BaseObj.__init__(self)
        self._canaux = {}
    
    def __getnewargs__(self):
        return ()
    
    def __contains__(self, nom_canal):
        """Retourne True si le nom de canal est dans le conteneur"""
        return nom_canal in dict(self._canaux)
    
    def __getitem__(self, nom_canal):
        """Retourne le canal si existe dans le conteneur"""
        return self._canaux[nom_canal]
    
    def __setitem__(self, nom_canal, canal):
        """Place 'canal' dans 'nom_canal'"""
        self._canaux[nom_canal] = canal
    
    def __delitem__(self, nom_canal):
        """Supprime le canal"""
        del self._canaux[nom_canal]
    
    def __len__(self):
        """Retourne le nombre de canaux"""
        return len(self._canaux)
    
    def iter(self):
        """Retourne le conteneur sous forme de dictionnaire"""
        return dict(self._canaux)
    
    def get_statut(self, personnage):
        """Retourne le statut de personnage dans les canaux du jeu"""
        statut = "user"
        for canal in self._canaux.values():
            if canal.auteur is personnage:
                statut = "admin"
                break
            if personnage in canal.moderateurs:
                statut = "modo"
                break
        
        return statut
    
    def canaux_connectes(self, personnage):
        """Retourne un tuple contenant les canaux auxquels
        le personnage est connecté.
        
        """
        canaux = []
        for canal in self._canaux.values():
            if personnage in canal.connectes:
                canaux.append(canal)
        
        return tuple(canaux)
