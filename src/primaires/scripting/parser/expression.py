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


"""Fichier contenant la classe Expression, détaillée plus bas."""

from abstraits.obase import BaseObj

from . import MetaExpression

class Expression(BaseObj, metaclass=MetaExpression):
    
    """Classe abstraite définissant une expression.

    Une expression est un élément exclusif d'une instruction.
    Dans sa forme la plus simple, une expression peut être une
    chaîne de caractère, une variable, un entier, un flottant.
    Dans sa forme la plus complexe, une expression peut être une fonction.
    
    Notez cependant qu'une expression n'est pas une action : une action
    est constituée de plusieurs instructions. Il en va de même pour
    les conditions. Chaque instruction a pour rôle de parser
    la chaîne ajoutée en fonction de s expressions qu'elle attend.
    Par exemple, une action est constituée d'un nom d'action et
    de plusieurs paramètres (soit des chaînes de caractères, soit
    des entiers, soit des variables... soit des fonctions).
    
    Méthodes définies dans la classe abstraite :
        __repr__ -- méthode retournant une chaîne de debug de l'expression
        __str__ -- méthode retournant l'expression telle qu'affichée
        parsable -- retourne True si la chaîne passée en paramètre est
                    parsable par l'expression
        parser -- retourne l'objet créé par le parsage et la chaîne
                  non interprétée
        code_python -- propriété retournant le code Python lié
        
    Pour plus de détails sur chacune des méthodes, consultez leur
    documentation.
    
    """
    
    nom = ""
    expressions_def = None
    def __init__(self):
        """Constructeur d'une expression."""
        BaseObj.__init__(self)
    
    def __getnewargs__(self):
        return ()
    
    @classmethod
    def parsable(cls, chaine):
        """Retourne True si l'expression peut parser cette chaîne.
        
        Chaque expression a ses règles de parsage.
        Par exemple, une chaîne est parsable si elle commence par
        un guillemet et qu'un autre guillemet au minimum peut être
        trouvé plus loin dans la chaîne.
        
        """
        raise NotImplementedError
    
    @classmethod
    def parser(cls, chaine):
        """Parse la chaîne passée en paramètre.
        
        Cette méthode retourne deux informations :
            l'objet de type expression nouvellement créé
            la chaîne non interprétée
        
        Pour des exemples plus concrets, regardez les implémentations
        des différentes expressions.
        
        """
        raise NotImplementedError
    
    def get_valeur(self, evt):
        """Retourne l'objet Python parsé."""
        raise NotImplementedError
    
    @property
    def code_python(self):
        """Retourne le code Python associé.
        
        Ce code doit être sous la forme d'une chaîne de caractères.
        
        """
        raise NotImplementedError
    
    @staticmethod
    def choisir(types, chaine):
        return MetaExpression.choisir(types, chaine)
