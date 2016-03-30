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


"""Ce fichier contient la classe BasePertu, détaillée plus bas."""

from vector import mag

from math import sqrt, pow, ceil
from random import randint, choice
from collections import OrderedDict

from abstraits.obase import BaseObj
from . import MetaPertu
from primaires.salle.coordonnees import Coordonnees

vent_x = [0, 1, 1, 1, 0, -1, -1, -1]
vent_y = [1, 1, 0, -1, -1, -1, 0, 1]
vents = ["le nord", "le nord-est", "l'est", "le sud-est",
    "le sud", "le sud-ouest", "l'ouest", "le nord-ouest"]
vents_opp = ["du sud", "du sud-ouest", "de l'ouest", "du nord-ouest",
    "du nord", "du nord-est", "de l'est", "du sud-est"]

AUCUN_FLAG = 0
STATIQUE = 1
OPAQUE = 2

class BasePertu(BaseObj, metaclass=MetaPertu):

    """Classe abstraite représentant la base d'une perturbation météo.

    Cette classe contient tout ce qui est commun à toutes les perturbations
    météorologiques.

    """

    nom_pertu = ""
    rayon_max = 0 # à redéfinir selon la perturbation
    duree_max = 15 # à peu près en minutes
    temperature_min = None
    temperature_max = None
    origine = True

    enregistrer = True
    def __init__(self, pos):
        """Constructeur d'une perturbation météo"""
        BaseObj.__init__(self)
        self.centre = pos
        self.rayon = randint(ceil(self.rayon_max / 2), self.rayon_max)
        self.duree = randint(ceil(self.duree_max / 1.5), self.duree_max)
        self.age = 0
        self.flags = AUCUN_FLAG
        self.statique = False
        self.dir = randint(0, 7)
        # 0 pour une perturbation en ligne droite, 1 pour aucun changement
        # majeur de direction, jusqu'à 10 pour un comportement aléatoire
        self.alea_dir = 1
        # (X, état renvoyé) avec X par rapport à 10 la fraction du rayon
        # concernée, en partant du centre
        self.etat = [
            (7, "Une perturbation roule au-dessus de votre tête."),
            (10, "Une perturbation gronde non loin."),
        ]
        # Messages renvoyés aux salles sous la perturbation
        self.message_debut = "Une perturbation se forme dans le ciel."
        self.message_fin = "La perturbation se dissipe peu à peu."
        # Message à une salle sur laquelle arrive la perturbation
        self.message_entrer = "Une perturbation arrive {dir}."
        # Message à une salle qui sort de la perturbation
        self.message_sortir = "La perturbation s'éloigne et disparaît au loin."
        # Liste des fins possibles d'une pertu enchaînant sur une autre
        # ("nom d'une pertu", "message d'enchaînement", proba)
        # Le choix d'une pertu est fait aléatoirement en tirant un nombre
        # entre 1 et 100 ; la première perturbation de la liste telle que
        # nombre_tire < proba est choisie (voir nuages pour un exemple).
        self.fins_possibles = []
        self._construire()

    def __getnewargs__(self):
        return (None, )

    def __repr__(self):
        """Représentation de la perturbation."""
        return "<{} ({}>)".format(self.nom_pertu, repr(self.centre))

    @property
    def liste_salles_sous(self):
        """Renvoie la liste des salles sous la perturbation"""
        ret = []
        for salle in importeur.salle._coords.values():
            if self.est_sur(salle):
                ret.append(salle)
        return ret

    def est_opaque(self):
        """Retourne True si on peut voir le ciel, False sinon."""
        return self.flags & OPAQUE != 0

    # Messages
    def envoyer_message_debut(self, salles=None, exceptions=None):
        """Envoie le message de début de la perturbation.

        Si les salles ne sont pas précisées, calcule les salles
        sous la perturbation actuelle.

        """
        exceptions = exceptions or []
        if salles is None:
            salles = self.liste_salles_sous

        for salle in salles:
            if salle in exceptions:
                continue

            if not salle.exterieur:
                continue

            importeur.meteo.salles[salle] = self
            salle.envoyer("|cy|" + self.message_debut + "|ff|",
                    prompt=False)

    def envoyer_message_entre(self, salles, exceptions=None):
        """Envoie le message quand la perturbation entre sur une salle."""
        exceptions = exceptions or []
        for salle in salles:
            if salle in exceptions:
                continue

            if not salle.exterieur:
                continue

            importeur.meteo.salles[salle] = self
            salle.envoyer("|cy|" + self.message_entrer.format(
                    dir=vents_opp[self.dir]) + "|ff|", prompt=False)

    def envoyer_message_sort(self, salles, exceptions=None):
        """Envoie le message quand la perturbation quitte une salle."""
        exceptions = exceptions or []
        for salle in salles:
            if salle in exceptions:
                continue

            if not salle.exterieur:
                continue

            importeur.meteo.salles[salle] = None
            salle.envoyer("|cy|" + self.message_sortir.format(
                    dir=vents[self.dir]) + "|ff|", prompt=False)

    def envoyer_message_transition(self, salles=None, message=""):
        """Envoie du message de transition."""
        if salles is None:
            salles = self.liste_salles_sous

        for salle in salles:
            if salle.exterieur:
                importeur.meteo.salles[salle] = self
                salle.envoyer("|cy|" + message + "|ff|",
                        prompt=False)

    def envoyer_message_fin(self, salles=None):
        """Envoie le message de fin de la perturbation.

        Les salles peuvent être précisées pour l'optimisation. Si
        elles ne le sont pas, les salles sous la perturbation sont
        sélectionnées.

        """
        if salles is None:
            salles = self.liste_salles_sous

        for salle in salles:
            if salle.exterieur:
                importeur.meteo.salles[salle] = None
                salle.envoyer("|cy|" + self.message_fin + "|ff|",
                        prompt=False)

    def tick(self):
        """Tick la perturbation à chaque minute.

        Si nécessaire, transforme la perturbation en une autre.
        Cette méthode appelle également les actions du cycle (qui
        font bouger la perturbation).

        """
        sous = self.liste_salles_sous
        if self.age >= self.duree:
            i = randint(0, 100)
            nom_pertu_enchainer = ""
            msg_enchainement = ""
            for fin in self.fins_possibles:
                if i <= fin[2]:
                    nom_pertu_enchainer = fin[0]
                    msg_enchainement = fin[1]
                    break

            if not nom_pertu_enchainer:
                self.envoyer_message_fin(sous)
            else:
                cls_pertu_enchainer = None
                for pertu_existante in importeur.meteo.perturbations:
                    if pertu_existante.nom_pertu == nom_pertu_enchainer:
                        cls_pertu_enchainer = pertu_existante
                        break

                if cls_pertu_enchainer:
                    pertu_enchainer = cls_pertu_enchainer(self.centre)
                    pertu_enchainer.rayon = self.rayon
                    pertu_enchainer.dir = self.dir
                    # Donne le message de transition
                    pertu_enchainer.envoyer_message_transition(sous,
                            msg_enchainement)
                    importeur.meteo.perturbations_actuelles.append(
                            pertu_enchainer)
            self.detruire()
            importeur.meteo.perturbations_actuelles.remove(self)
            return

        # On fait bouger les perturbations existantes
        self.cycle(sous)

    def cycle(self, salles=None):
        """Entame un nouveau cycle de la perturbation.

        Par défaut, elle se contente de bouger.

        """
        if salles is None:
            salles = self.liste_salles_sous

        self.action_cycle(salles)
        n_x, n_y = self.calculer_prochaines_coords()

        # Détection des collisions
        if self.flags & STATIQUE:
            self.flags = self.flags ^ STATIQUE

        for pertu in importeur.meteo.perturbations_actuelles:
            if pertu is not self and self.va_recouvrir(pertu, n_x, n_y):
                self.flags = self.flags ^ STATIQUE

        if not self.flags & STATIQUE and not self.statique:
            self.bouger(salles, n_x, n_y)

        self.age += 1

    def action_cycle(self, salles):
        """Définit une ou plusieurs actions effectuées à chaque cycle.

        Méthode à redéfinir pour des perturbations plus originales (l'orage
        par exemple qui tonne à chaque cycle aléatoirement).

        """
        pass

    def bouger(self, salles, n_x, n_y):
        """Bouge une perturbation.

        Paramètres de cette méthode :
            salles -- les salles sous la perturbation AVANT qu'elle ne bouge
            n_x -- la nouvelle coordonnée X
            n_y -- la nouvelle coordonnée Y

        """
        self.centre.x = n_x
        self.centre.y = n_y
        nouvelles = self.liste_salles_sous

        for salle in nouvelles:
            if salle not in salles:
                temperature = salle.zone.temperature
                if (self.temperature_min and temperature < \
                        self.temperature_min) or (self.temperature_max and \
                        temperature > self.temperature_max):
                    self.envoyer_message_fin(salles)
                    self.detruire()
                    importeur.meteo.perturbations_actuelles.remove(self)
                    break

        # Envoie du message de déplacement
        if self.e_existe:
            self.envoyer_message_sort(salles, nouvelles)
            self.envoyer_message_entre(nouvelles, salles)

        if randint(1, 10) <= self.alea_dir / 2:
            self.dir = randint(0, 7)

    def distance_au_centre(self, salle):
        """Retourne la distance de salle au centre de la perturbation"""
        x1 = salle.coords.x
        x2 = self.centre.x
        y1 = salle.coords.y
        y2 = self.centre.y
        return ceil(mag(x1, y1, 0, x2, y2, 0))

    def est_sur(self, salle):
        """Retourne True si salle est au-dessous de la perturbation"""
        return self.distance_au_centre(salle) <= self.rayon

    def message_pour(self, salle):
        """Retourne le message correspondant à la salle"""
        msg = ""
        for etat in self.etat:
            if self.distance_au_centre(salle) / self.rayon <= etat[0] / 10:
                msg = etat[1]
                break
        return msg

    @classmethod
    def accepte_temperature(cls, temperature):
        """Retourne True si accepte la température, False sinon.

        NOTE: une perturbation accepte une température donnée si
        elle est dans ses bornes de températures minimum et maximum.
        Bien entendu, si ces bornes n'existent pas (restent à None),
        cela n'a pas d'importance et la méthode retournera True.

        """
        if cls.temperature_min and cls.temperature_min > temperature:
            return False
        if cls.temperature_max and cls.temperature_max < temperature:
            return False

        return True

    def calculer_prochaines_coords(self):
        """Retourn les prochains (x, y)."""
        n_x = n_y = 0
        x = 0
        if randint(1, 10) <= self.alea_dir:
            x = choice([-1, 1])
        if self.dir + x > 7 or self.dir + x < 0:
            x = (x == -1 and 7) or -7
        n_x = self.centre.x + vent_x[self.dir + x]
        n_y = self.centre.y + vent_y[self.dir + x]
        return n_x, n_y

    def va_recouvrir(self, pertu, n_x=None, n_y=None):
        """Retourne True si le prochain mouvement de self va recouvrir pertu."""
        if n_x is None or n_y is None:
            n_x = self.centre.x
            n_y = self.centre.y

        return sqrt((pertu.centre.x - n_x) ** 2 + (pertu.centre.y - n_y) ** 2) <= \
                self.rayon + pertu.rayon
