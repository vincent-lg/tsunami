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


"""Fichier contenant la classe CommandeChantierNavale, détaillée plus bas."""

from datetime import datetime, timedelta

from abstraits.obase import BaseObj
from bases.exceptions.base import ExceptionMUD


class CommandeChantierNavale(BaseObj):

    """Classe décrivant une commande dans un chantier navale.

    Une commande est une opération "à faire" dans le chantier spécifié. Par
    exemple : le joueur X veut acheter un navire Y (mais l'achat du navire
    n'est pas instantanée, il faut le construire, ce qui prend plus ou moins
    de temps en fonction de la classe du navire).

    """

    def __init__(self, chantier, instigateur, navire, nom_type, duree, *args):
        """Constructeur d'une commande.

        Notez qu'il est préférable de passer par la méthode 'ajouter_commande' de ChantierNavale.

        Les paramètres à préciser sont :
            chantier -- le chantier navale (parent)
            instigateur -- le personnage ordonnant la commande
            navire -- le navire traité
            nom_type -- le type de commande
            duree -- la durée (en minutes) de la commande
            args -- des arguments supplémentaires en fonction du type

        """
        BaseObj.__init__(self)
        self.chantier = chantier
        self.instigateur = instigateur
        self.nom_type = nom_type
        self.duree = duree
        self.arguments = args
        self.date_debut = datetime.now()
        self._construire()

    def __getnewargs__(self):
        return (None, None, None, "inconnu", 0, )

    def __repr__(self):
        return "<CommandeChantierNavale {} pour {}>".format(
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

    # Types de commande
    def cmd_acheter(self):
        """Achète un navire."""
        cle_modele = self.arguments[0]
        modele = importeur.navigation.modeles[cle_modele]

        # On cherche un emplacement disponible dans le bassin
        point = None
        for navire in importeur.navigation.navires.values():
            t_point = None
            for point in self.points:
                v_point = Vector(*point)
                n_point = navire.opt_position
                if (n_point - v_point).mag < \
                        modele.get_max_distance_au_centre():
                    pass

class CommandeInterrompue(ExceptionMUD):

    """Exception levée quand la commande a été interrompue."""

    pass
