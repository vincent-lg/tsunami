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


import re

from .instruction import Instruction

"""Fichier contenant la classe Action, détaillée plus bas."""

class Action(Instruction):
    
    """Classe définissant une action.
    
    Une action est une instruction effectuant une action précise (dire
    à un joueur, faire apparaître un objet, créer une tempête...).
    
    """
    
    schema_arguments = None
    type_de_donnee = ""
    def __init__(self, cfg):
        """Construction d'une action.
        
        """
        Instruction.__init__(self, cfg)
        self.groupes["nom"] = ""
        self.groupes["parametres"] = ()
    
    def parser(self, regex, chaine):
        """Parse la regex de recherche.
        
        La chaîne va être utile ici car les arguments de l'action ne sont pas
        extraits par la première regex.        
        
        """
        nom_fonction = regex.groups()[0]
        arg = regex.groups()[1] or ""
        args = []
        if arg:
            args.append(arg)
        
        delimiteur_droit = self.cfg.delimiteur_droit.replace("\\", "")
        pos_del = -len(delimiteur_droit) or None
        chaine = chaine[len(nom_fonction) + 1 + len(arg):pos_del]
        regex_argument = r"({sep}({a}))({sep}({a}))*".format(
                a=type(self).type_de_donnee, sep=self.cfg.sep)
        argument_compile = re.compile("^" + type(self).schema_argument + "$")
        while chaine:
            res = argument_compile.search(chaine)
            groupes = res.groups()
            arg_c = groupes[0]
            arg_n = groupes[1]
            chaine = chaine[len(arg_c):]
            args.append(arg_n)
        
        self.groupes["nom"] = nom_fonction
        self.groupes["parametres"] = tuple(args)
