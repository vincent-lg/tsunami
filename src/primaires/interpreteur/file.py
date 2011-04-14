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


"""Fichier définissant les files d'attente des contextes :
-   La classe Filecontexte modélisant une file d'attente des contextes
-   L'exception fileVide

"""

from abstraits.obase import BaseObj

class FileContexte(BaseObj):
    """Cette classe définie une file d'attente des contextes.
    C'est une classe enveloppe de liste. On interragit avec cette
    classe qu'avec plusieurs méthodes :
        ajouter(self, objet) -- ajoute l'objet en tête de file
        retirer(self)        -- retire l'objet en tête de file et le retourne
    
    Cette file peut être parcourue et les différents items qu'elle contient
    sont indexées (file[0] retourne le premier élément).
    
    """
    
    def __init__(self, parent=None):
        """Constructeur de la file, initialement vide."""
        BaseObj.__init__(self)
        self._file = [] # la liste représentant la file d'attente
        self._taille_min = 1 # la taille minimum de la file d'attente
        self.parent = parent
   
    def __getinitargs__(self):
        """Méthode retournant les arguments à passer au constructeur"""
        return ()
    
    def __getitem__(self, index):
        """Retourne l'objet se trouvant à l'index 'index'"""
        return self._file.__getitem__(index)
    
    def __setitem__(self, index, contexte):
        """Change le contexte se trouvant à l'index 'index'"""
        self._file.__setitem__(index, contexte)
        if self.parent:
            self.parent.enregistrer()
    
    def __len__(self):
        """Retourne la taille de la file"""
        return len(self._file)
    
    def __iter__(self):
        """Retourne l'itérateur de la file"""
        return iter(self._file)
    
    def __str__(self):
        """Retourne la file"""
        return "f" + str(self._file)
    
    def ajouter(self, objet):
        """Ajoute l'objet à ajouter en tête de la file."""
        self._file.insert(0, objet)
        if self.parent:
            self.parent.enregistrer()
    
    def retirer(self):
        """Retire l'objet en tête de file et le retourne.
        Si la taille de la liste est trop faible (self._taille_min), une
        exception est levée.
        
        """
        if len(self._file) <= self._taille_min:
            raise FileVide
        
        objet = self._file[0]
        del self._file[0]
        if self.parent:
            self.parent.enregistrer()
        return objet
    
    def vider(self):
        """Vide la file des contextes"""
        self._file[:] = []

class FileVide(RuntimeError):
    """Exception appelée quand la file est vide ou d'une taille insuffisante.
    
    """
    def __str__(self):
        """Retourne l'exception de façon plus compréhensible"""
        return "la file d'attente est vide ou d'une taille trop faible"
