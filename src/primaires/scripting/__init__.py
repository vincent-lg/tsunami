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


"""Fichier contenant le module primaire scripting."""

import re

from abstraits.module import *
from .config import cfg_scripting

class Module(BaseModule):
    
    """Cette classe contient les informations du module primaire scripting.
    Ce module gère le langage de script utilisé pour écrire des quêtes et
    personnaliser certains objets de l'univers. Il regroupe également les
    éditeurs et les objets gérant les quêtes.
    
    """
    
    def __init__(self, importeur):
        """Constructeur du module"""
        BaseModule.__init__(self, importeur, "scripting", "primaire")
        self.cfg = None
    
    def config(self):
        """Méthode de configuration du module"""
        self.cfg = type(self.importeur).anaconf.get_config("scripting",
            "scripting/syntaxe.cfg", "config scripting", cfg_scripting)
        
        BaseModule.config(self)
    
    def init(self):
        """Initialisation"""
        #self.test_instruction("test(33, ab, -4.5, 1.48, \"ok,d\",oa123)")
        BaseModule.init(self)
    
    def test_instruction(self, chaine):
        """Test d'instruction.
        Méthode de debug.
        
        """
        cfg = self.cfg
        identifiant = cfg.identifiant
        type_de_donnee = "(" + ")|(".join([cfg.chaine, cfg.nombre, cfg.identifiant]) + ")"
        affectation = cfg.affectation.format(identifiant=identifiant,
                type_de_donnee=type_de_donnee)
        sep = cfg.sep
        fonction = r"({nom_fonction}){dg}({type_de_donnee})?({sep}({type_de_donnee}))*{dd}"
        fonction = fonction.format(nom_fonction=cfg.nom_fonction,
                sep=sep, type_de_donnee=type_de_donnee,
                dg=cfg.delimiteur_gauche, dd=cfg.delimiteur_droit)
        
        reg = re.compile("^" + fonction + "$", re.DEBUG)
        res = reg.search(chaine)
        if res is None:
            print("Non !")
            return
        
        nom_fonction = res.groups()[0]
        arg = res.groups()[1] or ""
        args = []
        if arg:
            args.append(arg)
        
        delimiteur_droit = cfg.delimiteur_droit.replace("\\", "")
        pos_del = -len(delimiteur_droit) or None
        chaine = chaine[len(nom_fonction) + 1 + len(arg):pos_del]
        ARGUMENT = r"({sep}({a}))({sep}({a}))*".format(a=type_de_donnee, sep=sep)
        RE_ARGUMENT = re.compile("^" + ARGUMENT + "$")
        while chaine:
            res = RE_ARGUMENT.search(chaine)
            groupes = res.groups()
            arg_c = groupes[0]
            arg_n = groupes[1]
            chaine = chaine[len(arg_c):]
            args.append(arg_n)
        
        print(nom_fonction, args)
