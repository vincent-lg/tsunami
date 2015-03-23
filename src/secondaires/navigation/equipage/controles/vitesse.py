# -*-coding:Utf-8 -*

# Copyright (c) 2014 LE GOFF Vincent
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


"""Fichier contenant le contrôle Vitesse."""

from math import fabs

from secondaires.navigation.constantes import *
from secondaires.navigation.equipage.controle import Controle

class Vitesse(Controle):

    """Classe représentant le contrôle 'vitesse'.

    Ce contrôle permet de spécifier une vitesse idéale en noeuds.
    Le commandant va ensuite combiner les différents facteurs propulsifs
    du navire pour trouver la vitesse qui se rapproche le plus de
    celle spécifiée. Par exemple, si le navire a des rames, le capitaine
    va calculer les vitesses possibles des rames (un simple calcul,
    car les rames ont cinq vitesses en comptant la marche arrière et
    il n'existe pas d'ordre pour demander à un rameur de ramer vite
    tandis que l'autre rame doucement). Si le navire a des voiles, le
    calcul devient plus compliqué car le capitaine doit calculer l'allure
    du navire et, en fonction de la force du vent et de la meilleure
    orientation possible, déduire des vitesses de ses voiles. En
    combinant tous ces résultats, le capitaine trouve un ensemble
    de propulsifs idéal et transmet les ordres adéquats.

    Par exemle :
        Je veux aller à 1,2 noeuds
        Le navire a une paire de rame
            Les viteses des rames sont 0,2 (lente), 0,5 (moyenne)
            et 0,8 (rapide).
        Le navire a deux voiles. Il est au largue et si il déploie
        une voile il est propulsé de 0,5 noeuds, 1 noeud si il déploie
        les deux voiles.
        En conséquence, la meilleure combinaison serai de déplier
        les 2 voiles et de ramer doucement.

    """

    cle = "vitesse"

    def __init__(self, equipage, vitesse=None, autoriser_vitesse_sup=True):
        Controle.__init__(self, equipage, vitesse, autoriser_vitesse_sup)
        self.vitesse = vitesse
        self.autoriser_vitesse_sup = autoriser_vitesse_sup
        self.vitesse_optimale = None
        self.derniere_vitesse = None
        self.force_vent = None

    def afficher(self):
        """Retourne le message pour l'affichage du contrôle."""
        vitesse = self.vitesse
        if vitesse is None:
            return "Au maximum de vitesse"
        else:
            s = "s" if vitesse != 1 else ""
            vitesse = str(round(vitesse, 1)).replace(".", ",")

        return "À {} noeud{s}".format(vitesse, s=s)

    def calculer_vitesse(self):
        """Calcul la vitesse en fonction des propulsifs.

        Cette méthode :
            Compte le nombre de propulsifs et leur type (rames, voiles)
            Calcul chaque potentiel de chaque propulsif ou état
            Cherche la meilleure combinaison de propulsifs et d'états.
            Transmet les ordres appropriés à l'équipage.

        """
        commandant = self.commandant
        if commandant is None:
            return

        personnage = commandant.personnage
        equipage = self.equipage
        navire = self.navire
        vent = navire.vent
        self.verifier_voiles()

        # Écrit la vitesse actuelle du vent
        if self.force_vent is None:
            self.force_vent = vent.mag

        # Retrouve tous les éléments propulsifs et cherche les vitesses
        nb_rames = len(navire.rames)
        nb_voiles = len(navire.voiles)
        vitesses = {}
        vit_rames = {}

        # Si la vitesse est de 0, le calcul est tout fait
        if self.vitesse == 0:
            choix = (0, "immobile", 0)
        else:
            # Si il y a des rames, on calcul leur force propulsive
            if nb_rames > 0:
                for nom in ("lente", "moyenne", "rapide"):
                    noms = (nom, ) * nb_rames
                    vitesse = get_vitesse_noeuds(navire.get_vitesse_rames(
                            noms) / 0.7)
                    vitesses[vitesse] = (nom, 0)
                    vit_rames[nom] = vitesse

            if navire.nom_allure != "vent debout":
                for i in range(nb_voiles):
                    voiles = (None, ) * (i + 1)
                    vit_voiles = get_vitesse_noeuds(navire.get_vitesse_voiles(
                            voiles, vent) / 0.7)
                    vitesses[vit_voiles] = ("immobile", i + 1)
                    for nom, vit_rame in vit_rames.items():
                        vitesse = vit_voiles + vit_rame
                        vitesses[vitesse] = (nom, i + 1)

            # À ce stade, on a chaque vitesse, avec ou sans voiles et rames
            # On cherche la vitesse la plus proche de l'objectif
            # Si la vitesse est illimitée, choisit le maximum
            if self.vitesse is None:
                vitesses = tuple(vitesses.items())
                vitesse, (vit_rame, nb_voiles) = max(vitesses)
                choix = (vitesse, vit_rame, nb_voiles)
            else:
                diff = attendue = self.vitesse
                for vitesse, (vit_rame, nb_voiles) in vitesses.items():
                    if not self.autoriser_vitesse_sup and vitesse > attendue:
                        continue

                    if fabs(attendue - vitesse) <= diff:
                        diff = fabs(attendue - vitesse)
                        choix = (vitesse, vit_rame, nb_voiles)

        # Écrit dans les logs le choix auquel on est parvenu
        vitesse, vit_rame, nb_voiles = choix
        self.debug("choisit la combinaison rames={} et voiles={} pour " \
                "vitesse={} (optimale={})".format(vit_rame, nb_voiles,
                vitesse, self.vitesse))

        # Donne les ordres correspondant
        # Les rames, si nécessaire
        if any(rame.vitesse != vit_rame for rame in navire.rames):
            equipage.demander("ramer", vit_rame, personnage=personnage)

        # Pour les voiles on cherche celles hissées
        nb_hissees = len([v for v in navire.voiles if v.hissee])
        nb_hissees += len(equipage.get_matelots_ayant_ordre("hisser_voile"))
        nb_hissees -= len(equipage.get_matelots_ayant_ordre("plier_voile"))
        diff = nb_voiles - nb_hissees
        if diff > 0:
            # On doit hisser au moins une voile
            equipage.demander("hisser_voiles", diff, personnage=personnage)
        elif diff < 0:
            # On doit plier au moins une voile
            equipage.demander("plier_voiles", -diff, personnage=personnage)
        self.vitesse_optimale = vitesse

    def verifier_voiles(self):
        """Vérifie les voiles.

        Si elles sont hissées et que le navire est vent debout,
        demande de les plier immédiatement, car le navire va culer
        sinon.

        """
        commandant = self.commandant
        if commandant is None:
            return

        personnage = commandant.personnage
        equipage = self.equipage
        navire = self.navire
        voiles = navire.voiles
        hissee = any(e.hissee for e in voiles)
        allure = navire.nom_allure
        if hissee and allure == "vent debout":
            if not equipage.get_matelots_ayant_ordre("plier_voile"):
                equipage.demander("plier_voiles", None, personnage=personnage)

    def controler(self):
        """Contrôle l'avancement du contrôle.

        On vérifie deux choses :
            Si s'applique, le vent a-t-il changé ?
            La dernière vitesse et vitesse courante sont-elles différentes ?

        """
        commandant = self.commandant
        if commandant is None:
            return

        equipage = self.equipage
        navire = self.navire
        vent = navire.vent
        self.verifier_voiles()
        if navire.acceleration.est_nul(1):
            self.ancienne_vitesse = navire.vitesse_noeuds
            if self.vitesse_optimale is not None and fabs(
                    self.ancienne_vitesse - self.vitesse_optimale) > 0.2:
                self.debug("optimale={}, actuelle={}".format(
                        self.vitesse_optimale, self.ancienne_vitesse))
                self.calculer_vitesse()
            elif fabs(self.force_vent - vent.mag) > 0.3:
                self.force_vent = vent.mag
                self.calculer_vitesse()

    def decomposer(self):
        """Décompose le contrôle en volontés."""
        commandant = self.commandant
        if commandant is None:
            return

        self.calculer_vitesse()
