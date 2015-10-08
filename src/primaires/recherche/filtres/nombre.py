# -*-coding:Utf-8 -*

# Copyright (c) 2014 LE GOFF VINCENT
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


"""Type de filtre nombre."""

import re

from primaires.format.fonctions import supprimer_accents
from primaires.recherche.type_filtre import TypeFiltre

# Constantes
RE_SIMPLE = re.compile(r"^\d+(,\d+)?$")
RE_COMPLETE = re.compile(r"^\<(\d+)(,\d+)?\>(\d+)(,\d+)?$")

OPERATEURS = [
        (("=", "=="), lambda a, b: a == b),
        (("!", "!="), lambda a, b: a != b),
        (("<="), lambda a, b: a <= b),
        (("<"), lambda a, b: a < b),
        ((">="), lambda a, b: a > b),
        ((">"), lambda a, b: a > b),
]

class Nombre(TypeFiltre):

    """Classe représentant le type de filtre nombre.

    Ce filtre est utilisé pour chercher un nombre avec des opérateurs
    spécifiques. Par exemple on peut chercher 5 pour une recherche simple
    (égale à 5). On peut aussi chercher <3 pour trouver ceux inférieurs à 3.

    """

    cle = "nombre"
    aide = """
        un nombre (entier ou flottant). Vous pouvez préciser un nombre
        avec une virgule (comme |ent|3,5|ff|). Vous pouvez préfixer le
        nombre d'un opérateur permettant une recherche plus précise, par
        exemple |cmd|<8|ff| pour rechercher sur tous les nombres
        inférieurs (strictement) à 8. Vous pouvez utiliser les opérateurs
        |cmd|!|ff| (différent de), |cmd|<|ff| (strictement inférieur à),
        |cmd|<=|ff| (inférieur ou égal à), |cmd|>|ff| (strictement
        supérieur à) ou |cmd|>=|ff| (supérieur ou égal à). Vous pouvez
        également préciser un intervalle sous la forme
        |ent|<borne_inf>borne_sup|ff| pour rechercher dans tous les nombres
        compris entre les bornes inférieures et supérieures inclues.
        Par exemple |cmd|<3>8|ff|.
    """

    @classmethod
    def tester(cls, objet, attribut, valeur):
        """Méthode testant la valeur.

        Cette méthode doit retourner True si la valeur correspond à la
        recherche, False sinon.

        """
        attribut = float(attribut)

        # Est-ce un simple nombre ?
        if RE_SIMPLE.search(valeur):
            valeur = valeur.replace(",", ".")
            valeur = float(valeur)
            return attribut == valeur

        intervalle = RE_COMPLETE.search(valeur)
        if intervalle:
            groupes = intervalle.groups()
            borne_inf = groupes[0] + "." + (groupes[1] if groupes[1] else "0")
            borne_sup = groupes[2] + "." + (groupes[3] if groupes[3] else "0")
            borne_inf = float(borne_inf)
            borne_sup = float(borne_sup)
            return borne_inf <= attribut <= borne_sup

        # On cherche un éventuel opérateur
        for operateurs, fonction in OPERATEURS:
            for operateur in operateurs:
                if valeur.startswith(operateur):
                    valeur = valeur[len(operateur):]
                    valeur = valeur.replace(",", ".")
                    try:
                        valeur = float(valeur)
                    except ValueError:
                        raise TypeError("format de nombre {} inconnu".format(repr(valeur)))
                    return fonction(attribut, valeur)

        raise TypeError("format de nombre {} inconnu".format(repr(valeur)))
