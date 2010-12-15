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


"""Fichier contenant des fonctions utiles à la manipulation des noeuds"""

from primaires.interpreteur.masque.noeuds.embranchement import Embranchement
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
            if nv_noeud.est_parametre():
                commande = nv_noeud.masque
                nv_embranchement = Embranchement()
                nv_embranchement.ajouter_fils(nv_noeud, commande)
                nv_noeud.suivant = creer_noeud(commande, schema)
                nv_noeud = nv_embranchement
            else:
                nv_noeud.suivant = creer_noeud(commande, schema)
    
    return nv_noeud

def ajouter_fils(noeud_racine, noeud_fils):
    """Ajoute un fils au noeud racine spécifié.
    Si c'est un embranchement, on ajoute un fils.
    Sinon, on modifie tout simplement le noeud suivant.
    
    """
    if isinstance(noeud_racine, Embranchement):
        noeud_racine.suivant.append(noeud_fils)
    else:
        noeud_racine.suivant = noeud_fils
    
    return noeud_fils

def etendre_arborescence(racine_base, racine_sup, cmd_base, cmd_sup):
    """Etend l'arborescence de racine_base grâce à racine_sup."""
    # On cherche une divergence
    # Si on en trouve pas, on cherche le fils commun aux deux arborescence et
    # on appelle récursivement la fonction
    suiv_base = racine_base.suivant
    
    trouve = False
    if type(suiv_base) is not dict:  # ce n'est pas un embranchement
        suiv_base = {suiv_base: cmd_base}
    
    for suiv, cmd in suiv_base.items():
        if not trouve and suiv.nom == racine_sup.nom:
            # On a trouvé un point commun, on appelle récursivement la fonction
            etendre_arborescence(suiv, racine_sup.suivant, cmd, cmd_sup)
            trouve = True
    
    if not trouve: # on n'a trouvé aucun point commun
        inserer_embranchement(racine_base, racine_sup, cmd_base, cmd_sup)

def inserer_embranchement(racine_base, racine_sup, cmd_base, cmd_sup):
    """Insère un embranchement au noeud suivant de racine_base.
    Dans cet embranchement, on place en fils :
    -   l'ancien fils direct de racine_base
    -   la racine_sup
    
    Si le fils de racine_base est déjà un embranchement, on insère simplement
    racine_sup.
    
    """
    if isinstance(racine_base, Embranchement):
        racine_base.ajouter_fils(racine_sup, cmd_sup)
    elif isinstance(racine_base.suivant, Embranchement):
        racine_base.suivant.ajouter_fils(racine_sup, cmd_sup)
    else:
        fils = racine_base.suivant
        racine_base.suivant = Embranchement()
        if fils:
            racine_base.suivant.ajouter_fils(fils, cmd_base)
        racine_base.suivant.ajouter_fils(racine_sup, cmd_sup)
