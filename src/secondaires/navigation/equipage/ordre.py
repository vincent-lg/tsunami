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


"""Fichier contenant la classe Ordre et ses exceptions."""

from abstraits.obase import BaseObj, MetaBaseObj
from bases.exceptions.base import ExceptionMUD
from secondaires.navigation.equipage.generateur import GenerateurOrdre

ordres = {}

class MetaOrdre(MetaBaseObj):

    """Métaclasse des ordres.

    Elle ajoute l'ordre dans le dictionnaire 'ordres' si il possède
    une clé.

    """

    def __init__(cls, nom, bases, contenu):
        """Constructeur de la métaclasse"""
        MetaBaseObj.__init__(cls, nom, bases, contenu)
        if cls.cle:
            ordres[cls.cle] = cls

class Ordre(BaseObj, metaclass=MetaOrdre):

    """Classe représentant un ordre.

    Attributs définis :
        matelot -- le matelot accomplissant l'ordre

    Méthodes définies :
        choisir_personnage -- choisit un personnage pour cet ordre
        calculer_empechement -- retourne l'empêchement calculé du mtelot
        executer -- commence l'exécution de l'ordre

    """

    id_actuel = 1
    cle = ""
    logger = type(importeur).man_logs.get_logger("ordres")
    def __init__(self, matelot, navire):
        """Construit un ordre.

        Si le navire existe et qu'aucun matelot n'a été trouvé pour cet ordre,
        recherche le meilleur matelot.

        """
        BaseObj.__init__(self)
        self.matelot = matelot
        self.navire = navire
        self.id = Ordre.id_actuel
        Ordre.id_actuel += 1
        self.priorite = 1
        self.suite = None
        if self.matelot is None and navire:
            matelots = navire.matelots
            self.matelot = self.choisir_matelot(matelots)

    def __getnewargs__(self):
        return (None, None, )

    def __repr__(self):
        return "<ordre '{}({})' pour {}".format(self.cle, self.id,
                self.cle_matelot)

    @property
    def cle_matelot(self):
        return self.matelot and self.matelot.identifiant or "inconnue"

    def creer_generateur(self):
        """Crée un générateur spécifique pour cet ordre."""
        generateur = self.executer()
        generateur_ordre = GenerateurOrdre(self, generateur)
        return generateur_ordre

    def choisir_matelot(self, matelots):
        """Retourne le meilleur matelot pour cet ordre.

        Cette méthode prend en paramètre la liste des matelots disponibles.
        Un d'entre eux doit être choisi sur des critères propres à l'ordre.

        """
        raise NotImplementedError

    def calculer_empechement(self):
        """Retourne une estimation de l'empêchement du matelot.

        Cet empêchement doit être entre 0 et 100 (0 pas du tout empêché,
        100 gravement empêché). Cet empêchement est confronté à la priorité
        de l'ordre.

        """
        return 0

    def executer(self):
        """Exécute l'ordre.

        Cette méthode est appelée pour commencer seulement à exécuter un ordre.
        La plupart des ordres mettent plusieurs secondes pour le moins à s'exécuter.
        Cette méthode n'est que le déclencheur.

        """
        raise NotImplementedError


class ExceptionOrdre(ExceptionMUD):

    """Exception spécifique à un ordre."""

    pass

class PrioriteTropFaible(ExceptionOrdre):

    """Exception levée quand la priorité de l'ordre est trop faible."""

    pass

class OrdreDiffere(ExceptionOrdre):

    """Exception levée quand l'ordre doit être différé.

    On attend en paramètre :
        L'ordre
        Le message (d'excuse)
        Le temps estimé pour la mise en attente de l'ordre (en secondes).

    Il s'agit ensuite pour l'intelligence minimale d'annuler l'ordre en
    utilisant un autre matelot ou d'attendre.

    """

    def __init__(self, ordre, message, temps):
        self.ordre = ordre
        self.message = message
        self.temps = temps

    def __str__(self):
        return self.message + " (" + str(self.temps) + "s)"

    @property
    def priorite(self):
        return self.ordre.differe + temps

class OrdreEmpeche(ExceptionOrdre):

    """Exception levée quand un ordre est impossible de part les circonstances."""

    pass

class OrdreSansSubstitution(ExceptionOrdre):

    """Exception appelée si on cherche un matelot de substitution.

    Tous les ordres n'acceptent pas de choisir des matelots de substitution.
    Certains ordres sont faits pour UN matelot et ne doivent pas en choisir
    de substitution.

    """
