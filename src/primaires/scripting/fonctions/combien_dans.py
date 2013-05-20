# -*-coding:Utf-8 -*

# Copyright (c) 2012 LE GOFF Vincent
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


"""Fichier contenant la fonction combien_dans."""

from primaires.scripting.fonction import Fonction
from primaires.scripting.instruction import ErreurExecution

class ClasseFonction(Fonction):

    """Renvoie le nombre d'objets dans un conteneur."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.cb_dans, "Objet")
        cls.ajouter_types(cls.cb_dans_proto, "Objet", "str")

    @staticmethod
    def cb_dans(conteneur):
        """RRenvoie le nombre d'objets contenus dans le conteneur."""
        if conteneur.est_de_type("conteneur de potion"):
            return 1 if conteneur.potion else 0
        if conteneur.est_de_type("conteneur de nourriture"):
            return len(conteneur.nourriture)
        if conteneur.est_de_type("conteneur"):
            return sum(nb for o, nb in conteneur.conteneur.iter_nombres)
        raise ErreurExecution("{} n'est pas un conteneur".format(conteneur))

    @staticmethod
    def cb_dans_proto(conteneur, prototype):
        """Renvoie la quantité d'objets du prototype dans le conteneur."""
        if not prototype in importeur.objet.prototypes:
            raise ErreurExecution("prototype {} introuvable".format(prototype))
        prototype = importeur.objet.prototypes[prototype]
        if conteneur.est_de_type("conteneur de potion"):
            if conteneur.potion and conteneur.potion.prototype is prototype:
                return 1
            return 0
        if conteneur.est_de_type("conteneur de nourriture"):
            return len(o for o in conteneur.nourriture \
                    if o.prototype is prototype)
        if conteneur.est_de_type("conteneur"):
            return sum(nb for o, nb in conteneur.conteneur.iter_nombres() \
                    if o.prototype is prototype)
        raise ErreurExecution("{} n'est pas un conteneur".format(conteneur))
