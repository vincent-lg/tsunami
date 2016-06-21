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


"""Fichier contenant la classe Banc définissant un banc de poisson."""

from abstraits.obase import BaseObj

class Banc(BaseObj):

    """Classe représentant un banc de poisson.

    Un banc possède :
        cle -- une clé identifiante
        etendue -- une étendue utilisant ce banc (optionnel)
        salles -- une liste de salles utilisant ce banc (optionnel)
        abondance_max -- l'abondance maximum (entre en Kg / heure
        abondance_actuelle -- l'abondance actuelle du banc (entre 1 et max
        poissons -- un dictionnaire représentant les poissons à pêcher {1]

    [1] Le dictionnaire des poissons à pêcher est sous la forme :
    {
        prototype_poisson1: probabilite,
        prototype_poisson2: probabilite,
        ...
    }
    La probabilité totale n'est pas 100 mais la somme de la probabilité
    de tous les poissons. Par exemple, si un banc défini des carpes en
    probabilité 5 et des truites en probabilité 1, un joueur pêchant
    dans ce banc aura une chance sur six de pêcher une truite.

    """

    enregistrer = True

    def __init__(self, cle, modele=None):
        """Constructeur du banc.

        La clé identifiante doit être précisée en paramètre.

        On peut également préciser en paramètre un modèle pour le cloner.
        Les informations dans le modèle seront prises comme base pour
        définir le banc.

        """
        BaseObj.__init__(self)
        self.cle = cle
        self.etendue = None
        self.salles = []
        self._abondance_max = 100
        self.abondance_actuelle = 100
        self.poissons = {}
        if modele:
            self.poissons = dict(modele.poissons)
        self._construire()

    def __getnewargs__(self):
        return ("", )

    def __repr__(self):
        """Affichage de debug."""
        return "<banc {} {}/{} ({}%)>".format(repr(
                self.cle), self.abondance_actuelle, self._abondance_max,
                int(self.abondance_actuelle / self._abondance_max * 100))

    def __str__(self):
        return self.cle

    def _get_abondance_max(self):
        return self._abondance_max
    def _set_abondance_max(self, abondance_max):
        self._abondance_max = abondance_max
        self.abondance_actuelle = abondance_max
    abondance_max = property(_get_abondance_max, _set_abondance_max)

    @property
    def aff_etendue(self):
        return self.etendue and self.etendue.cle or "aucune"

    def pecher(self, poisson):
        """Pêche le poisson indiqué."""
        self.abondance_actuelle -= poisson.poids

    def tick(self):
        """Tick qui doit être appelé toute les minutes."""
        if self.abondance_actuelle < self.abondance_max:
            plus = int(self.abondance_max / 60)
            if plus == 0:
                plus = 1
            self.abondance_actuelle += plus

        if self.abondance_actuelle > self.abondance_max:
            self.abondance_actuelle = self.abondance_max
