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


"""Fichier définissant la classe statique de manipulation des joueurs."""

from primaires.joueur.joueur import Joueur
from test.primaires.connex.fausse_instance_connexion import \
        FausseInstanceConnexion

class ManipulationJoueur:

    """Classe utilisée pour manipuler des joueurs dans les tests unitaires.

    Cette classe sert à créer et supprimer des joueurs de façon
    simple et transparente à l'intérieur de tests unitaires. Elle
    comporte plusieurs méthodes statiques utiles pour la manipulation,
    donc on peut hériter une classe de cette classe de manipulation
    (et d'autres si nécessaire).

    """

    @staticmethod
    def creer_joueur(compte, nom):
        """Crée un joueur dans le compte indiqué.

        Les paramètres attendus sont :

          compte -- le nom du compte (il doit déjà avoir été créé)
          nom -- le nom du joueur à créer

        """
        compte = importeur.connex.comptes[compte]
        joueur = Joueur()
        joueur.nom = nom
        joueur.instance_connexion = FausseInstanceConnexion()
        joueur.instance_connexion.joueur = joueur
        compte.ajouter_joueur(joueur)
        joueur.pre_connecter()
        return joueur

    def supprimer_joueur(self, joueur):
        """Supprime le joueur précisé."""
        if joueur.compte:
            joueur.compte.supprimer(joueur)

        joueur.pre_deconnecter()
        joueur.detruire()
