# -*-coding:Utf-8 -*

# Copyright (c) 2010-2016 NOEL-BARON Léo
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


"""Package contenant la commande 'cuisiner'."""

from math import sqrt
from random import random
from textwrap import dedent

from primaires.interpreteur.commande.commande import Commande

class CmdCuisiner(Commande):

    """Commande 'cuisiner'.

    """

    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "cuisiner", "cook")
        self.schema = ""
        self.aide_courte = "permet de cuire un plat"
        self.aide_longue = \
            ""

    def interpreter(self, personnage, dic_masques):
        """Interprétation de la commande"""
        ustensile = None
        for objet, qtt, t_conteneur in \
                personnage.equipement.inventaire.iter_objets_qtt(
                conteneur=True):
            if objet.est_de_type("ustensile") and objet.nourriture:
                ustensile = objet
                conteneur = t_conteneur
                break

        if ustensile is None:
            personnage << "|err|Vous ne tenez rien susceptible de cuire ou " \
                    "d'être cuit.|ff|"
            return

        try:
            feu = importeur.salle.feux[personnage.salle.ident]
            assert 5 < feu.puissance <= 40
        except (KeyError, AssertionError):
            personnage << "|err|Il n'y a pas de feu adéquat par ici.|ff|"
            return

        for objet in personnage.salle.objets_sol:
            if objet.est_de_type("ustensile") \
                    and objet.etat_singulier == objet.etat_cuisson:
                personnage << "|err|Quelque chose cuit déjà sur ce feu.|ff|"
                return

        # On commence réellement à cuisiner
        etat = ""
        personnage.agir("cuisiner")
        personnage << "Vous posez délicatement {} sur le feu.".format(
                ustensile.get_nom())
        conteneur.retirer(ustensile)
        personnage.salle.objets_sol.ajouter(ustensile)
        ustensile.etat_singulier = ustensile.etat_cuisson
        recette, qtt = importeur.cuisine.identifier_recette(
                [n.prototype for n in ustensile.nourriture])
        yield 2

        # Si l'ustensile n'est plus au sol
        if ustensile.contenu is not personnage.salle.objets_sol:
            return

        if recette:
            if ustensile.nom_type not in recette.ustensiles:
                etat = "ustensile"
                del ustensile.etat_singulier
            else:
                talent = personnage.pratiquer_talent("cuisine") / 100
                difficulte = sqrt(recette.difficulte / 100)
                reussite = random() > difficulte - talent
                # À ce stade, on cuit dans tous les cas
                for i in range(recette.temps_cuisson):
                    yield 1
                    if ustensile.contenu is not \
                            personnage.salle.objets_sol:
                        return

                    # On stoppe la cuisson si le feu est trop faible
                    if feu.puissance < recette.feu_mini:
                        personnage << "Le feu devient trop faible, votre " \
                                "mixture ne cuit plus."
                        del ustensile.etat_singulier
                        return

                    # Si la préparation a brûlée
                    if feu.puissance > recette.feu_maxi:
                        etat = "brule"
                        reussite = False
                        break

                # Retire les ingrédients en train de cuir
                for item in ustensile.nourriture:
                    importeur.objet.supprimer_objet(item.identifiant)
                ustensile.nourriture = []
                del ustensile.etat_singulier

                # Si on a réussi la recette
                if reussite:
                    # Ajoute le plat cuisiné
                    for i in range(qtt):
                        ustensile.nourriture.append(
                                importeur.objet.creer_objet(recette.resultat))
                    personnage << "Vous achevez de cuisiner {}.".format(
                            recette.resultat.get_nom(qtt))

                    # On donne l'expérience relative à la recette au personnage
                    personnage.gagner_xp("survie", (recette.xp * qtt))
                    return
                else:
                    etat = "rate"
        else:
            del ustensile.etat_singulier
            etat = "ingredients"

        if etat == "brule":
            personnage << dedent("""
                |err|Le feu était trop fort|ff| et votre préparation se mue
                en un résidu noirâtre que vous préférez jeter immédiatement.
            """.strip("\n"))
        elif etat == "rate":
            personnage << dedent("""
                |err|Tout semblait prêt|ff|, néanmoins votre préparation se
                transforme rapidement en quelque chose de peu ragoûtant que
                vous préférez jeter. Vous n'avez de toute évidence pas encore
                le coup de main.
            """.strip("\n"))
        elif etat == "ustensile":
            personnage << dedent("""
                |err|Votre ustensile n'était pas adéquat|ff| pour ce que
                vous tentiez de cuisiner.
            """.strip("\n"))
        elif etat == "ingredients":
            personnage << dedent("""
                |err|Visiblement, votre préparation n'aurait rien donné|ff|
                de comestible. Peut-être vous faudrait-il essayer un
                autre mélange.
            """.strip("\n"))
