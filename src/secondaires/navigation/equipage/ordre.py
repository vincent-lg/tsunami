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
from secondaires.navigation.equipage.signaux import *

ordres = {}

class MetaOrdre(MetaBaseObj):

    """Métaclasse des ordres.

    Elle ajoute l'ordre dans le dictionnaire 'ordres' si il possède
    une clé.

    """

    etats_autorises = ("", )
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
    etats_autorises = ("", )
    peut_deleguer = True
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
        self.volonte = None
        self.invalide = False
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

    def executer(self):
        """Exécute l'ordre.

        Cette méthode est appelée pour commencer seulement à exécuter un ordre.
        La plupart des ordres mettent plusieurs secondes pour le moins à s'exécuter.
        Cette méthode n'est que le déclencheur.

        """
        raise NotImplementedError

    # Méthodes utilisées par des sous-ordres
    def relayer_si_fatigue(self, endurance_min):
        """Relaye l'ordre si le matelot est trop fatigué."""
        matelot = self.matelot
        personnage = matelot.personnage
        if personnage.stats.endurance < endurance_min:
            return SignalRelais("{} est trop fatigué".format(personnage))

        return None

    # Méthodes de manipulation d'un personnage
    def jeter_ou_entreposer(self, exception):
        """Jète les objets tenus ou les met en cale.

        Si l'objet tenu peut être mis en cale, il est entreposé. Sinon
        il est jeté.

        Cette méthode ne fait quelque chose que si le personnage n'a
        aucune main libre.

        """
        personnage = self.matelot.personnage
        navire = self.navire
        cale = navire.cale
        if personnage.nb_mains_libres > 0:
            return

        for objet in list(personnage.equipement.tenus):
            if personnage.nb_mains_libres > 0:
                return

            if objet.nom_type != exception:
                detruire = False
                personnage.equipement.tenus.retirer(objet)
                if objet.nom_type in cale.types:
                    try:
                        cale.ajouter_objets([objet])
                    except ValueError:
                        detruire = True
                else:
                    detruire = True

                if detruire:
                    importeur.objet.supprimer_objet(objet.identifiant)
