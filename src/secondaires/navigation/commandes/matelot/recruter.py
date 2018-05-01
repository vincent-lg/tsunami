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
# ARE DISCLAIMED. IN NO Ematelot SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""Fichier contenant le paramètre 'recruter' de la commande 'matelot'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmRecruter(Parametre):

    """Commande 'matelot recruter'.

    """

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "recruter", "recruit")
        self.schema = "(<nombre> <personnage_present>)"
        self.tronquer = True
        self.aide_courte = "recrute un matelot"
        self.aide_longue = \
            "Cette commande permet de recruter un matelot présent " \
            "dans la même salle que vous. Deux cas sont à distinguer " \
            ": si vous êtes à terre (si vous êtes dans un bureau de " \
            "recrutement par exemple), vous pouvez demander aux matelots " \
            "récemment recrutés de rejoindre votre bord. Si vous êtes " \
            "sur un navire (que vous venez d'aborder, par exemple), vous " \
            "pouvez demander à un matelot de rejoindre votre navire si " \
            "celui-ci est assez proche. Cette commande prend deux " \
            "arguments : le numéro correspondant à votre navire. Vous " \
            "pouvez entrer la commande sans paramètre pour le connaître, " \
            "les navires que vous possédez (et qui peuvent être utilisés " \
            "pour le recrutement) seront affichés. Le second paramètre " \
            "est un fragment du nom du personnage que vous souhaitez " \
            "recruter. Si la commande réussi, le matelot recruté " \
            "rejoindra le navire ciblé d'ici quelques instants. Veillez " \
            "à rester accosté si vous êtes dans un port, sans quoi les " \
            "matelots ne pourront pas vous rejoindre."

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        salle = personnage.salle
        navires = importeur.navigation.get_navires_possedes(personnage)
        navire = getattr(salle, "navire", None)
        if dic_masques["nombre"] and dic_masques["personnage_present"]:
            nombre = dic_masques["nombre"].nombre
            cible = dic_masques["personnage_present"].personnage
            cle = getattr(cible, "cle", None)
            try:
                fiche = importeur.navigation.fiches[cle]
            except KeyError:
                personnage.envoyer("|err|Vous ne pouvez recruter {}.|ff|",
                        cible)
                return

            try:
                n_cible = navires[nombre - 1]
            except IndexError:
                personnage << "|err|Ce navire n'est pas visible.|ff|"
                return

            if cible.etats:
                personnage.envoyer("{} est occupé.", cible)
                return

            # Feint de partir
            if navire is None:
                sortie = [s for s in salle.sorties][0]
                salle.envoyer("{{}} s'en va vers {}.".format(
                        sortie.nom_complet), cible)
            else:
                salle.envoyer("{} saute à l'eau.", cible)
                matelot = navire.equipage.get_matelot_depuis_personnage(
                        cible)
                if matelot:
                    navire.equipage.supprimer_matelot(matelot.nom)

            cible.salle = None
            nom = "matelot_" + cible.identifiant
            importeur.diffact.ajouter_action(nom, 15, fiche.recruter,
                    cible, n_cible)
            personnage.envoyer("Vous recrutez {{}} sur {}.".format(
                    n_cible.desc_survol), cible)
        else:
            if navires:
                msg = "Navires que vous possédez :\n"
                for i, navire in enumerate(navires):
                    msg += "\n |ent|{}|ff| - {}".format(i + 1,
                            navire.desc_survol)
            else:
                msg = "|att|Vous ne possédez aucun navire " \
                        "pouvant servir au recrutement.|ff|"

            personnage << msg
