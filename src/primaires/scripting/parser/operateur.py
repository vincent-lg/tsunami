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


"""Fichier contenant la classe Operateur, détaillée plus bas."""

from .expression import Expression
from primaires.scripting.constantes.operateurs import OPERATEURS

class Operateur(Expression):
    
    """Expression opérateur.
    
    Les opérateurs sont définis dans le module
    primaires.scripting.constantes.operateurs.
   
    """
    
    nom = "operateur"
    def __init__(self):
        """Constructeur de l'expression."""
        Expression.__init__(self)
        self.operateur = None
    
    @classmethod
    def parsable(cls, chaine):
        """Retourne True si la chaîne est parsable, False sinon."""
        chaine = chaine.lstrip()
        if " " in chaine:
            fin = chaine.find(" ")
        else:
            fin = None
        chaine = chaine[:fin]

        return chaine in OPERATEURS.keys()
    
    @classmethod
    def parser(cls, chaine):
        """Parse la chaîne.
        
        Retourne l'objet créé et la partie non interprétée de la chaîne.
        
        """
        objet = cls()
        chaine = chaine.lstrip()
        if " " in chaine:
            fin = chaine.find(" ")
        else:
            fin = None
        objet.operateur = chaine[:fin]
        chaine = chaine[fin:]
        return objet, chaine
    
    def get_valeur(self, evt):
        """Retourne l'opérateur Python correspondant."""
        return OPERATEURS[self.operateur]
    
    def __repr__(self):
        return " op({}) ".format(self.operateur)
    
    def __str__(self):
        return str(self.operateur)
    
    @property
    def code_python(self):
        """Retourne le code Python associé."""
        return OPERATEURS[self.operateur]
