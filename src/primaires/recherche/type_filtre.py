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


"""Module contenant la classe abtraite des types de filtres."""

types = {}

class MetaTypeFiltre(type):

    """Métaclasse des types de filtre."""

    def __init__(cls, nom, bases, contenu):
        """Constructeur de la métaclasse"""
        type.__init__(cls, nom, bases, contenu)
        if cls.cle:
            types[cls.cle] = cls

class TypeFiltre(metaclass=MetaTypeFiltre):

    """Classe abstraite représentant un type de filtre.

    Un type de filtre détermine le type de la donnée qu'il doit recevoir.
    La clé de la classe (attribut de classe) détermine le nom du filtre
    utilisé dans le cherchable. Un type de filtre peut être spécialisé dans
    les nombres, un autre dans les chaînes, un autre dans les regex, etc.

    Il est possible de définir d'autres types de filtre dans un module
    spécifique. Sinon, les types de filtre proposés dans le package
    'filtres' peuvent être utilisés depuis n'importe quel module.
    Le besoin de réimplémenter des types dans un module spécifique est
    normalement faible.

    """

    cle = ""

    def __repr__(self):
        return self.cle

    @classmethod
    def tester(cls, objet, attribut, valeur):
        """Méthode testant la valeur.

        Cette méthode doit retourner True si la valeur correspond à la
        recherche, False sinon. Elle doit être redéfinie par les
        types pour inclure des fonctionnalités tels que des opérateurs
        spécifiques ou autre.

        """
        raise NotImplementerError
