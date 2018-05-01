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


"""Package contenant le paramètre 'boule' de la commande 'neige'."""

from primaires.interpreteur.masque.parametre import Parametre
from primaires.perso.exceptions.stat import DepassementStat

class PrmBoule(Parametre):

    """Commande 'neige boule'"""

    def __init__(self):
        """Constructeur du paramètre."""
        Parametre.__init__(self, "boule", "ball")
        self.aide_courte = "fabrique une boule de neige"
        self.aide_longue = \
            "Cette commande permet de rassembler de la neige afin de " \
            "fabriquer une boule de neige. Vous pouvez ensuite la lancer " \
            "sur quelqu'un avec la commande %lancer%."

    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        salle = personnage.salle
        personnage.agir("neige")
        try:
            personnage.stats.endurance -= 3
        except DepassementStat:
            personnage << "|err|Vous êtes trop fatigué.|ff|"
        else:
            if personnage.nb_mains_libres < 2:
                personnage << "|err|Il vous faut au moins deux mains " \
                        "de libre.|ff|"
                return

            if "neige" not in salle.affections:
                personnage << "|err|Il n'y a pas de neige ici.|ff|"
                return

            if salle.affections["neige"].force < 5:
                personnage << "|err|Il n'y a pas assez de neige ici.|ff|"
                return

            personnage << "Vous commencez à rassembler de la neige."
            salle.envoyer("{} commence à rassembler de la neige.",
                    personnage)
            salle.affections["neige"].force -= 1
            personnage.etats.ajouter("bonhomme_neige")
            yield 3
            if "bonhomme_neige" not in personnage.etats:
                return

            personnage.etats.retirer("bonhomme_neige")
            boule = importeur.objet.creer_objet(importeur.objet.prototypes[
                    "boule_neige"])
            for membre in personnage.equipement.membres:
                if membre.peut_tenir() and membre.tenu is None:
                    membre.tenu = boule
                    boule.contenu = personnage.equipement.tenus
                    break

            personnage << "Vous avez fabriqué {}.".format(boule.get_nom())
            salle.envoyer("{{}} a fabriqué {}.".format(
                    boule.get_nom()), personnage)
