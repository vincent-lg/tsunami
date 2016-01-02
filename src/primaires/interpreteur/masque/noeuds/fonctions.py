# -*-coding:Utf-8 -*

# Copyright (c) 2010-2016 LE GOFF Vincent
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


"""Fichier contenant des fonctions utiles à la manipulation des noeuds"""

from primaires.interpreteur.masque.noeuds.noeud_masque import NoeudMasque
from primaires.interpreteur.masque.noeuds.noeud_optionnel import NoeudOptionnel

def creer_noeud(commande, schema):
    """Fonction appelée pour créer un noeud.
    Elle prend en paramètre :
    commande - la commande
    schema   - le schéma, sous la forme d'une liste de caractères, qui va
               nous indiquer quel noeud créer
    
    """
    nv_noeud = None
    while schema and schema[0] == " ":
        schema.pop(0)
    if schema:  # schema n'est pas vide
        caractere = schema[0]
        if caractere == '(': # un noeud optionnel
            schema.pop(0)
            noeud_interne = creer_noeud(commande, schema)
            noeud_suivant = creer_noeud(commande, schema)
            nv_noeud = NoeudOptionnel(noeud_interne, noeud_suivant)
        elif caractere == ')':
            schema.pop(0)
            nv_noeud = None
        else:
            nv_noeud = NoeudMasque(commande, schema)
            nv_noeud.construire_depuis_schema(schema)
            nv_noeud.suivant = creer_noeud(commande, schema)
    
    return nv_noeud

