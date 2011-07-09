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


"""Ce fichier contient la classe Attitudes détaillée plus bas."""


from abstraits.obase import BaseObj
from .attitude import Attitude

class Attitudes(BaseObj):

    """Classe conteneur des attitudes sociales.
    Cette classe liste tous les items Attitude utilisables dans l'univers
    à un instant donné.
    
    Voir : ./attitude.py
    
    """
    
    def __init__(self, parent=None):
        """Constructeur du conteneur"""
        BaseObj.__init__(self)
        self._attitudes = []
    
    def __getnewargs__(self):
        return ()
    
    def __contains__(self, cle):
        """Renvoie True si l'attitude existe, False sinon"""
        return self.get_attitude(cle) != -1
    
    def iter(self):
        """Boucle sur les attitudes contenues"""
        return list(self._attitudes)
    
    def ajouter(self, cle):
        """Ajoute une attitude à la liste"""
        attitude = Attitude(cle)
        self._attitudes.append(attitude)
        return attitude
    
    def get_attitude(self, cle):
        """Renvoie une attitude à partir de sa clé"""
        for attitude in self._attitudes:
            if attitude.cle == cle:
                return attitude        
        return -1
    
    def jouer(self, acteur, arguments):
        """Fait jouer une attitude à acteur"""
        cle = arguments.split(" ")[0]
        attitude = self.get_attitude(cle)
        attitude.jouer(acteur, arguments)
