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


"""Type de filtre bool."""

from primaires.recherche.type_filtre import TypeFiltre

class Bool(TypeFiltre):

    """Classe représentant le type de filtre bool.

    Ce filtre est utilisé pour comparer des booléens simples. La valeur
    doit être soit 0 (False) soit 1 (True).

    """

    cle = "bool"
    aide = """
        une valeur optionnelle. Si la valeur n'est pas précisée,
        le booléen est considéré comme vrai. Vous pouvez préciser |ent|1|ff|
        ou |ent|0|ff| pour indiquer, respectivement, que le booléen
        doit être vrai (c'est déjà le cas par défaut) ou faux. Les
        caractères |ent|=|ff| et |ent|!|ff| ont la même valeur.
    """

    @classmethod
    def tester(cls, objet, attribut, valeur):
        """Méthode testant la valeur.

        Cette méthode doit retourner True si la valeur correspond à la
        recherche, False sinon.

        """
        if valeur in ("0", "!"):
            valeur = "False"
        elif valeur in ("", "1", "="):
            valeur = "True"
        else:
            raise TypeError("valeur {} invalide".format(repr(valeur)))

        return attribut == valeur
