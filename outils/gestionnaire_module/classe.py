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

CONTENU_CLASSE = """
\"""Ce fichier contient la classe {classe} détaillée plus bas.\"""

from abstraits.obase import BaseObj

class {classe}(BaseObj):

    \"""
    TODO
    \"""
    
    def __init__(self):
        \"""Constructeur de la classe\"""
        pass
    
    def __getnewarges__(self):
        return ()
    

"""

CONTENU_CONTENEUR = """
\"""Ce fichier contient la classe {classe}s détaillée plus bas.\"""

import datetime
from datetime import timedelta

from abstraits.obase import BaseObj
from .conversation import Conversation

class Conversations(BaseObj):

    \"""Classe conteneur des {lclasse}s
    
    Voir : ./{lclasse}.py
    
    \"""
    
    def __init__(self, parent=None):
        \"""Constructeur du conteneur\"""
        BaseObj.__init__(self)
        self._{lclasse}s = []
    
    def __getnewargs__(self):
        return ()
    
    def iter(self):
        \"""Boucle sur les {lclasse}s contenues\"""
        return list(self._{lclasse}s)
    

"""

def ajouter(rep, entete, commande):
    
    if len(commande) < 2:
        print("Pas assez d'argument")
        return
    
    classe = commande[1].lower()
    
    contenu = CONTENU_CLASSE.format(classe=classe.capitalize())
    path = rep + classe + ".py"
    if os.path.exists(path):
        print("Une classe portant ce nom existait, annulation")
    else:
        write(path, entete + contenu)
    
    if len(commande) > 2 and commande[2] == "oui":
        contenu = CONTENU_CONTENEUR.format(lclasse=classe,classe=classe.capitalize())
        path = rep + classe + "s.py"
        if os.path.exists(path):
            print("Un conteneur portant ce nom existait, annulation")
            return
        write(path, entete + contenu)

