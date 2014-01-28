# -*-coding:Utf-8 -*

# Copyright (c) 2012 NOEL-BARON Léo
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


"""Fichier contenant la classe Feu, détaillée plus bas."""

from random import randint, choice, random

from abstraits.obase import BaseObj
from corps.fonctions import lisser
from primaires.perso.exceptions.stat import *

class Feu(BaseObj):

    """Classe représentant une feu.

    Un feu est, aussi simplement que son nom l'indique, un feu de camp, un
    incendie ou autre. Il est caractérisé par une salle parente, et une
    puissance entre 1 et 100 dont dépendent sa durée de vie et une propension
    à se propager. Les feux sont gérés par le module salle via une action
    différée qui permet leur évolution dans le temps.

    Un feu peut en outre être allumé, puis alimenté via deux commandes.

    """

    _nom = "feu"
    enregistrer = True

    def __init__(self, salle, puissance=10):
        """Constructeur d'un feu"""
        BaseObj.__init__(self)
        self._puissance = puissance if puissance <= 100 else 100
        self.salle = salle
        self.stabilite = 0
        self.generation = 0
        self.tour = 0

    def __getnewargs__(self):
        return (None, )

    def __str__(self):
        """Méthode d'affichage du feu (fonction de la puissance)"""
        cheminee = None
        msg_cheminee = (
            (1, "{cheminee} ne contient qu'un tas de cendres encore chaudes."),
            (5, "{cheminee} contient encore quelques flammes vascillantes."),
            (8, "Quelques flammes encore vives brûlent dans {cheminee}."),
            (15, "Un feu clair crépite gaiement au coeur de {cheminee}."),
            (25, "De hautes flammes dansent au coeur de {cheminee}."),
            (40, "Un feu trop ardent emplit littéralement {cheminee}."),
            (55, "Un début d'incendie menace, envahissant peu à peu les lieux."),
            (70, "Un brasier enthousiaste flamboie ici et vous roussit le " \
                    "poil."),
            (85, "Une fournaise étouffante vous prend à la gorge et menace " \
                    "de vous consummer."),
            (100, "Un véritable bûcher se dresse tout autour de vous, " \
                    "sans espoir de survie."),
        )

        for detail in self.salle.details:
            if detail.a_flag("cheminée"):
                messages = msg_cheminee
                cheminee = detail

        if cheminee is None:
            cfg_salle = importeur.anaconf.get_config("salle")
            messages = cfg_salle.messages_feu

        for puissance_max, msg in messages:
            if self.puissance <= puissance_max:
                retenu = msg
                break

        if cheminee:
            retenu = lisser(retenu.format(cheminee=cheminee.titre))
            retenu = retenu.capitalize()

        return retenu

    def _set_puissance(self, valeur):
        if valeur >= 100:
            self._puissance = 100
        elif valeur <= 0:
            self._puissance = 0
        else:
            self._puissance = valeur
    def _get_puissance(self):
        return self._puissance
    puissance = property(_get_puissance, _set_puissance)

    def bruler(self):
        """Méthode d'action de base du feu"""
        self.tour = 0 if self.tour == 5 else self.tour + 1
        messages_standard = [
            "Une bûche cède soudain dans un grand craquement.",
            "Quelques étincelles s'envolent vers le ciel.",
            "Le feu redouble d'ardeur et les flammes montent brusquement.",
            "Un crépitement sec retentit.",
            "Une ou deux flammes tentent de s'échapper du foyer.",
            "Les flammes dansent sous un léger coup de vent.",
            "Le feu vascille, hésite et reprend de plus belle.",
            "Les flammes montent à l'assaut d'un nouveau bout de bois.",
            "Une langue de feu s'échappe vers le ciel dans un souffle.",
            "Une branche un peu verte proteste bruyamment.",
            "Un noeud dans le bois éclate en une pluie d'étincelle.",
            "Une brusque rafale de vent couche les flammes un instant.",
        ]
        messages_fin = [
            "Le feu crachote comme un vieillard malade.",
            "Quelques flammes faiblardes tentent de s'extirper de la cendre.",
            "Les flammes se ravivent un instant, puis retombent, vaincues.",
        ]
        if not importeur.salle.peut_allumer_feu(self.salle):
            self.puissance = 1

        if random() < self.stabilite and self.tour == 5:
            if self.puissance <= 5:
                self.salle.envoyer("Le feu s'éteint sans crier gare, à la " \
                        "faveur d'un souffle d'air.", prompt=False)
                importeur.salle.eteindre_feu(self.salle)
                return
            elif self.puissance <= 40:
                # Entre 5 et 40, on laisse osciller un peu la puissance
                if random() < 0.44:
                    self.puissance += randint(-1, 1)
            else:
                self.puissance += randint(0, 2)
                self.propager()

        # Cas standard, sans tenir compte de l'instabilité
        if self.puissance == 1:
            if random() < 0.20:
                self.salle.envoyer("Un petit nuage de cendres annonce la " \
                        "mort définitive du feu.", prompt=False)
                importeur.salle.eteindre_feu(self.salle)
        elif self.salle.interieur and self.puissance <= 40:
            return
        elif self.puissance <= 5:
            self.salle.envoyer(choice(messages_fin), prompt=False)
            # On rend le feu instable
            if self.tour == 5:
                self.stabilite += 1 - self.puissance / 5
                self.puissance -= 1
        elif self.puissance <= 40:
            if random() < 0.67:
                self.salle.envoyer(choice(messages_standard), prompt=False)
            if self.tour == 5:
                self.puissance -= 1
        else:
            # Cas de l'incendie
            for personnage in self.salle.personnages:
                dommages = int(0.1 * personnage.vitalite_max)
                personnage << "Le feu vous brûle la couenne."
                try:
                    personnage.vitalite = personnage.vitalite - dommages
                except DepassementStat:
                    personnage << "Vous rendez l'âme dans le brasier."
                    personnage.mourir()
            if self.tour == 5:
                self.stabilite = self.puissance / 200
                self.puissance -= 1

    def propager(self):
        """Méthode de propagation.

        Un feu est maîtrisé jusqu'à une puissance de 40 ; au-delà la
        probabilité qu'il gonfle spontanément et se propage est multipliée.
        Un feu se propage de proche en proche en perdant 10 de puissance à
        chaque fois, mais rien n'empêche qu'il reprenne de la puissance une
        fois installé dans la salle de destination, et ainsi de suite en
        fonction de la météo et d'autres conditions.

        Il faudra alors avoir certains talents et faire certaines actions
        (par exemple verser de l'eau) pour endiguer un incendie.

        """
        if self.generation >= 5:
            return
        perturbation = None
        pertus = [p for p in importeur.meteo.perturbations_actuelles \
                if p.est_sur(self.salle)]
        if pertus:
            perturbation = pertus[0]
        # Pas de propagation possible en cas d'orage ou de pluie
        if perturbation and perturbation.nom_pertu in ("pluie", "orage"):
            return
        if perturbation and perturbation.nom_pertu == "vent":
            coef_puissance = 0
        else:
            coef_puissance = 10
        salles = [s.salle_dest for s in self.salle.sorties]
        salles = [s for s in salles if importeur.salle.peut_allumer_feu(s)]
        if not salles:
            return

        salle_fils = choice(salles)
        if salle_fils.ident in importeur.salle.feux:
            feu_fils = importeur.salle.feux[salle_fils.ident]
        else:
            feu_fils = importeur.salle.allumer_feu(salle_fils)
        feu_fils.puissance = self.puissance - coef_puissance
        feu_fils.generation = self.generation + 1
        salle_fils.envoyer("Un incendie se déclare tout à coup.", prompt=False)

    @classmethod
    def repop(cls):
        """Méthode de repop des feux ; boucle sur les feux en déclenchant
        leur méthode bruler.

        """
        for feu in list(importeur.salle.feux.values()):
            feu.bruler()
        importeur.diffact.ajouter_action("repop_feux", 9, cls.repop)
