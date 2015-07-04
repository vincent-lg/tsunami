# -*-coding:Utf-8 -*

# Copyright (c) 2015 LE GOFF Vincent
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


"""Fichier contenant le paramètre 'commenter' de la commande 'rapport'."""

import argparse
import shlex

from primaires.format.fonctions import supprimer_accents
from primaires.interpreteur.masque.parametre import Parametre
from secondaires.rapport.constantes import CATEGORIES, PRIORITES

# Constantes
AIDE = """
Cette commande permet de commenter un rapport.
Elle commande prend deux arguments obligatoires :
le numéro du rapport suivi du commentaire. Par exemple
%rapport% %rapport:commenter%|cmd| 12 Bonne suggestion|ff|.
""".strip()

class PrmCommenter(Parametre):

    """Commande 'rapport commenter'."""

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "commenter", "comment")
        self.tronquer = True
        self.schema = "<nombre> <texte_libre>"
        self.aide_courte = "commente un rapport"
        self.aide_longue = AIDE

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        def n_exit(code, msg):
            """Ne quitte pas Python."""
            raise ValueError(msg)

        id = dic_masques["nombre"].nombre
        texte = dic_masques["texte_libre"].texte

        try:
            rapport = importeur.rapport.rapports[id]
        except KeyError:
            personnage << "|err|Ce rapport n'existe pas.|ff|"
            return

        parser = argparse.ArgumentParser(conflict_handler='resolve')
        parser.exit = n_exit

        # Ajout des options
        parser.add_argument("defaut", nargs='*')
        parser.add_argument("-f", "--fermer", action="store_true")
        parser.add_argument("-o", "--ouvrir", action="store_true")
        parser.add_argument("-a", "--assigner")
        parser.add_argument("-i", "--auto-assigner", action="store_true")
        parser.add_argument("-c", "--categorie")
        parser.add_argument("-v", "--avancement")
        parser.add_argument("-b", "--boost", action="count")
        parser.add_argument("-p", "--priorite")
        commentaire = None

        if personnage.est_immortel():
            options = texte
        elif rapport.createur is not personnage and not rapport.public:
            personnage << "|err|Vous n'avez pas le droit de commenter " \
                    "ce rapport.|ff|"
            return
        else:
            options = "ok"
            commentaire = texte

        try:
            args = parser.parse_args(shlex.split(options))
        except ValueError as err:
            personnage << "|err|Les options n'ont pas été interprétées " \
                    "correctement : {}.|ff|".format(err)
            return

        if commentaire:
            texte = commentaire
        else:
            texte = " ".join(args.defaut)

        # Traitement des options
        if args.fermer:
            rapport.statut = "fermé"
            personnage << "Fermeture du rapport."
        elif args.ouvrir:
            rapport.statut = "en cours"
            personnage << "Passage du rapport en statut \"en cours\"."

        # Assigné
        if args.auto_assigner:
            rapport.assigne_a = personnage
            personnage << "Vous vous êtes auto-assigné ce rapport."
        elif args.assigner:
            nom_joueur = args.assigner
            try:
                autre = importeur.joueur.get_joueur(nom_joueur)
            except KeyError:
                personnage << "|err|Le joueur {} est introuvable.|ff|".format(
                        repr(nom_joueur))
                return
            else:
                if autre.est_immortel():
                    rapport.assigne_a = autre
                    personnage << "Ce rapport a été assigné à {}.".format(
                            nom_joueur)
                else:
                    personnage << "|err|Le joueur {} n'est pas " \
                            "immortel.|ff|".format(repr(nom_joueur))
                    return

        # Catégorie
        if args.categorie:
            nom_categorie = supprimer_accents(args.categorie).lower()
            trouve = False
            for categorie in CATEGORIES:
                if supprimer_accents(categorie).startswith(nom_categorie):
                    rapport.categorie = categorie
                    personnage << "Placement du rapport dans la " \
                            "catégorie {}.".format(categorie)
                    trouve = True
                    break

            if not trouve:
                personnage << "|err|Catégorie {} inconnue.|ff|".format(
                        repr(nom_categorie))
                return

        # Avancement
        if args.avancement:
            avancement = args.avancement
            try:
                avancement = int(avancement)
                assert avancement >= 0 and avancement <= 100
            except (ValueError, AssertionError):
                personnage << "|err|Avancement {} invalide.|ff|".format(
                        repr(avancement))
                return
            else:
                rapport.avancement = avancement
                personnage << "Changement de l'avancement du rapport."
        elif args.boost:
            avancement = rapport.avancement
            avancement += 10 * args.boost
            if avancement > 100:
                avancement = 100

            rapport.avancement = avancement
            personnage << "Le rapport est à présent avancé à {}%.".format(
                    avancement)

        # Priorité
        if args.priorite:
            nom_priorite = supprimer_accents(args.priorite).lower()
            trouve = False
            for priorite in PRIORITES:
                if supprimer_accents(priorite).startswith(nom_priorite):
                    rapport.priorite = priorite
                    personnage << "Changement de la priorité du rapport."
                    trouve = True
                    break

            if not trouve:
                personnage << "|err|Priorité {} introuvable.|ff|".format(
                        repr(nom_priorite))
                return

        # Création du commentaire à proprement parlé
        commentaire = rapport.commenter(personnage, texte)
        personnage << "|att|Le rapport #{} a bien été commenté.|ff|".format(
                rapport.id)

        commentaire.notifier()
