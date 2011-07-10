# -*-coding:Utf-8 -*

# Copyright (c) 2011 DAVY Guillaume
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

from .divers import *


CONTEXTE_MESSAGE = """
\"""Package contenant les contextes du module {module}.\"""
"""


CONTENU_CONTEXTE = """
\"""Package contenant le contexte '{module}:{lcontexte}'.

\"""

from primaires.interpreteur.contexte import Contexte

class {contexte}(Contexte):
    
    \"""Contexte '{lcontexte}'.
    
    \"""
    
    def __init__(self, pere):
        \"""Constructeur du contexte\"""
        Contexte.__init__(self, pere)
        self.opts.prompt_prf = ""
        self.opts.prompt_clr = ""
        self.options = {{
            "q" : self.opt_quit,
            }}
    
    def __getstate__(self):
        \"""Nettoyage des options\"""
        dico_attr = Contexte.__getstate__(self)
        dico_attr["options"] = dico_attr["options"].copy()
        for rac, fonction in dico_attr["options"].items():
            dico_attr["options"][rac] = fonction.__name__
        return dico_attr
    
    def __setstate__(self, dico_attr):
        \"""Récupération du contexte\"""
        Contexte.__setstate__(self, dico_attr)
        for rac, nom in self.options.items():
            fonction = getattr(self, nom)
            self.options[rac] = fonction
    
    def accueil(self):
        \"""Message d'accueil du contexte\"""
        res = "TODO"
        return res
    
    def interpreter(self, msg):
        \"""Méthode d'interprétation du contexte\"""
        if msg.startswith("/"):
            # C'est une option
            # On extrait le nom de l'option
            mots = msg.split(" ")
            option = mots[0][1:]
            arguments = " ".join(mots[1:])
            if option not in self.options.keys():
                self.pere << "|err|Option invalide ({{}}).|ff|".format(option)
            else: # On appelle la fonction correspondante à l'option
                fonction = self.options[option]
                fonction(arguments)            
        else:
            pass
    
    def opt_quit(self, arguments):
        \"""Option quitter : /q\"""
        #TODO
        pass
    

"""

def ajouter(rep, module, typeMod, entete, commande):
    if len(commande) < 2:
        print("Pas assez d'argument")
        return
    
    contexte = commande[1].lower()
    
    contenu = CONTENU_CONTEXTE.format(
        lcontexte=contexte,
        contexte=contexte.capitalize(),
        module=module)
    
    repcontexte = rep + "contextes/" + contexte + "/"
    
    os.makedirs(repcontexte)
    
    path = repcontexte + "__init__.py"
    if os.path.exists(path):
        print("Un contexte portant ce nom existait, annulation")
        return
    write(path, entete + contenu)
    
    path = rep + "contextes/" + "__init__.py"
    
    if not os.path.exists(path):
        write(path, entete + CONTEXTE_MESSAGE.format(module=module))
    
    append(path, "from .{lcontexte} import {contexte}\n".format(
        lcontexte=contexte,contexte=contexte.capitalize()))
    

