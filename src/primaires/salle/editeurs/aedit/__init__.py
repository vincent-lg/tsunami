# -*-coding:Utf-8 -*

# Copyright (c) 2015 LE GOFF Vincent
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


"""Package contenant l'éditeur 'aedit'.

Si des redéfinitions de contexte-éditeur standard doivent être faites, elles
seront placées dans ce package

Note importante : ce package contient la définition d'un éditeur, mais
celui-ci peut très bien être étendu par d'autres modules. Au quel cas,
les extensions n'apparaîtront pas ici.

"""

from primaires.interpreteur.editeur.entier import Entier
from primaires.interpreteur.editeur.flag import Flag
from primaires.interpreteur.editeur.presentation import Presentation
from primaires.scripting.editeurs.edt_script import EdtScript

class EdtAedit(Presentation):

    """Classe définissant l'éditeur d'étendue 'aedit'."""

    nom = "aedit"

    def __init__(self, personnage, etendue):
        """Constructeur de l'éditeur"""
        if personnage:
            instance_connexion = personnage.instance_connexion
        else:
            instance_connexion = None

        Presentation.__init__(self, instance_connexion, etendue)
        if personnage and etendue:
            self.construire(etendue)

    def __getnewargs__(self):
        return (None, None)

    def construire(self, etendue):
        """Construction de l'éditeur"""
        # Altitude
        altitude = self.ajouter_choix("altitude", "a", Entier, etendue,
                "altitude", None, None)
        altitude.parent = self
        altitude.apercu = "{valeur}"
        altitude.prompt = "Entrez l'altitude de l'étendue : "
        altitude.aide_courte = \
            "Entrez |ent|l'altitude|ff| de l'étendue.\n\nL'altitude " \
            "correspond à la coordonnée Z de tout navire sur cette " \
            "étendue.\n\nAltitude actuelle : {valeur}"

        # Profondeur
        profondeur = self.ajouter_choix("profondeur", "p", Entier, etendue,
                "profondeur", None, None)
        profondeur.parent = self
        profondeur.apercu = "{valeur}"
        profondeur.prompt = "Entrez la profondeur de l'étendue : "
        profondeur.aide_courte = \
            "Entrez |ent|la profondeur|ff| de l'étendue.\n\nLa " \
            "profondeur, précisée en brasses, indique le tirant d'eau " \
            "maximum\nautorisé pour naviguer dans cette étendue, " \
            "ainsi que le fait de\npouvoir y jeter l'ancre.\n\nProfondeur " \
            "actuelle : {valeur}"

        # Eau douce
        douce = self.ajouter_choix("eau douce", "e", Flag, etendue,
                "eau_douce")
        douce.parent = self

        # Script
        scripts = self.ajouter_choix("scripts", "sc", EdtScript,
                etendue.script)
        scripts.parent = self

