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


"""Ce fichier contient la classe Roadmap, détaillée plus bas."""

from datetime import datetime

from abstraits.obase import BaseObj

class Roadmap(BaseObj):

    """Classe représentant un élément de la feuille de route (roadmap).

    La feuille de route est constituée d'éléments spécifiques,
    numérotés pour les administrateurs. Par exemple, une feuille
    de route pourrait contenr le nombre approximatif de salles
    en travaux, ou bien le nombre de quêtes disponibles à la
    prochaine ouverture. Si un joueur consulte la feuille de route,
    tous les éléments la contenant sont indiqués comme lus pour
    ce joueur. À chaque connexion, le joueur est informé de si des
    informations ont été modifiées sur la feuille de route.

    Notez que cette classe ne représente pas une feuille de route,
    mais bien les éléments constituant cette feuille de route. La
    feuille de route est constituée de l'ensemble des éléments
    actuels.


    """

    enregistrer = True
    no_actuel = 0

    def __init__(self, titre, texte):
        """Constructeur de la News Letter."""
        BaseObj.__init__(self)
        self.titre = titre
        self.texte = texte
        self.no = type(self).no_actuel + 1
        type(self).no_actuel += 1
        self.derniere_modification = datetime.now()
        self.joueurs_ayant_lu = []
        self._construire()

    def __getnewargs__(self):
        return ("aucun", "")

    def __repr__(self):
        return "<Roadmap {}>".format(repr(self.no))

    def mettre_a_jour(self, texte):
        """Met à jour l'avancement."""
        if self.titre:
            self.texte = texte
        else:
            self.titre = texte

        self.derniere_modification = datetime.now()
        self.joueurs_ayant_lu[:] = []
