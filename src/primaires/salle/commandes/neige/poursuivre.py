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


"""Package contenant le paramètre 'poursuivre' de la commande 'neige'."""

from primaires.interpreteur.masque.parametre import Parametre
from primaires.perso.exceptions.stat import DepassementStat
from primaires.salle.bonhomme_neige import BonhommeNeige

class PrmPoursuivre(Parametre):

    """Commande 'neige poursuivre'"""

    def __init__(self):
        """Constructeur du paramètre."""
        Parametre.__init__(self, "poursuivre", "resume")
        self.schema = "<element_observable>"
        self.aide_courte = "continue un bonhomme de neige"
        self.aide_longue = \
            "Cette commande permet de continuer la fabrication d'un " \
            "bonhomme de neige. Vous devez préciser le nom du bonhomme " \
            "déjà entamé (celui visible dans le %regarder%)."

    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        elt = dic_masques["element_observable"].element
        salle = personnage.salle
        end = 25
        force = 7
        personnage.agir("neige")

        # Vérifie qu'il s'agit bien d'un bonhomme de neige
        if not isinstance(elt, BonhommeNeige):
            personnage << "|err|Ceci n'est pas un bonhomme de neige.|ff|"
            return

        bonhomme = elt
        if bonhomme.complet:
            personnage << "|err|Ce bonhomme de neige est déjà complet.|ff|"
            return

        try:
            personnage.stats.endurance -= end
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

            if salle.affections["neige"].force < force:
                personnage << "|err|Il n'y a pas assez de neige ici.|ff|"
                return

            personnage << "Vous commencez à rassembler de la neige."
            salle.envoyer("{} commence à rassembler de la neige.",
                    personnage)
            salle.affections["neige"].force -= force
            personnage.etats.ajouter("bonhomme_neige")
            yield 40
            if "bonhomme_neige" not in personnage.etats:
                return

            personnage.etats.retirer("bonhomme_neige")
            bonhomme.etat += 1
            ponctuation = "."
            if bonhomme.complet:
                ponctuation = " !"
            personnage << "Vous avez fabriqué {}{}".format(
                    bonhomme.get_nom(), ponctuation)
            salle.envoyer("{{}} a fabriqué {}.".format(
                    bonhomme.get_nom()), personnage)
