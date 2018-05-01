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


"""Package contenant le paramètre 'ajouter' de la commande 'auberge'."""

import argparse
import shlex

from primaires.interpreteur.masque.parametre import Parametre

# Constantes
AIDE = """
Cette commande permet d'ajouter une chambre à une
auberge existante. Elle prend en premier paramètre
la clé de l'auberge, et en second le numéro de la
chambre. La salle dans laquelle vous vous trouvez
sera ajoutée à l'auberge sous le numéro indiqué.
Des options permettent d'ajouter plus rapidement
d'autres informations. Vous devez préciser ces options
après le numéro de la chambre à ajouter.

Options disponibles :
        |cmd|-p|ff| ou |cmd|--prix|ent| <prix par jour>|ff|
                Permet de changer le prix par jour de la
                chambre ajoutée. Par défaut, le prix par
                jour est à 1. Exemple :
                %auberge% %auberge:ajouter%|cmd| CLEDELAUBERGE NUMERO -p 5|ff|.
        |cmd|-d|ff| ou |cmd|--dependances|ent| <dépendances>|ff|
                Ajoute une ou plusieurs dépendances à
                la chambre. Les dépendances sont des
                salles liées à la chambre (qui peut
                s'étendre sur plusieurs salles). Un
                joueur se connectant dans une
                dépendance dont il n'est pas
                propriétaire est déplacé au comptoir
                de l'auberge. Pour ajouter des
                dépendances, vous pouvez préciser
                soit un nom de sortie qui sera
                cherché dans la salle courante, soit
                un identifiant (|ent|zone:mnémoniaque|ff|)
                de salle. Vous pouvez ajouter plusieurs
                dépendances en séparant les informations
                par une virgule. Exemples :
                %auberge% %auberge:ajouter%|cmd| AUBERGE NUMERO -d sud|ff|
                %auberge% %auberge:ajouter%|cmd| AUBERGE NUMERO -d depart:1|ff|
                %auberge% %auberge:ajouter%|cmd| AUBERGE NUMERO -d est, sud|ff|
""".strip("\n")

class PrmAjouter(Parametre):

    """Commande 'auberge ajouter'"""

    def __init__(self):
        """Constructeur du paramètre."""
        Parametre.__init__(self, "ajouter", "add")
        self.schema = "<cle> <texte_libre>"
        self.aide_courte = "ajoute une chambre d'auberge"
        self.aide_longue = AIDE

    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        def n_exit(code, msg):
            """Ne quitte pas Python."""
            raise ValueError(msg)

        cle = dic_masques["cle"].cle
        if cle not in importeur.auberge.auberges:
            personnage << "|err|Cette clé d'auberge est introuvable.|ff|"
            return

        auberge = importeur.auberge.auberges[cle]
        salle = personnage.salle
        options = dic_masques["texte_libre"].texte

        # Création de l'interpréteur d'option
        parser = argparse.ArgumentParser(conflict_handler='resolve')
        parser.exit = n_exit
        parser.add_argument("numero", nargs='+')
        parser.add_argument("-p", "--prix")
        parser.add_argument("-d", "--dependances", nargs='+')

        try:
            args = parser.parse_args(shlex.split(options))
        except ValueError as err:
            personnage << "|err|Les options n'ont pas été interprétées " \
                    "correctement : {}.|ff|".format(err)
            return

        if salle is auberge.comptoir:
            personnage << "|err|Cette salle est le comptoir de l'auberge.|ff|"
            return

        if salle in auberge.salles:
            personnage << "|err|Cette salle est déjà une chambre de " \
                    "l'auberge.|ff|"
            return

        numero = " ".join(args.numero)
        chambre = auberge.get_chambre_avec_numero(numero)
        if chambre:
            personnage << "|err|La chambre avec le numéro {} existe " \
                    "déjà.|ff|".format(repr(numero))
            return

        chambre = auberge.ajouter_chambre(numero, salle)
        personnage << "La chambre de numéro {} a bien été ajoutée à " \
                "l'auberge {}.".format(repr(numero), repr(auberge.cle))

        # Gestion du prix par jour
        prix = 1
        if args.prix:
            try:
                prix = int(args.prix)
                assert prix > 0
            except (ValueError, AssertionError):
                personnage << "|err|Le prix par jour entré est invalide.|ff|"

        chambre.prix_par_jour = prix
        personnage << "Le prix par jour de cette chambre est à {}.".format(
                prix)

        # Gestion des dépendances
        salles = []
        if args.dependances:
            dependances = " ".join(args.dependances).split(",")
            for dependance in dependances:
                dependance = dependance.strip()
                try:
                    sortie = salle.sorties.get_sortie_par_nom_ou_direction(
                            dependance)
                except KeyError:
                    try:
                        salles.append(importeur.salle[dependance])
                    except KeyError:
                        personnage << "|err|La salle {} est " \
                                "introuvable.|ff|".format(repr(dependance))
                else:
                    if sortie.salle_dest:
                        salles.append(sortie.salle_dest)

        chambre.dependances.extend(salles)
        if salles:
            s = "s" if len(salles) > 1 else ""
            a = "ont" if len(salles) > 1 else "a"
            personnage << "{} dépendance{s} {a} été ajoutée{s}.".format(
                    len(salles), s=s, a=a)
