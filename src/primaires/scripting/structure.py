# -*-coding:Utf-8 -*

# Copyright (c) 2010-2017 LE GOFF Vincent
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


"""Fichier contenant la classe Structure détaillée plus bas."""


from abstraits.obase import *

class StructureSimple(BaseObj):

    """Classe contenant une simple structure non enregistrée.

    Les structures sont manipulables dans le scripting comme des
    dictionnaires. Elles en contiennent d'ailleurs un. La différemce
    avec le dictionnaire est qu'elles peuvent être enregistrés et
    récupérés dans le système. Les structures simples sont faites
    pour être enregistrées dans d'autres objets, cependant, pas
    pour être récupérées. Voir la classe StructureComplete plus bas.
    Toutefois, il est à noter que ces deux classes partagent la
    même hiérarchie et le même fonctionnement (simplement, l'une
    d'entres elles possède des mécanismes pour être enregistrés
    directement).

    """

    def __init__(self):
        """Constructeur d'une variable"""
        BaseObj.__init__(self)
        self.donnees = {}
        self._construire()

    def __getnewargs__(self):
        return ()

    def __repr__(self):
        return "<Structure {}>".format(repr(self.donnees))

    def __str__(self):
        return str(self.donnees)

    def __getattr__(self, nom):
        """Essaye de récupérer la valeur indiquée."""
        if "_statut" not in self.__dict__ or not self.construit:
            return object.__getattr__(self, nom)
        else:
            return self.donnees.get(nom)

    def __setattr__(self, nom, valeur):
        """Modifie la donnée."""
        if not self.construit:
            object.__setattr__(self, nom, valeur)
        else:
            self.donnees[nom] = valeur

    def get_nom_pour(self, personnage):
        """Affichage d'une structure."""
        return str(self)


class StructureComplete(StructureSimple):

    """Une structure de données destinée à être enregistrée."""

    enregistrer = True

    def __init__(self, structure):
        StructureSimple.__init__(self)
        self.donnees.update({
                "structure": structure,
                "id": 0,
        })

    def __getnewargs__(self):
        return ("inconnu", )
