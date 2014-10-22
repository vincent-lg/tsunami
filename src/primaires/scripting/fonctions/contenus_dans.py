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


"""Fichier contenant la fonction contenus_dans."""

from fractions import Fraction

from primaires.scripting.fonction import Fonction
from primaires.scripting.instruction import ErreurExecution

class ClasseFonction(Fonction):

    """Renvoie les objets contenus dans un conteneur."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.contenus_dans, "Objet")

    @staticmethod
    def contenus_dans(conteneur):
        """Renvoie la liste des objets contenus dans ce conteneur.

        On doit donc utiliser une boucle pour pardcourir les objets
        retournés par cette fonction. Le conteneur peut être un conteneur
        simple, un conteneur de nourriture ou de potion. Dans ce dernier
        cas, il ne retourne qu'un seul objet qui est la potion contenue.

        NOTE IMPORTANTE : si le conteneur est un conteneur standard,
        ne retourne que les objets uniques. C'est-à-dire, principalement,
        que l'argent ne sera pas retourné.

        """
        if conteneur.est_de_type("conteneur de potion"):
            return [conteneur.potion] if conteneur.potion else []
        if conteneur.est_de_type("conteneur de nourriture"):
            return list(conteneur.nourriture)
        if conteneur.est_de_type("conteneur"):
            return list(conteneur.conteneur._objets)
        raise ErreurExecution("{} n'est pas un conteneur".format(conteneur))
