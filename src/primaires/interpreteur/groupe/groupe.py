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


"""Ce fichier définit les groupes de personnages.
Un groupe est un objet donnant plusieurs informations sur les
utilisateurs et permettant de différencier les joueurs des administrateurs
par exemple.
Les administrateurs auront plusieurs flags actifs que les joueurs n'auront
pas, et auront accès à des commandes auxquelles les joueurs ne peuvent
accéder.

Ce système permet à chaque créateur de MUD de faire sa propre hiérarchie
d'utilisateurs (un niveau pour les NPCs, un niveau pour les joueurs, un niveau
pour les modérateurs, plusieurs niveaux d'immortels...).

"""

from abstraits.obase import BaseObj

class Groupe(BaseObj):
    
    """Classe définissant un groupe.
    
    """
    
    def __init__(self, nom):
        """Constructeur d'un groupe"""
        BaseObj.__init__(self)
        self.nom = nom
        self.flags = []
        self.groupes_inclus = []
    
    def __getinitargs__(self):
        """Retourne les arguments à passer au constructeur"""
        return ("", )
    
    def ajouter_groupe_inclus(self, groupe):
        """Ajoute 'groupe' dans les groupes inclus.
        Si le groupe A inclus le groupe B, alors les joueurs du groupe A
        pourront utiliser les commandes du groupe B.
        
        """
        if groupe not in self.groupes_inclus:
            self.groupes_inclus.append(groupe)
    
    def supprimer_groupe_inclus(self, groupe):
        """Supprime 'groupe' des groupes inclus"""
        if groupe in self.groupes_inclus:
            self.groupes_inclus.remove(groupe)
