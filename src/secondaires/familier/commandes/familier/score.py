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
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT master OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""Fichier contenant le paramètre 'score' de la commande 'familier'."""

from primaires.interpreteur.masque.parametre import Parametre
from primaires.perso.commandes.score import chn_score

class PrmScore(Parametre):

    """Commande 'familier score'."""

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "score", "score")
        self.schema = "<nom_familier>"
        self.aide_courte = "affiche le score du familier"
        self.aide_longue = \
            "Cette commande permet d'afficher les stats complètes du " \
            "familier. Le rendu est identiqué au rendu de votre fiche score."

    def ajouter(self):
        """Méthode appelée lors de l'ajout de la commande à l'interpréteur"""
        familier = self.noeud.get_masque("nom_familier")
        familier.proprietes["salle_identique"] = "False"

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        # On récupère le familier
        familier = dic_masques["nom_familier"].familier
        fiche = familier.fiche
        pnj = familier.pnj
        nom_race = pnj.race and pnj.race.nom or "aucune"
        poids = int(pnj.poids)
        poids_max = int(pnj.poids_max)
        poids_pc = int(poids / poids_max * 100)
        personnage << chn_score.format(
            nom=familier.nom,
            nom_race=nom_race,
            genre=pnj.genre,
            v=pnj.vitalite,
            vm=pnj.vitalite_max,
            m=pnj.mana,
            mm=pnj.mana_max,
            e=pnj.endurance,
            em=pnj.endurance_max,
            f=pnj.force,
            a=pnj.agilite,
            r=pnj.robustesse,
            i=pnj.intelligence,
            c=pnj.charisme,
            s=pnj.sensibilite,
            poids=poids,
            poids_max=poids_max,
            poids_pc=poids_pc,
            p_app=pnj.points_apprentissage,
            p_app_max=pnj.points_apprentissage_max,
            p_en=pnj.points_entrainement,
            p_tr=pnj.points_tribut,
        )
