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


"""Package contenant la commande 'addroom'."""

import argparse
import shlex

from primaires.format.fonctions import format_nb
from primaires.interpreteur.commande.commande import Commande
from primaires.interpreteur.masque.exceptions.erreur_interpretation import \
    ErreurInterpretation

# Constantes
AIDE = """
Cette commande permet d'ajouter une salle à l'univers. Elle prend
en paramètre obligatoire la direction absolue dans laquelle vous
voulez créer la salle (|ent|est|ff|, |ent|sud-est|ff|, |ent|sud|ff|...,
|ent|haut|ff| ou |ent|bas|ff|). Vous pouvez également préciser après
cette direction des options facultatives dont voici la liste :

Options possibles :
        |cmd|-t|ff| ou |cmd|--titre|ff|
                Cette option va créer la nouvelle salle en copiant
                le titre de la salle actuel.
        |cmd|-d|ff| ou |cmd|--description|ff|
                Copie la description de la salle courante vers
                la salle cible. Cette option est très utile si les
                deux salles sont destinées à utiliser des flottantes.
                Les scripts de la description (c'est-à-dire les
                éléments dynamiques) sont également copiés.
        |cmd|-e|ff| ou |cmd|--details|ff|
                Copie les détails de la salle d'origine. Cette option
                copie également les scripts des détails (éléments
                dynamiques des descriptions et actions liées à des
                commandes dynamiques). Notez qu'il est tout de même
                préférable d'utiliser des flottantes, sauf cas particulier.
        |cmd|-m|ff| ou |cmd|--mnemonique|ff| |ent[ARG]|ff|
                Cette option est utile si vous voulez que la nouvelle
                salle soit créée avec un mnémonique spécifique. Vous
                devez préciser après cette option le nouveau mnémonique.
                Soit c'est un nom simple : dans ce cas la zone de la
                salle courante sera conservé. Soit c'est un nom de
                zone suivi de deux points et d'un nom de mnémonique :
                dans ce cas-là, la nouvelle salle sera créée dans
                l'autre zone indiquée. Si vous faites par exemple
                %addroom%|cmd| est -m auberge|ff|, la nouvelle salle
                sera créé dans la même zone que la salle où vous vous
                trouvez mais elle aura pour mnémonique |ent|auberge|ff|.
        |cmd|-c|ff| ou |cmd|--script|ff|
                Copie les scripts de la salle d'origine. Les évènements,
                sous-évènements et tests sont copiés et déréférencés :
                cela signifie que vous pourrez modifier un des  scripts
                d'une des salles sans que cela ne modifie celui de
                l'autre.
        |cmd|-s|ff| ou |cmd|--sorties|ff|
                Si la salle créée a des coordonnées valides, crée
                toutes les sorties (est, sud-est, sud, sud-ouest...
                bas, haut) dont les coordonnées pointent vers
                des salles existantes. Cette option crée également
                les réciproques des sorties. Cette option est en
                fait une combinaison des options |cmd|-h|ff|
                (|cmd|--horizontales|ff|) et |cmd|-v|ff|
                (|cmd|--verticales|ff|). En somme, entrer
                %addroom%|ent| <direction>|cmd| -s|ff| revient à
                entrer %addroom%|ent| <direction>|cmd| -hv|ff|.
        |cmd|-h|ff| ou |cmd|--horizontales|ff|
                Si la salle créée a des coordonnées valides, crée
                toutes les sorties horizontales (est, sud-est, sud,
                sud-ouest, ..., nord, nord-est) si les coordonnées
                pointent vers des salles déjà existantes. Cette
                option crée également les sorties réciproques.
        |cmd|-v|ff| ou |cmd|--verticales|ff|
                Si la salle créée a des coordonnées valides, crée
                toutes les sorties verticales (haut et bas)
                si les coordonnées pointent vers des salles déjà
                existantes. Cette option crée également les sorties
                réciproques.
        |cmd|-r|ff| ou |cmd|--sans-reciproque|ff|
                Crée la sortie d'origine et la sortie réciproque dans
                la salle opposée, mais supprime le lien entre elles.
                Cela signifie que les deux sorties peuvent évoluer
                indépendemment. Par exemple, il vous serai possible de
                créer une sortie menant vers le bas que l'on peut
                emprunter sans escalader, alors que pour remonter il
                faudrait escalader. Pour cela il faut avoir deux sorties
                sans réciproque. Utilisez cette option pour en créer."
""".strip()


HORIZONTALES = {
        "est": (1, 0, 0),
        "sud-est": (1, -1, 0),
        "sud": (0, -1, 0),
        "sud-ouest": (-1, -1, 0),
        "ouest": (-1, 0, 0),
        "nord-ouest": (-1, 1, 0),
        "nord": (0, 1, 0),
        "nord-est": (1, 1, 0),
}

VERTICALES = {
        "bas": (0, 0, -1),
        "haut": (0, 0, 1),
}

SORTIES = HORIZONTALES.copy()
SORTIES.update(VERTICALES)

class CmdAddroom(Commande):

    """Commande 'addroom'"""

    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "addroom", "addroom")
        self.groupe = "administrateur"
        self.schema = "<direction> (<texte_libre>)"
        self.nom_categorie = "batisseur"
        self.aide_courte = "ajoute une salle à l'univers"
        self.aide_longue = AIDE

    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        def n_exit(code, msg):
            """Ne quitte pas Python."""
            raise ValueError(msg)

        direction = dic_masques["direction"].direction
        salle = personnage.salle
        options = ""
        if dic_masques["texte_libre"]:
            options = dic_masques["texte_libre"].texte

        # Création de l'interpréteur d'option
        parser = argparse.ArgumentParser(conflict_handler='resolve')
        parser.exit = n_exit
        parser.add_argument("-t", "--titre", action="store_true")
        parser.add_argument("-d", "--description", action="store_true")
        parser.add_argument("-e", "--details", action="store_true")
        parser.add_argument("-m", "--mnemonique")
        parser.add_argument("-c", "--script", action="store_true")
        parser.add_argument("-s", "--sorties", action="store_true")
        parser.add_argument("-h", "--horizontales", action="store_true")
        parser.add_argument("-v", "--verticales", action="store_true")
        parser.add_argument("-r", "--sans-reciproque", action="store_true")

        try:
            args = parser.parse_args(shlex.split(options))
        except ValueError as err:
            personnage << "|err|Les options n'ont pas été interprétées " \
                    "correctement : {}.|ff|".format(err)
            return

        if args.mnemonique:
            try:
                zone, mnemonic = args.mnemonique.split(":")
            except ValueError:
                zone = salle.nom_zone
                mnemonic = args.mnemonique
        else:
            zone = salle.nom_zone
            mnemonic = salle.zone.chercher_mnemonic_libre(salle.mnemonic)

        dir_opposee = salle.sorties.get_nom_oppose(direction)

        if salle.sorties.sortie_existe(direction):
            raise ErreurInterpretation(
                "|err|Cette direction a déjà été définie dans la salle.|ff|")

        nv_coords = getattr(salle.coords, direction.replace("-", ""))
        if nv_coords.valide and nv_coords in type(self).importeur.salle:
            raise ErreurInterpretation(
                "|err|Ces coordonnées sont déjà utilisées.|ff|")

        x, y, z, valide = nv_coords.tuple_complet()

        try:
            nv_salle = importeur.salle.creer_salle(zone, mnemonic,
                    x, y, z, valide)
        except ValueError as err_val:
            personnage << str(err_val) + "."
        else:
            if args.sans_reciproque:
                salle.sorties.ajouter_sortie(direction, direction,
                        salle_dest=nv_salle, corresp=None)
                nv_salle.sorties.ajouter_sortie(dir_opposee, dir_opposee,
                        salle_dest=salle, corresp=None)
            else:
                salle.sorties.ajouter_sortie(direction, direction,
                        salle_dest=nv_salle, corresp=dir_opposee)
                nv_salle.sorties.ajouter_sortie(dir_opposee, dir_opposee,
                        salle_dest=salle, corresp=direction)

            nv_salle.interieur = salle.interieur
            nv_salle.illuminee = salle.illuminee
            nv_salle.nom_terrain = salle.nom_terrain
            if args.titre:
                nv_salle.titre = salle.titre
            if args.description:
                nv_salle.description.copier_depuis(salle.description)
            if args.details:
                nv_salle.details.copier_depuis(salle.details, True)
            if args.script:
                nv_salle.script.copier_depuis(salle.script)

            personnage << "|att|La salle {} a bien été ajouté vers {}.|ff|". \
                    format(nv_salle.ident, salle.sorties[direction].nom_complet)

            sup = None
            if args.sorties:
                sup = SORTIES
            elif args.horizontales:
                sup = HORIZONTALES
            elif args.verticales:
                sup = VERTICALES

            if sup:
                if not nv_coords.valide:
                    personnage << "|err|La salle créée n'a pas de " \
                            "coordonnées valides.|ff|"
                    return

                nb = 0
                for direction, coords in sup.items():
                    n_x = x + coords[0]
                    n_y = y + coords[1]
                    n_z = z + coords[2]
                    dir_opposee = nv_salle.sorties.get_nom_oppose(direction)
                    salle = importeur.salle._coords.get((n_x, n_y, n_z))
                    if salle is None:
                        continue

                    if not salle.sorties.sortie_existe(dir_opposee) and not \
                            nv_salle.sorties.sortie_existe(direction):
                        nv_salle.sorties.ajouter_sortie(direction, direction,
                                salle_dest=salle, corresp=dir_opposee)
                        salle.sorties.ajouter_sortie(dir_opposee, dir_opposee,
                                salle_dest=nv_salle, corresp=direction)
                        nb += 1

                if nb > 0:
                    personnage << format_nb(nb, "{nb} sortie{s} " \
                            "supplémentaire{s} créée{s}.")
