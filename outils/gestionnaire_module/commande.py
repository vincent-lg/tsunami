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


CMD_MESSAGE = """
\"""Package contenant les commandes du module {module}.\"""
"""


CONTENU_CMD = """
\"""Package contenant la commande '{lcommande}'.

\"""

from primaires.interpreteur.commande.commande import Commande

class Cmd{commande}(Commande):
    
    \"""Commande '{lcommande}'.
    
    \"""
    
    def __init__(self):
        \"""Constructeur de la commande\"""
        Commande.__init__(self, "{lcommande}", "{commande_en}")
        self.nom_categorie = "{categorie}"
        self.schema = "{schema}"
        self.aide_courte = "TODO"
        self.aide_longue = \\
            "TODO"
    
    def interpreter(self, personnage, dic_masques):
        \"""Interprétation de la commande\"""
        pass
    

"""

def ajouter(rep, module, typeMod, entete, commande):
    if len(commande) < 2:
        print("Pas assez d'argument")
        return
    
    commande_fr = commande[1].lower()
    commande_en = commande_fr
    schema = ""
    categorie = ""
    if len(commande) > 2:
        commande_en = commande[2]
    if len(commande) > 3:
        categorie = commande[3]
    if len(commande) > 4:
        schema = commande[4]
    
    contenu = CONTENU_CMD.format(
        lcommande=commande_fr,
        commande=commande_fr.capitalize(),
        commande_en=commande_en,
        categorie = categorie,
        schema = schema)
    
    repcmd = rep + "commandes/" + commande_fr + "/"
    
    os.makedirs(repcmd)
    
    path = repcmd + "__init__.py"
    if os.path.exists(path):
        print("Une commande portant ce nom existait, annulation")
        return
    write(path, entete + contenu)
    
    path = rep + "commandes/" + "__init__.py"
    
    if not os.path.exists(path):
        write(path, entete + CMD_MESSAGE.format(module=module))
    
    append(path, "from . import {commande}\n".format(commande=commande_fr))
    
    print("ATTENTION : vous devze modifié le __init__.py du module " \
        "pour y rajouter cette commande")
    
