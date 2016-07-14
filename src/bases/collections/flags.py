# -*-coding:Utf-8 -*

# Copyright (c) 2010-2016 LE GOFF Vincent
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


"""Fichier contenant la classe Flags détaillée plus bas."""

class Flags:

    """Classe représentant des constantes de flags.

    Elle est simple à utiliser : d'abord, on crée le flag en constante
    (par exemple une variable de premier niveau du module), ensuite on
    ajoute les flags grâce à la méthode 'ajouter' en précisant le nom du
    flag et sa valeur binaire (1, 2, 4, 8, 16, 32...).
    On peut accéder à l'objet des flags comme un dictionnaire (avec
    les méthodes 'keys', 'values' et 'items').

    """

    def __init__(self):
        self.flags = {}

    def __contains__(self, nom):
        return nom in self.flags

    def __getitem__(self, nom):
        return self.flags[nom]

    def __setitem__(self, nom, valeur):
        raise RuntimeError("Operation non permise, utiliser la méthode " \
                "'ajouter'")

    def ajouter(self, nom, binaire=0):
        flags = list(self.flags.values())
        if binaire in self.flags.values():
            raise ValueError("le flag {} est déjà utilisé".format(binaire))
        if flags:
            flag = max(flags)
            flag = flag * 2
        else:
            flag = 1

        if binaire:
            self.flags[nom] = binaire
        else:
            raise ValueError("le flag {} n'a pas de valeur binaire " \
                    "spécifiée, attend {}".format(nom, flag))
        
        return binaire

    def keys(self):
        return self.flags.keys()

    def values(self):
        return self.flags.values()

    def items(self):
        return self.flags.items()
