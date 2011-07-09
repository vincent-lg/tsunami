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

from abstraits.obase import BaseObj

"""Fichier contenant la classe Instruction, détaillée plus bas."""

class Instruction(BaseObj):
    
    """Classe abstraite définissant une instruction.
    Les différents types d'instructions doivent en hériter.
    Par exemple, l'instruction conditionnelle, la fonction, les boucles si
    existent.
    
    Cette classe propose plusieurs mécanismes génériques de manipulation
    d'instruction.
    Elle est notamment capable de dire si une chaîne de caractère
    correspond à son schéma de validation.
    
    """
    
    schema = None
    def __init__(self, cfg):
        """Construction d'une instruction.
        
        Note : on ne doit pas construire une isntruction mais une de ses
        classes filles.
        
        """
        BaseObj.__init__(self)
        self.cfg = cfg
        self.groupes = {}
    
    def changer_schema(nouveau_schema):
        """Met à jour le schéma.
        On le compile pour plus de facilité.
        
        """
        Instruction.schema = re.compile(nouveau_schema)
    
    def correspond_schema(self, chaine):
        """Retourne True si la chaîne correspond au schéma, False sinon.
        
        Le schéma est donné sous la forme d'une regex.
        
        """
        return type(self).schema.search(chaine)
    
    def parser(self, regex, chaine):
        """Parse la regex de recherche.
        
        Ce parsage peut s'appuyer sur regex.groups().
        Redéfinir cette méthode dans la classe fille.
        
        """
        raise NotImplementedError
