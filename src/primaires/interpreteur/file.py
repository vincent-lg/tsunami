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
        self._position = 0 # position dans la file
        self.parent = parent
   
    def __getnewargs__(self):
        """Méthode retournant les arguments à passer au constructeur"""
        return ()
    
    def __getitem__(self, index):
        """Retourne l'objet se trouvant à l'index 'index'
        
        index peut également être un type de contexte.
        
        """
        if isinstance(index, int):
            return self._file.__getitem__(index)
        else:
            for contexte in self._file:
                if isinstance(contexte, index):
                    print(contexte)
                    return contexte
            
            raise ValueError("contexte de type inconnu".format(index))
    
    def __setitem__(self, index, contexte):
        """Change le contexte se trouvant à l'index 'index'"""
        self._file.__setitem__(index, contexte)
    
    def __len__(self):
        """Retourne la taille de la file"""
        return len(self._file)
    
    def __iter__(self):
        """Retourne l'itérateur de la file"""
        return iter(self._file)
    
    def __str__(self):
        """Retourne la file"""
        return "f" + str(self._file)
    
    def _get_position(self):
        return self._position
    def _set_position(self, position):
        self._position = position
    position = property(_get_position, _set_position)
    
    def get(self, index):
        """Essaye de récupérer le contexte à l'index indiqué.
        
        Si échoue, retourne None.
        
        Note : index doit être positif.
        
        """
        if index < 0:
            raise IndexError
        
        try:
            contexte = self[index]
        except IndexError:
            contexte = None
        
        return contexte
    
    def get_position(self, contexte):
        """Retourne la position du contexte passé en paramètre.
        
        Si le contexte ne peut être trouvé, retourne la position actuelle.
        
        """
        try:
            return self._file.index(contexte)
        except ValueError:
            return self._position
    
    def ajouter(self, objet):
        """Ajoute l'objet à ajouter en index self._position."""
        self._file.insert(self._position, objet)
    
    def retirer(self, contexte=None):
        """Retire le contexte précisé ou actuel et le retourne.
        
        Si la taille de la liste est trop faible (self._taille_min), une
        exception est levée.
        
        Si le contexte est précisé, retire le contexte précis.
        
        """
        if contexte:
            self._file.remove(contexte)
            self.actualiser_position()
        else:
            if len(self._file) <= self._taille_min:
                raise FileVide
            contexte = self.actuel
            del self._file[self._position]
            self.actualiser_position()
        
        return contexte
    
    def vider(self):
        """Vide la file des contextes"""
        self._file[:] = []
        self.actualiser_position()
    
    @property
    def actuel(self):
        """Retourne le contexte actuel.
        
        On se base sur la position pour savoir quel est le contexte actuel.
        Si le contexte n'est pas trouvé, lève une exception IndexError.
        
        """
        return self[self._position]
    
    def avancer_position(self):
        """Avance la position (déplacement positif).
        
        Si aucun contexte n'est trouvé à la position ciblée, lève une
        exception IndexError.
        
        Retourne le nouveau contexte actuel.
        
        """
        nouveau_contexte = self[self._position + 1]
        self._position += 1
        self.actualiser_position()
        
        return nouveau_contexte
    
    def reculer_position(self):
        """Recule la position (déplacement négatif).
        
        Si aucun contexte n'est trouvé à la position ciblée, lève une
        exception IndexError.
        
        Retourne le nouveau contexte actuel.
        
        """
        if self._position <= 0:
            raise IndexError
        
        nouveau_contexte = self[self._position - 1]
        self._position -= 1
        self.actualiser_position()
        
        return nouveau_contexte
    
    def actualiser_position(self):
        """Actualise la position.
        
        Si la position est supérieure à la liste des contextes,
        la remet à un nouveau raisonnable.
        
        """
        if self._position >= len(self._file):
            self._position = len(self._file) - 1


class FileVide(RuntimeError):
    """Exception appelée quand la file est vide ou d'une taille insuffisante.
    
    """
    def __str__(self):
        """Retourne l'exception de façon plus compréhensible"""
        return "la file d'attente est vide ou d'une taille trop faible"
