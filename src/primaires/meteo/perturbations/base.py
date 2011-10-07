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


"""Ce fichier contient la classe BasePertu, détaillée plus bas."""

from math import sqrt, pow, ceil
from random import randint, choice
from collections import OrderedDict

from abstraits.id import ObjetID
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

class BasePertu(ObjetID, metaclass=MetaPertu):
    
    """Classe abstraite représentant la base d'une perturbation météo.
    Cette classe contient tout ce qui est commun à toutes les perturbations
    météorologiques.
    
    """
    
    groupe = "perturbations"
    sous_rep = "meteo/perturbations"
    nom_pertu = ""
    rayon_max = 0 # à redéfinir selon la perturbation
    duree_max = 15 # à peu près en minutes
    
    def __init__(self, pos):
        """Constructeur d'une perturbation météo"""
        ObjetID.__init__(self)
        self.centre = pos
        self.rayon = randint(ceil(self.rayon_max / 2), self.rayon_max)
        self.duree = randint(ceil(self.duree_max / 1.5), self.duree_max)
        self.age = 0
        self.flags = AUCUN_FLAG
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
    
    def __getnewargs__(self):
        return (None, )
    
    @property
    def liste_salles_sous(self):
        """Renvoie la liste des salles sous la perturbation"""
        ret = []
        for salle in type(self).importeur.salle._salles.values():
            if self.est_sur(salle):
                ret.append(salle)
        return ret
    
    def cycle(self):
        """Entame un nouveau cycle de la perturbation.
        Par défaut, elle se contente de bouger.
        
        """
        salles = self.liste_salles_sous
        self.action_cycle(salles)
        # Détection des collisions
        for pertu in type(self).importeur.meteo.perturbations_actuelles:
            if pertu is not self:
                if sqrt(pow(pertu.centre.x - self.centre.x, 2) + \
                        pow(pertu.centre.y - self.centre.y, 2)) <= \
                        self.rayon + pertu.rayon:
                    self.flags = self.flags ^ STATIQUE
        if not self.flags & STATIQUE:
            self.bouger(salles)
        self.age += 1
    
    def action_cycle(self, salles):
        """Définit une ou plusieurs actions effectuées à chaque cycle.
        Méthode à redéfinir pour des perturbations plus originales (l'orage
        par exemple qui tonne à chaque cycle aléatoirement).
        
        """
        pass
    
    def bouger(self, salles):
        """Bouge une perturbation"""
        x = 0
        if randint(1, 10) <= self.alea_dir:
            x = choice([-1, 1])
        if self.dir + x > 7 or self.dir + x < 0:
            x = (x == -1 and 7) or -7
        self.centre.x += vent_x[self.dir + x]
        self.centre.y += vent_y[self.dir + x]
        for salle in self.liste_salles_sous:
            if not salle in salles and salle.exterieur:
                salle.envoyer("|cy|" + self.message_entrer.format(
                        dir=vents_opp[self.dir]) + "|ff|")
        for salle in salles:
            if not self.est_sur(salle) and salle.exterieur:
                salle.envoyer("|cy|" + self.message_sortir.format(
                        dir=vents[self.dir]) + "|ff|")
        if randint(1, 10) <= self.alea_dir / 2:
            self.dir = randint(0, 7)
    
    def distance_au_centre(self, salle):
        """Retourne la distance de salle au centre de la perturbation"""
        x1 = salle.coords.x
        x2 = self.centre.x
        y1 = salle.coords.y
        y2 = self.centre.y
        return ceil(sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2)))
    
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

ObjetID.ajouter_groupe(BasePertu)
