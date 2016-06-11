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


"""Fichier contenant la classe Porte, détaillée plus bas;"""

from abstraits.obase import BaseObj

class Porte(BaseObj):
    
    """Cette classe définit une porte dans une sortie.
    
    Une porte est un objet naturellement commun à deux sorties :
        La sortie d'origine
        La sortie de destination
    
    La sortie de destination est la sortie opposée de la sortie d'origine.
    
    La classe porte définit :
        serrure -- la présence d'une serrure
        ouverte -- le flag d'ouverture de la porte
    Notez que la propriété fermee existe également.
    
    """
    
    groupe = "porte"
    sous_rep = "sorties/portes"
    def __init__(self, clef=None):
        """Constructeur de la porte."""
        BaseObj.__init__(self)
        self.ouverte = False
        self._clef = clef if clef is None else clef.cle
        self.verrouillee = False if clef is None else True
        # On passe le statut en CONSTRUIT
        self._construire()
    
    def __getnewargs__(self):
        return ()
    
    @property
    def fermee(self):
        return not self.ouverte
    
    @property
    def serrure(self):
        return not self.clef is None
    
    def _get_clef(self):
        if self._clef in type(self).importeur.objet.prototypes:
            return type(self).importeur.objet.prototypes[self._clef]
        else:
            self._clef = None
            return None
    def _set_clef(self, clef):
        self._clef = clef.cle
    clef = property(_get_clef, _set_clef)
    
    def ouvrir(self):
        """Ouvre la porte."""
        if self.ouverte:
            raise ValueError("la porte est déjà ouverte")
        self.ouverte = True
    
    def fermer(self):
        """Ferme la porte."""
        if not self.ouverte:
            raise ValueError("la porte est déjà fermée")
        self.ouverte = False
    
    def verrouiller(self):
        """Verrouille la porte."""
        if self.verrouillee:
            raise ValueError("la porte est déjà verrouillée")
        self.verrouillee = True
    
    def deverrouiller(self):
        """Déverrouille la porte."""
        if not self.verrouillee:
            raise ValueError("la porte est déjà déverrouillée")
        self.verrouillee = False
