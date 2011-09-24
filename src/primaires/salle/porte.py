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


"""Fichier contenant la classe Porte, détaillée plus bas;"""

from abstraits.id import ObjetID

class Porte(ObjetID):
    
    """Cette classe définit une porte dans une sortie.
    
    Une porte est un objet naturellement commun à deux sorties :
        La sortie d'origine
        La sortie de destination
    
    La sortie de destination est la sortie opposée de la sortie d'origine.
    
    La classe porte définit :
        serrure -- la présence d'une serrure
        ouverte -- Le flag d'ouverture de la porte
            Notez aue la propriété fermee existe également.
    
    """
    
    groupe = "porte"
    sous_rep = "sorties/portes"
    def __init__(self):
        """Constructeur de la porte."""
        ObjetID.__init__(self)
        self.ouverte = False
        self.serrure = False
        # On passe le statut en CONSTRUIT
        self._construire()
    
    def __getnewargs__(self):
        return ()
    
    @property
    def fermee(self):
        return not self.ouverte
    
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

ObjetID.ajouter_groupe(Porte)
