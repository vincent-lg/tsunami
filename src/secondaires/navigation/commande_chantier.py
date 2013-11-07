# -*-coding:Utf-8 -*

# Copyright (c) 2013 LE GOFF Vincent
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


"""Fichier contenant la classe CommandeChantierNaval, détaillée plus bas."""

from datetime import datetime, timedelta
from math import radians

from vector import *

from abstraits.obase import BaseObj
from bases.exceptions.base import ExceptionMUD
from corps.fonctions import lisser


class CommandeChantierNaval(BaseObj):

    """Classe décrivant une commande dans un chantier naval.

    Une commande est une opération "à faire" dans le chantier spécifié. Par
    exemple : le joueur X veut acheter un navire Y (mais l'achat du navire
    n'est pas instantanée, il faut le construire, ce qui prend plus ou moins
    de temps en fonction de la classe du navire).

    """

    def __init__(self, chantier, instigateur, navire, nom_type, duree, *args):
        """Constructeur d'une commande.

        Notez qu'il est préférable de passer par la méthode 'ajouter_commande' de ChantierNaval.

        Les paramètres à préciser sont :
            chantier -- le chantier naval (parent)
            instigateur -- le personnage ordonnant la commande
            navire -- le navire traité
            nom_type -- le type de commande
            duree -- la durée (en minutes) de la commande
            args -- des arguments supplémentaires en fonction du type

        """
        BaseObj.__init__(self)
        self.chantier = chantier
        self.instigateur = instigateur
        self.navire = navire
        self.nom_type = nom_type
        self.duree = duree
        self.arguments = args
        self.date_debut = datetime.now()
        self._construire()

    def __getnewargs__(self):
        return (None, None, None, "inconnu", 0, )

    def __repr__(self):
        return "<CommandeChantierNaval {} pour {}>".format(
                repr(self.nom_type), self.instigateur)

    @property
    def date_fin(self):
        """Retourne la date de fin (date de début + duree projetée)."""
        delta = timedelta(seconds=self.duree * 60)
        return self.date_debut + delta

    @property
    def a_faire(self):
        """Retourne True si la commande est à faire maintenant, False sinon."""
        return datetime.now() >= self.date_fin

    @property
    def duree_restante(self):
        """Retourne la durée restante sous la forme d'une chaîne."""
        if self.a_faire:
            return "moins d'une minute"

        delta = self.date_fin - datetime.now()
        secondes = delta.total_seconds()
        if secondes < 60:
            return "moins d'une minute"
        elif secondes < 3600:
            nb = secondes // 60
            unite = "minute"
        elif secondes < 24 * 3600:
            nb = secondes // 3600
            unite = "heure"
        else:
            nb = secondes // (3600 * 24)
            unite = "jour"

        s = "s" if nb > 1 else ""
        return "{} {}{s}".format(int(nb), unite, s=s)

    def executer(self):
        """Exécute la commande.

        En fonction du type on appelle une méthode différente.

        """
        nom_type = self.nom_type
        methode = "cmd_" + nom_type
        if not callable(getattr(self, methode, None)):
            raise ValueError("le type de commande {} est invalide".format(
                    repr(nom_type)))

        getattr(self, methode)()

    def get_nom(self):
        """Retourne le nom correspondant au type."""
        return getattr(self, "nom_" + self.nom_type)()

    # Noms de type
    def nom_acheter(self):
        """Retourne le nom quand un navire est en cours d'achat."""
        modele = importeur.navigation.modeles[self.arguments[0]]
        return lisser("Achat de " + modele.nom)

    def nom_renommer(self):
        """Retourne le nom de la commande quand on renomme un navire."""
        navire = self.navire
        return lisser("Changement de nom de " + navire.nom)

    # Types de commande
    def cmd_acheter(self):
        """Achète un navire."""
        cle_modele = self.arguments[0]
        modele = importeur.navigation.modeles[cle_modele]

        # On cherche un emplacement disponible dans le bassin
        point = None
        points = self.chantier.points
        for x, y, z in points:
            vecteur = Vector(x, y, z)
            vecteurs = []
            invalide = False
            for t_x, t_y, t_z in modele.salles.keys():
                if t_z != 0:
                    # La salle est ignorée
                    continue

                t_vecteur = Vector(t_x, t_y, t_z)
                t_vecteur.around_z(radians(90))
                t_vecteur = t_vecteur + vecteur
                t_x, t_y, t_z = t_vecteur.x, t_vecteur.y, t_vecteur.z
                t_x, t_y, t_z = int(t_x), int(t_y), int(t_z)
                if (t_x, t_y, t_z) in points:
                    vecteurs.append(vecteur)
                else:
                    print(t_x, t_y, t_z, "not in", points)
                    invalide = True
                    break

            if invalide:
                print("Point invalide", x, y, z, t_x, t_y, t_z)
                continue

            # On vérifie que la distance minimale avec TOUS les points
            # est supérieure ou égale à 1
            distances = []
            for vecteur in vecteurs:
                distances.append(
                        importeur.navigation.distance_min_avec_navires(
                        vecteur))
            distances = [d for d in distances if d is not None]
            print("Distances", x, y, z, distances)
            if len(distances) == 0 or min(distances) >= 1:
                point = (x, y, z)
                break

        if point is None:
            raise CommandeInterrompue("Il n'y a plus de place dans le " \
                    "chantier naval")

        x, y, z = point
        navire = importeur.navigation.creer_navire(modele)
        navire.etendue = self.chantier.etendue
        navire.position.x = x
        navire.position.y = y
        navire.position.z = z
        navire.maj_salles()
        navire.valider_coordonnees()
        navire.proprietaire = self.instigateur
        navire.arreter()

    def cmd_renommer(self):
        """Renomme un navire."""
        navire = self.navire
        x, y, z = int(navire.position.x), int(navire.position.y), \
                int(navire.position.z)
        if (x, y, z) not in self.chantier.points:
            raise CommandeInterrompue("Le navire n'est plus dans le " \
                    "chantier naval")


        nom = self.arguments[0]
        navire.nom_personnalise = nom


class CommandeInterrompue(ExceptionMUD):

    """Exception levée quand la commande a été interrompue."""

    pass
