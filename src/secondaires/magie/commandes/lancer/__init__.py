# -*-coding:Utf-8 -*

# Copyright (c) 2010 DAVY Guillaume
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


"""Package contenant la commande 'lancer'."""

from primaires.format.fonctions import contient
from primaires.interpreteur.commande.commande import Commande
from primaires.perso.personnage import Personnage
from primaires.objet.objet import Objet

class CmdLancer(Commande):

    """Commande 'lancer'.

    """

    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "lancer", "cast")
        self.groupe = "pnj"
        self.schema = "<nom_sort> (sur/to <cible_sort>)"
        self.nom_categorie = "combat"
        self.aide_courte = "lance un sort"
        self.aide_longue = \
            "Cette commande lance un sort dans la salle où vous vous " \
            "trouvez, à condition que vous maîtrisiez ce sort bien entendu. " \
            "Vous pouvez préciser une cible si le sort en demande une."

    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        from primaires.joueur.joueur import Joueur
        sort = dic_masques["nom_sort"].sort
        parchemin = dic_masques["nom_sort"].parchemin
        personnage.agir("lancersort")
        cible = dic_masques["cible_sort"] and dic_masques["cible_sort"].cible \
                or None

        salle = personnage.salle
        if not personnage.est_immortel() and salle.a_flag("anti magie"):
            personnage << "|err|Vous ne percevez aucun courant magique " \
                    "ici.|ff|"
            return

        if cible is None and sort.type_cible == "personnage":
            if sort.offensif:
                combat = importeur.combat.combats.get(personnage.salle.ident)
                if combat is not None:
                    cible = combat.combattus.get(personnage)
                else:
                    cible = importeur.combat.cible.get(personnage)
            else:
                cible = personnage

        salle_cible = personnage.salle
        if sort.type_cible == "salle":
            if cible is None:
                cible = personnage.salle
            elif isinstance(cible, Personnage):
                cible = cible.salle

        if cible and sort.type_cible == "personnage" and sort.offensif:
            if not personnage.est_immortel() and not personnage.pk and \
                    isinstance(cible, Joueur):
                personnage << "|err|Votre flag PK n'est pas actif.|ff|"
                return

            if not personnage.est_immortel() and not cible.pk:
                personnage << "|err|Vous ne pouvez attaquer un joueur qui " \
                        "n'a pas le flag PK activé.|ff|"
                return

        if cible is None:
            if sort.type_cible != "aucune":
                personnage << "|err|Vous devez préciser une cible pour ce " \
                        "sort.|ff|"
            else:
                if not sort.peut_lancer(personnage):
                    personnage << "|err|Vous ne pouvez lancer ce sort.|ff|"
                    return

                personnage.agir("magie")
                personnage.cle_etat = "magie"
                if parchemin:
                    sort.concentrer(personnage, None, apprendre=False)
                    parchemin.charges -= 1
                else:
                    sort.concentrer(personnage, None)
        else:
            if sort.type_cible == "aucune":
                personnage << "|err|Ce sort ne peut être lancé sur une " \
                        "cible.|ff|"
            else:
                # Vérification du type de cible
                if sort.type_cible == "personnage" and not isinstance(cible,
                        Personnage):
                    personnage << "|err|Ce sort ne peut être lancé que sur " \
                            "un personnage ou une créature.|ff|"
                    return
                if sort.type_cible == "objet" and not isinstance(cible, Objet):
                    personnage << "|err|Ce sort ne peut être lancé que sur " \
                            "un objet.|ff|"
                    return

                if not sort.peut_lancer(personnage):
                    personnage << "|err|Vous ne pouvez lancer ce sort.|ff|"
                    return

                personnage.agir("magie")
                personnage.cle_etat = "magie"
                if parchemin:
                    sort.concentrer(personnage, cible, apprendre=False)
                    parchemin.charges -= 1
                else:
                    sort.concentrer(personnage, cible)
