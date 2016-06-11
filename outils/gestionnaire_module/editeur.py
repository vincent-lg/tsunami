# -*-coding:Utf-8 -*

# Copyright (c) 2010-2016 DAVY Guillaume
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


EDITEUR_MESSAGE = """
\"""Package contenant les éditeurs du module {module}.\"""
"""


CONTENU_EDITEUR = """
\"""Package contenant l'éditeur '{lediteur}'.
Si des redéfinitions de contexte-éditeur standard doivent être faites, elles
seront placées dans ce package.

Note importante : ce package contient la définition d'un éditeur, mais
celui-ci peut très bien être étendu par d'autres modules. Auquel cas,
les extensions n'apparaîtront pas ici.

\"""

from primaires.interpreteur.editeur import Editeur

class Edt{editeur}(Editeur):
    
    \"""Classe définissant l'éditeur '{lediteur}'.
    
    \"""
    
    nom = "{lediteur}"
    
    def __init__(self, personnage):
        \"""Constructeur de l'éditeur\"""
        if personnage:
            instance_connexion = personnage.instance_connexion
        else:
            instance_connexion = None
        Editeur.__init__(self, instance_connexion, attitude)
        self.ajouter_option("todo", self.opt_todo)
        self.aide_courte = "TODO\n"
    
    def opt_todo(self, arguments):
        pass
    

"""

def ajouter(rep, module, typeMod, entete, commande):
    if len(commande) < 2:
        print("Pas assez d'argument")
        return
    
    editeur = commande[1]
    
    contenu = CONTENU_EDITEUR.format(
        lediteur=editeur,
        editeur=editeur.capitalize())
    
    repediteur = rep + "editeurs/" + editeur + "/"
    
    os.makedirs(repediteur)
    
    path = repediteur + "__init__.py"
    if os.path.exists(path):
        print("Une commande portant ce nom existait, annulation")
        return
    write(path, entete + contenu)
    
    path = rep + "editeurs/" + "__init__.py"
    
    if not os.path.exists(path):
        write(path, entete + EDITEUR_MESSAGE.format(module=module))
    
    append(path, "from . import {editeur}\n".format(editeur=editeur))
    
    print("ATTENTION : vous devze modifié le __init__.py du module " \
        "pour y rajouter cette editeur")
    
