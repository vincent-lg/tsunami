# -*-coding:Utf-8 -*

# Copyright (c) 2010-2017 DAVY Guillaume
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


"""Package contenant les plateaux.

Chaque sous-package est un plateau.

Il possède un fichier __init__.py dans lequel se trouve la classe Plateau.

Ce fichier définit la classe BasePlateau dont doit être héritée chaque plateau.
Elle est détaillée plus bas.

"""

from abstraits.obase import BaseObj

class BasePlateau(BaseObj):
    
    """Classe définissant un plateau de jeu.
    
    Un plateau est différent du
    jeu lui-même (on peut jouer à plusieurs jeux depuis le même plateau).
    
    """
    
    jeux = [] # liste des noms de jeux liés à ce plateau
    nom = "" # nom de ce plateau
    def __init__(self):
        """Initialisation du plateau."""
        BaseObj.__init__(self)
        self.init()
        self._construire()
    
    def __getnewargs__(self):
        return ()
    
    def afficher(self, personnage, jeu, partie):
        """Affiche la partie en cours au personnage."""
        return ""
