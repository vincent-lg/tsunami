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


MASQUE_MESSAGE = """
\"""Package contenant les masques du module {module}.\"""
"""


CONTENU_MASQUE = """
\"""Package contenant le masque '<{lmasque}>'.

\"""

from primaires.interpreteur.masque.masque import Masque
from primaires.interpreteur.masque.fonctions import *
from primaires.interpreteur.masque.exceptions.erreur_validation \\
        import ErreurValidation

class {masque}(Masque):
    
    \"""Masque <{lmasque}>.
    
    \"""
    
    nom = "{lmasque}"
    nom_complet = "{nom_complet}"
    
    def init(self):
        \"""Initialisation des attributs\"""
        pass
    
    def valider(self, personnage, dic_masques, commande):
        \"""Validation du masque\"""
        Masque.valider(self, personnage, dic_masques, commande)
    

"""

def ajouter(rep, module, typeMod, entete, commande):
    if len(commande) < 2:
        print("Pas assez d'argument")
        return
    
    masque = commande[1].lower()
    nom_complet = masque
    if len(commande) > 2:
        nom_complet = commande[2]
    
    contenu = CONTENU_MASQUE.format(lmasque=masque,masque=masque.capitalize(),
        nom_complet=nom_complet)
    
    repmasque = rep + "masques/" + masque + "/"
    
    os.makedirs(repmasque)
    
    path = repmasque + "__init__.py"
    if os.path.exists(path):
        print("Un masque portant ce nom existait, annulation")
        return
    write(path, entete + contenu)
    
    path = rep + "masques/" + "__init__.py"
    
    if not os.path.exists(path):
        write(path, entete + MASQUE_MESSAGE.format(module=module))
    
    append(path, "from . import {masque}\n".format(masque=masque))
    
