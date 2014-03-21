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


"""Package contenant le paramètre 'fabriquer' de la commande 'neige'."""

from primaires.interpreteur.masque.parametre import Parametre
from primaires.perso.exceptions.stat import DepassementStat

class PrmFabriquer(Parametre):

    """Commande 'neige fabriquer'"""

    def __init__(self):
        """Constructeur du paramètre."""
        Parametre.__init__(self, "fabriquer", "build")
        self.schema = "<bonhomme_neige>"
        self.aide_courte = "commence un bonhomme de neige"
        self.aide_longue = \
            "Cette commande permet de commencer à fabriquer un bonhomme " \
            "de neige. Vous devez préciser un nom de modèle, sachant que " \
            "rien ne vous permet de les connaître à l'avance (ce peut " \
            "être un nom de race, d'animal et même parfois des noms plus " \
            "exotiques, cela dépend). Le bonhomme de neige que vous " \
            "fabriquerez ne sera pas complet à la fin, vous devrez " \
            "utiliser la commande %neige:poursuivre%."

    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        modele = dic_masques["bonhomme_neige"].modele
        salle = personnage.salle
        force = 7
        end = 25
        personnage.agir("neige")
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
            bonhomme = salle.ajouter_decor(modele)
            bonhomme.etat = 0
            bonhomme.createur = personnage
            personnage << "Vous avez fabriqué {}.".format(
                    bonhomme.get_nom())
            salle.envoyer("{{}} a fabriqué {}.".format(
                    bonhomme.get_nom()), personnage)
