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


"""Fichier contenant le paramètre 'voir' de la commande 'route'."""

from textwrap import wrap

from primaires.interpreteur.masque.parametre import Parametre

class PrmVoir(Parametre):

    """Commande 'route voir'."""

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "voir", "view")
        self.schema = "<nombre>"
        self.aide_courte = "affiche la route"
        self.aide_longue = \
            "Cette commande permet d'obtenir plus d'informations sur " \
            "une route. Vous devez préciser en paramètre le numéro " \
            "de la route, tel que spécifié dans %route% %route:liste%."

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        nombre = dic_masques["nombre"].nombre
        routes = list(importeur.route.routes.values())
        routes.sort(key=lambda t: t.ident)
        if nombre < 1 or nombre > len(routes):
            personnage << "|err|Cette route n'existe pas.|ff|"
            return

        route = routes[nombre - 1]
        description = route.description
        msg = "Description de la route {} :".format(nombre)
        msg += "\n  Origine de la route : {}".format(description.origine)
        destination = description.destination or "inconnue"
        msg += "\n  Destination de la route : {}".format(destination)
        msg += "\n  Salles de la route :"
        msg += "\n    " + "\n    ".join(wrap(
                description.afficher(ligne=True), 70))
        personnage << msg
