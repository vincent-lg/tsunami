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


"""Fichier contenant le paramètre 'script' de la commande 'tags'."""

import argparse
import shlex

from primaires.format.tableau import Tableau, DROITE
from primaires.interpreteur.masque.parametre import Parametre

# Constantes
AIDE = """
Cette commande permet de consulter ou modifier
la liste des scripts définis dans le tag. Elle prend
en paramètre obligatoire la clé du tag. Dans ce
cas, la liste des évènements inclus dans le script
du tag sont affichés.

Vous pouvez également préciser deux autres paramètres
après la clé du tag pour ajouter des scripts au tag.
Le premier est la clé de l'information à retrouver.

Par exemple, si le tag est de type PNJ, vous devrez
entrer une clé de prototype de PNJ. Le second paramètre
est l'évènement à copier. Dans sa forme la plus simple :
    %tags% %tags:script%|cmd| marchand vendeur_picte discute|ff|
Copiera l'évènement 'discute' du PNJ 'vendeur_picte'
dans le tag 'marchand'. Vous pouvez aussi préciser
un évènement spécifique, comme |ent|meurt.avant|ff|
par exemple. Enfin, vous pouvez préciser |ent|*|ff|
à la place du nom de l'évènement. Dans ce dernier
cas, tous les évènements possédant des lignes
de script seront copiés.""".lstrip("\n")

class PrmScript(Parametre):

    """Commande 'tags script'."""

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "script", "script")
        self.tronquer = True
        self.schema = "<cle> (<texte_libre>)"
        self.aide_courte = "modifie les scripts d'un tag"
        self.aide_longue = AIDE

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        def n_exit(code, msg):
            """Ne quitte pas Python."""
            raise ValueError(msg)

        cle = dic_masques["cle"].cle
        try:
            tag = importeur.tags.tags[cle]
        except KeyError:
            personnage << "|err|Ce tag n'existe pas.|ff|"
            return

        if not dic_masques["texte_libre"]:
            tableau = Tableau("Évènements du tag {} de type {}".format(
                    tag.cle, tag.type))
            tableau.ajouter_colonne("Évènement")
            tableau.ajouter_colonne("Lignes")
            for evt in tag.script.evenements.values():
                tableau.ajouter_ligne(evt.nom, evt.nb_lignes)

            personnage << tableau.afficher()
            return

        texte = dic_masques["texte_libre"].texte

        parser = argparse.ArgumentParser(conflict_handler='resolve')
        parser.exit = n_exit

        # Ajout des options
        parser.add_argument("objet")
        parser.add_argument("evenement")

        try:
            args = parser.parse_args(shlex.split(texte))
        except ValueError as err:
            personnage << "|err|Les options n'ont pas été interprétées " \
                    "correctement : {}.|ff|".format(err)
            return

        # Lecture des options
        objet = args.objet
        evenement = args.evenement

        # Récupération de l'objet du bon type
        try:
            objet = importeur.tags.cles[tag.type][objet]
        except KeyError:
            personnage << "|err|Clé de type {} {} introuvable.|ff|".format(
                    tag.type, repr(objet))
            return

        # Copie des évènements
        evenements = objet.script.evenements
        if evenement is "*":
            evenements = [e for e in evenements.values() if e.nb_lignes]
        else:
            morceaux = evenement.split(".")
            for morceau in morceaux:
                try:
                    evt = evenements[morceau]
                except KeyError:
                    personnage << "L'évènement {} dans {} ne peut " \
                            "être trouvé.|ff|".format(repr(morceau),
                            repr(evenement))
                    return
                else:
                    evenements = evt.evenements

            evenements = [evt]

        # Copie des évènements sélectionnés
        for evenement in evenements:
            personnage << "Copie de l'évènement {} ({} lignes).".format(
                    evenement.nom, evenement.nb_lignes)

            if evenement.nb_lignes == 0:
                continue

            tag.copier_evenement(evenement)
