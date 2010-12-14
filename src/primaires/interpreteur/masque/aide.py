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


"""Fichier contenant des fonctions utiles à l'affichage de l'aide de
noeuds / masques.

"""

from textwrap import wrap

from primaires.format.constantes import *

def afficher_aide(personnage, masque_depart, embranchement_fils,
    explorer=1, dic_masques={}, indentation=0):
    """Fonction retournant l'aide de masque_depart.
    Les fils sont déduits de l'embranchement.
    Le nombre explorer permet de savoir combien de fois on explore
    récursivement l'arborescence (1 revient à juste le départ et les fils
    de l'embranchement).
    dic_masques est le dictionnaire des masques parcourus. Ce paramètre est
    utile quand l'aide doit être déduite d'une commande partiellement validée.
    Enfin, indentation est utile pour l'appel récursif, doit être laissé à 0
    par défaut.
    
    """
    if not dic_masques: # le dictionnaire des masques n'a pas été précisé
        dic_masques[masque_depart.nom] = masque_depart
    
    # On regroupe les masques dans une chaîne
    masques = " ".join([masque.nom for masque in dic_masques.values()])
    
    if indentation == 0: # c'est la première fois qu'on appelle la fonction
        chn_aide = "Synopsis : {0}".format(masques)
    else:
        chn_aide = masques
    
    indentation = len(chn_aide) + 3
    
    chn_aide += " - " + ("\n" + indentation * " ").join(wrap(
            masque_depart.aide_courte, longueur_ligne - indentation))
    
    if indentation == 0:
        chn_aide += "\n"
    
    return chn_aide
