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


"""Type de filtre chaine."""

from primaires.format.fonctions import supprimer_accents
from primaires.recherche.type_filtre import TypeFiltre

class Chaine(TypeFiltre):

    """Classe représentant le type de filtre chaîne.

    Ce filtre est utilisé pour comparer des chaînes de caractère simples.

    """

    cle = "chaine"
    aide = """
        une chaîne simple comme un ou une suite de mot(s). Les accents
        et majuscules sont ignorés lors de la recherche.
    """

    @classmethod
    def tester(cls, objet, attribut, valeur):
        """Méthode testant la valeur.

        Cette méthode doit retourner True si la valeur correspond à la
        recherche, False sinon.

        """
        valeur = supprimer_accents(valeur).lower().replace("_b_", "|")
        attribut = supprimer_accents(attribut).lower()
        return valeur in attribut
