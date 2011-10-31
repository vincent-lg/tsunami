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


"""Module contenant la base des fonctions aléatoires.

Fonctions définies :
    choix_probable(objets, attribut)
    varier(base, variable, min=1, max=None)

"""

import random

def choix_probable(objets, attribut="probabilite"):
    """Retourne aléatoirement un choix en fonction de certaines probabilités.
    
    Chaque élément du paramètre objets est un objet avec
    une certaine probabilité. La probabilité indiquée est un poids
    en terme d'effectif, pas nécessairement un taux ou pourcentage.
    La probabilité de l'objet se déduit grâce au nom d'attribut
    passé en second paramètre (par défaut 'probabilite').
    
    Si vous passez à cette fonction une liste d'objets en premier
    paramètre (sans second paramètre), la fonction va constituer
    la liste des effectifs en cherchant, sur chaque objet,
    la valeur de l'attribut 'probabilite'.
    
    Elle retournera ensuite un objet de la liste.
    
    Les objets d'effectif 0 n'ont aucune chance de sortir.
    
    """
    poids = [getattr(objet, attribut) for objet in objets]
    rnd = random.random() * sum(poids)
    for i, w in enumerate(weights):
        rnd -= w
        if rnd < 0:
            return objets[i]

def varier(base, variable, min=1, max=None):
    """Retourne un entier varié de base + ou - variable.
    
    min et max permettent de définir la marge minimum et maximum dans
    laquelle peut se trouver la valeur ede retour.
    
    Par exemple :
        varier(15, 5) retourne un nombre entre 10 et 20
        varier(25, 30, min=1) retourne un entier entre 1 et 55
    
    Note : si une des bornes min ou max est à None, la valeur de retour ne
    sera pas limitée sur cette borne. La valeur de min étant de 1 par défaut,
    cela signifie que l'appel à la fonction varier ne retournera que des
    entiers par défaut. Pour modifier ce comportement, passez None à
    l'argument min.
    
    """
    r_min = base - variable
    r_max = base + variable
    if min is not None:
        r_min = min if min > r_min else r_min
    if max is not None:
        r_max = max if max < r_max else r_max
    
    return random.randint(r_min, r_max)
