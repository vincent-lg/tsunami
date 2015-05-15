# -*-coding:Utf-8 -*

# Copyright (c) 2010 LE GOFF Vincent
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


"""Package contenant l'éditeur 'zedit'.
Si des redéfinitions de contexte-éditeur standard doivent être faites, elles
seront placées dans ce package

Note importante : ce package contient la définition d'un éditeur, mais
celui-ci peut très bien être étendu par d'autres modules. Au quel cas,
les extensions n'apparaîtront pas ici.

"""

from primaires.interpreteur.editeur.presentation import Presentation
from primaires.interpreteur.editeur.flag import Flag
from primaires.interpreteur.editeur.entier import Entier

class EdtZedit(Presentation):

    """Classe définissant l'éditeur de zone 'zedit'.

    """

    nom = "zedit"

    def __init__(self, personnage, zone):
        """Constructeur de l'éditeur"""
        if personnage:
            instance_connexion = personnage.instance_connexion
        else:
            instance_connexion = None

        Presentation.__init__(self, instance_connexion, zone)
        if personnage and zone:
            self.construire(zone)

    def __getnewargs__(self):
        return (None, None)

    def construire(self, zone):
        """Construction de l'éditeur"""
        # Ouverte / fermée
        ouverte = self.ajouter_choix("ouverte", "o", Flag, zone,
                "ouverte")
        ouverte.parent = self

        # Trésor
        tresor = self.ajouter_choix("tresor", "t", Entier, zone,
                "argent_total")
        tresor.parent = self
        tresor.apercu = "{objet.argent_total}"
        tresor.prompt = "Entrez le trésor de la zone : "
        tresor.aide_courte = \
            "Entrez |ent|le trésor|ff| de la zone.\n\nTrésor actuel : " \
            "{objet.argent_total}"


        # Température
        temperature = self.ajouter_choix("modificateur de température", "m",
                Entier, zone, "mod_temperature", None, None)
        temperature.parent = self
        temperature.apercu = "{valeur}°"
        temperature.prompt = "Entrez le modificateur de la température " \
                "de la zone : "
        temperature.aide_courte = \
            "Entrez |ent|le modificateur de température|ff| de la " \
            "zone en degrés\nou |ent|/|ff| pour revenir à la fenêtre " \
            "parente.\n\nLe modificateur de la température influence " \
            "la température qui règne\ndans la zone. Si vous choisissez " \
            "un modificateur de |ent|-10|ff| par\nexemple, et qu'il " \
            "fait 20° dans l'univers, alors il n'en fera que 10\ndans " \
            "la zone modifiée. Ce système influence directement la " \
            "météo, car\nune zone avec des températures élevées n'aura " \
            "jamais de neige, alors\nqu'une zone tout le temps froide " \
            "en aura constamment.\n\nModificateur de température " \
            "actuel : {valeur}°"
