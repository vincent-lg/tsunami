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


"""Fichier contenant la classe Guilde, détaillée plus bas."""

from math import ceil

from abstraits.obase import BaseObj
from secondaires.crafting.exception import ExceptionCrafting
from secondaires.crafting.progression import Progression
from secondaires.crafting.rang import Rang, RangIntrouvable

class Guilde(BaseObj):

    """Classe représentant une guilde.

    Dans le crafting, une guilde est une organisation, artisanale
    ou politique. Les guildes politiques ne sont que des organisations
    et permettent souvent de progresser grâce à des quêtes. Les
    guildes artisanales sont plus complexes, car elles gèrent des
    matières premières, une notion d'approvisionnement et d'opérations
    usuelles. Le détail des différents types de guilde se trouve
    à l'adresse http://redmine.kassie.fr/issues/130 .

    """

    enregistrer = True

    def __init__(self, cle):
        """Constructeur de la fiche."""
        BaseObj.__init__(self)
        self.cle = cle
        self.nom = "une guilde"
        self.ouverte = False
        self.ateliers = []
        self.commandes = []
        self.talents = []
        self.types = []
        self.membres = {}
        self.rangs = []
        self._construire()

    def __getnewargs__(self):
        return ("", )

    def rejoindre(self, personnage):
        """Permet au personnage passé en paramètre de rejoindre la guilde.

        Cette méthode demande au personnage (joueur ou PNJ) passé
        en paramètre de rejoindre la guilde.

        Lève l'exception :
            GuildeSansRang si la guilde n'a aucun rang
            DejaMembre si le personnage est déjà membre de la guilde
            PointsGuildeInsuffisants si le membre manque de points de guilde

        """
        if len(self.rangs) == 0:
            raise GuildeSansRang("la guilde {} n'a aucun rang défini".format(
                    self.cle))

        if personnage in self.membres:
            raise DejaMembre("le personnage {} est déjà membre de " \
                    "la guilde {}".format(personnage, self.cle))

        rang = self.rangs[0]
        disponibles = importeur.crafting.get_points_guilde_disponibles(
                personnage)
        if disponibles < rang.points_guilde:
            raise PointsGuildeInsuffisants("le personnage {} n'a " \
                    "pas suffisamment de points de guilde ({} " \
                    "nécessaires contre {} disponibles)".format(
                    personnage, rang.points_guilde, disponibles))

        self.changer_rang(personnage, rang)

    def promouvoir(self, personnage):
        """Promeut un membre au rang suivant.

        Lève l'exception :
            GuildeSansRang si la guilde n'a aucun rang
            RangIntrouvable si le rang est introuvable
            NonMembre si le personnage n'est pas membre de la guilde
            PointsGuildeInsuffisants si le membre manque de points de guilde

        """
        if len(self.rangs) == 0:
            raise GuildeSansRang("la guilde {} n'a aucun rang défini".format(
                    self.cle))

        if personnage not in self.membres:
            raise NonMebre("le personnage {} n'est pas membre de " \
                    "la guilde {}".format(personnage, self.cle))

        progression = self.membres[personnage]
        rang = progression.rang

        # On cherche à identifier le rang suivant
        try:
            indice = self.rangs.index(rang)
        except ValueError:
            raise RangIntrouvable("le rang courant de {} dans la guilde " \
                    "{} est introuable".format(personnage, self.cle))

        try:
            suivant = self.rangs[indice + 1]
        except IndexError:
            raise RangIntrouvable("il n'y a pas de rang après {} " \
                    "dans la guilde {}".format(rang.cle, self.cle))

        disponibles = importeur.crafting.get_points_guilde_disponibles(
                personnage)
        if disponibles < suivant.points_guilde:
            raise PointsGuildeInsuffisants("le personnage {} n'a " \
                    "pas suffisamment de points de guilde ({} " \
                    "nécessaires contre {} disponibles)".format(
                    personnage, suivant.points_guilde, disponibles))

        self.changer_rang(personnage, suivant)

    def quitter(self, personnage):
        """Quitte la guilde.

        Lève l'exception :
            NonMembre si le personnage n'est pas membre de la guilde

        Déclare une partie des points de guilde récupérés en
        malus (5).

        """
        if personnage not in self.membres:
            raise NonMebre("le personnage {} n'est pas membre de " \
                    "la guilde {}".format(personnage, self.cle))

        progression = self.membres[personnage]
        points = progression.rang.total_points_guilde
        del self.membres[personnage]
        progressions = [p for p in importeur.crafting.membres.membres[
                personnage] if p.rang.guilde is not self]
        importeur.crafting.membres.membres[personnage] = progressions

        # Écriture du malus
        malus = ceil(points * 5 / 100)
        malus += importeur.crafting.membres.malus.get(personnage, 0)
        importeur.crafting.membres.malus[personnage] = malus

    def changer_rang(self, personnage, rang):
        """Change le rang du personnage précisé.

        À la différence des méthodes 'rejoindre', 'quitter', ou
        'promouvoir', cette méthode ne fait aucune vérification.

        """
        progression = Progression(personnage, rang)
        self.membres[personnage] = progression
        progressions = importeur.crafting.membres.membres.get(personnage, [])
        progressions = [p for p in progressions if p.rang.guilde is not self]
        progressions.append(progression)
        importeur.crafting.membres.membres[personnage] = progressions

    def ajouter_rang(self, cle):
        """Ajoute le rang indiqué."""
        rang = Rang(self, cle)
        self.rangs.append(rang)
        return rang


class GuildeSansRang(ExceptionCrafting):

    """Exception levée quand la guilde n'a aucun rang défini."""

    pass

class DejaMembre(ExceptionCrafting):

    """Exception levée quand le personnage est déjà membre de la guilde."""

    pass

class NonMembre(ExceptionCrafting):

    """Exception levée quand le personnage n'est pas membre de la guilde."""

    pass

class PointsGuildeInsuffisants(ExceptionCrafting):

    """Exception levée quand l'opération attendue attend trop de points.

    Les opérations consommant des points de guilde sont le fait
    de rejoindre une guilde ou de changer de rang.

    """

    pass
