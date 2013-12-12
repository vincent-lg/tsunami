# -*-coding:Utf-8 -*

# Copyright (c) 2013 LE GOFF Vincent
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


"""Fichier contenant la donnée de configuration 'nb_abandon'."""

from secondaires.navigation.equipage.donnees.base import Donnee

class NbAbandon(Donnee):

    """Classe définissant la donnée de configuration 'nb_abandon'.

    Cette donnée de configuration permet de configurer le nombre minimum
    de matelots avant que l'équipage se rende. Si cette donnée est à
    5 et qu'il ne reste plus que 5 matelots dans l'équipage, alors
    l'équipage se rend.

    """

    cle = "nb_abandon"
    expression = Donnee.compiler(r"^([0-9]+) matelots minimum$")

    def __init__(self, nombre=1):
        Donnee.__init__(self)
        self.nombre = nombre

    def __str__(self):
        return "Nombre de matelots minimum avant abandon : {}".format(
                self.nombre)

    def valeur(self):
        return self.nombre

    @classmethod
    def defaut(cls):
        """Retourne le nombre minimum de matelots par défaut."""
        return 0

    @classmethod
    def convertir(cls, nombre):
        return (int(nombre), )
