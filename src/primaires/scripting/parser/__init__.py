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


"""Package contenant le parser du scripting.

Il ne définit pas le parsage des actions ou conditions, mais celui
des différents types de données, des entiers, flottants, chaînes de
caractères, ainsi que des fonctions.

Pour voir la classe de base des expressions, rendez-vous dans le fichier
Expression.py.

Dans ce fichier est également conservé la métaclasse des expressions.

"""

from abstraits.obase import MetaBaseObj

expressions = {}

class MetaExpression(MetaBaseObj):
    
    """Métaclasse représentant une expression.
    
    Elle se contente d'ajouter chaque classe avec un nom valide dans
    le dictionnaire des expressions.
    
    """
    
    def __init__(cls, nom, bases, attrs):
        """Constructeur de la classe."""
        MetaBaseObj.__init__(cls, nom, bases, attrs)
        if cls.nom:
            expressions[cls.nom] = cls
            cls.expressions_def = expressions
    
    @staticmethod
    def choisir(types, chaine):
        """Parse la chaîne entre les types sélectionnés et en choisit un.
        
        Les types doivent être donnés sous la forme d'une liste de
        chaînes de caractères, comme ("calcul", "fonction", "variable"].
        
        On retourne l'expression du type choisi et la chaîne non interprétée.
        
        Le choix se fait sur le critère d'interprétation : le type
        d'expression interprétant la plus grande partie de la chaîne
        est choisi.
        
        """
        types = [expressions[t] for t in types]
        types_app = [type for type in types if type.parsable(chaine)]
        if not types_app:
            raise ValueError("impossible de parser {}".format(chaine))
        
        a_chaine = t_chaine = chaine
        expression = None
        for type in types_app:
            chaine = a_chaine
            exp, chaine = type.parser(chaine)
            if len(chaine) < len(t_chaine):
                t_chaine = chaine
                expression = exp
        
        return expression, t_chaine


from .chaine import *
from .nombre import *
from .variable import *
from .fonction import *
from .calcul import *
from .operateur import *
from .connecteur import *
from .tests import *
