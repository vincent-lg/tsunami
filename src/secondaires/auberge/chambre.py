# -*-coding:Utf-8 -*

# Copyright (c) 2010-2017 LE GOFF Vincent
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


"""Fichier contenant la classe Chambre, détaillée plus bas."""

from datetime import datetime

from abstraits.obase import BaseObj

# Constantes
MAX_NB_JOURS = 10
FCT_MIN = 0.6

class Chambre(BaseObj):

    """Classe représentant une chambre à louer.

    Une chambre fait parti d'une auberge. Elle possède un
    numéro, un prix (variable en fonction du nombre de jours). Elle
    possède également un propriétaire et une information de durée
    qui doivent être renseignés si la chambre est louée pour le
    moment.

    """

    def __init__(self, auberge, numero, salle):
        """Constructeur du navire."""
        BaseObj.__init__(self)
        self.auberge = auberge
        self.numero = numero
        self.salle = salle
        self.prix_par_jour = 1
        self.proprietaire = None
        self.expire_a = None
        self.dependances = []

    def __getnewargs__(self):
        return (None, "", None)

    def __repr__(self):
        return "<Chambre {}>".format(self.ident_salle)

    @property
    def ident_salle(self):
        return self.salle and self.salle.ident or "aucune"

    @property
    def expiree(self):
        """Retourne True si la chambre a expirée."""
        if self.expire_a is None:
            return False

        return datetime.now() > self.expire_a

    @property
    def aff_temps(self):
        """Affiche le temps avant expiration."""
        if self.expire_a is None:
            return

        delta = self.expire_a - datetime.now()
        if delta.days > 0:
            valeur = delta.days
            unite = "jour{s}"
        elif delta.total_seconds() > 3600:
            valeur = delta.total_seconds() // 3600
            unite = "heure{s}"
        else:
            valeur = delta.total_seconds() // 60
            unite = "minute{s}"
            if 5 <= valeur < 10:
                valeur = round(valeur // 2) * 2
            elif 10 <= valeur < 30:
                valeur = round(valeur // 5) * 5
            elif valeur >= 30:
                valeur = round(valeur // 10) * 10

        s = "s" if valeur > 1 else ""
        return str(valeur) + " " + unite.format(s=s)

    @property
    def nom_proprietaire(self):
        """Retourne le nom du propriétaire si louée."""
        return self.proprietaire and self.proprietaire.nom or "|att|aucun|ff|"

    @property
    def salles(self):
        """Retourne la salle de la chambre et les dépendances."""
        salles = [self.salle]
        salles.extend(self.dependances)
        return salles

    def prix(self, nb_jours):
        """Retourne le prix en fonction du nombre de jours loués.

        Ce prix est au minimum de 1. Il n'est pas équivalent au nombre
        de jours multipliés par le prix par jour, car plus le nombre
        est important, plus le prix relatif diminue (7 jours doivent
        coûter moins cher que 7 * 1 jorur).

        """
        absolu = self.prix_par_jour * nb_jours
        if nb_jours == 1:
            facteur = 1
        else:
            facteur = FCT_MIN + (30 - nb_jours) / 30 * \
                    (1 - FCT_MIN)

        prix = int(facteur * absolu)
        if prix < 1:
            prix = 1

        return prix

    def verifier_expiration(self):
        """Vérifie l'expiration."""
        if self.expiree:
            self.proprietaire = None
            self.expire_a = None
