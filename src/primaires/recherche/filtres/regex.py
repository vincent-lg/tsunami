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


"""Type de filtre regex."""

import re

from primaires.format.fonctions import supprimer_accents
from primaires.recherche.type_filtre import TypeFiltre

class Regex(TypeFiltre):

    """Classe représentant le type de filtre regex.

    Ce filtre est utilisé pour chercher dans une expression rationnelle.

    """

    cle = "regex"
    aide = """
        une expression régulière. Ce peut être une chaîne simple mais
        il y a des options plus précises pour rechercher le début, la
        fin, des expressions plus précises, etc.
    """

    @classmethod
    def tester(cls, objet, attribut, valeur):
        """Méthode testant la valeur.

        Cette méthode doit retourner True si la valeur correspond à la
        recherche, False sinon.

        """
        valeur = supprimer_accents(valeur).lower().replace("_b_", "|")
        attribut = supprimer_accents(attribut).lower()
        try:
            valeur = valeur = re.compile(valeur, re.I)
        except re.error:
            raise TypeError(
                    "le type précisé doit être une expression régulière")
        else:
            return valeur.search(attribut)
