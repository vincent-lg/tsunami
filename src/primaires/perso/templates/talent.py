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


"""Fichier contenant la classe Talent, détaillée plus bas."""

from corps.fonctions import valider_cle

class Talent:

    """Classe template des talents.

    Cette classe possède les attributs et méthodes propres à un talent.

    Attributs :
        cle -- la clé du talent (ne doit pas changer)
        nom -- le nom du talent (peut être modifié par la suite)
        niveau -- le nom du niveau secondaire du talent
        difficulte -- la difficulté d'apprentissage (entre 0 et 1)
        liberer_points (True par défaut)

    Le paramètre 'liberer_points' permet de savoir si l'ajout de
    ce talent entraîne l'ajout de 50 nouveaux points d'apprentissage
    disponibles à tous (c'est le cas par défaut).

    Notez que le nombre de points d'apprentissage disponibles
    peut être contrôlé par l'hook 'perso:points_apprentissage'.

    """

    def __init__(self, niveaux, cle, nom, niveau, difficulte,
            liberer_points=True):
        """Constructeur du talent."""
        valider_cle(cle)
        self.cle = cle
        self.nom = nom
        self.cle_niveau = niveau
        self.niveau = niveaux[niveau]
        self.difficulte = difficulte
        self.liberer_points = liberer_points

    def __repr__(self):
        return "niveau(" + self.cle + ")"

    def __str__(self):
        return self.nom

    def estimer_difficulte(self, configuration, avancement):
        """Estime et retourne la difficulté entre 0 et 1.

        La configuration permet de connaître le coefficient d'apprentissage.
        L'avancement représente la connaissance actuel dans le talent.

        Pour un personnage, il s'agit de son avancement dans le talent
        (entre 1 et 100).

        """
        if avancement >= 100:
            return 0

        restant = 100 - avancement
        restant = restant / 100
        coef = configuration.coefficient_apprentissage
        return self.difficulte ** coef * restant
