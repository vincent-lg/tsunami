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


"""Module contenant des fonctions utiles aux corps.

Elles sont donc utilisables par les modules, primaires ou secondaires.

Liste des fonctions :
    valider_cle     Valide une chaîne comme une clé (un identifiant) valide
    lisser          Lisse une chaîne ("de le" = "du")
    get_nom_nombre  Retourne le nom du nombre

"""

import re

# Constantes
RE_CLE_VALIDE = re.compile(r"^[a-z0-9_]+$")
NOMBRES = {
    1: "un",
    2: "deux",
    3: "trois",
    4: "quatre",
    5: "cinq",
    6: "six",
    7: "sept",
    8: "huit",
    9: "neuf",
    10: "dix",
    11: "onze",
    12: "douze",
    13: "treize",
    14: "quatorze",
    15: "quinze",
    16: "seize",
    17: "dix-sept",
    18: "dix-huit",
    19: "dix-neuf",
    20: "vingt",
}
def valider_cle(chaine):
    """Valide la chaîne passée en paramètre comme étant une clé.
    
    Une clé doit être une chaîne constituée de caractères minuscules,
    de chiffres et du signe _ (souligné).
    
    Si la chaîne passé en paramètre ne remplit pas ces conditions,
    lève une exception ValueError.
    
    """
    if RE_CLE_VALIDE.search(chaine) is None:
        raise ValueError("{} n'est pas une clé valide".format(repr(chaine)))

def lisser(chaine):
    """Retourne la chaîne lisser.
    
    On lisse une chaîne en remplaçant certains schémas comme
    " de le " par " du ".
    
    """
    schemas = (
        (" le a", " l'a"),
        (" le e", " l'e"),
        (" le h", " l'h"),
        (" le i", " l'i"),
        (" le o", " l'o"),
        (" le u", " l'u"),
        (" le é", " l'é"),
        (" la a", " l'a"),
        (" la e", " l'e"),
        (" la h", " l'h"),
        (" la i", " l'i"),
        (" la o", " l'o"),
        (" la u", " l'u"),
        (" la é", " l'é"),
        (" de le ", " du "),
        (" de les ", " des "),
        (" à les ", " aux "),
        (" à le ", " au "),
        (" de a", " d'a"),
        (" de e", " d'e"),
        (" de h", " d'h"),
        (" de i", " d'i"),
        (" de o", " d'o"),
        (" de u", " d'u"),
        (" de é", " d'é"),
    )
    for o_val, r_val in schemas:
        chaine = chaine.replace(o_val, r_val)
    
    return chaine

def get_nom_nombre(nombre):
    """Retourne, si trouvé, le nom du nombre.
    
    Si le nombre est 1, retourne par exemple "un".
    
    Si le nombre est trop élevé (seuls les vingt premiers
    nombres sont donnés), retourne le nombre en forme de chaîne.
    
    """
    return NOMBRES.get(nombre, str(nombre))
