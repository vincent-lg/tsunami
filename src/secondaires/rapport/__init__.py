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


"""Fichier contenant le module secondaire rapport."""

from abstraits.module import *
from primaires.format.fonctions import format_nb
from . import commandes
from . import editeurs
from . import cherchables
from .rapport import Rapport
from .editeurs.bugedit import EdtBugedit
from .editeurs.bugedit_p import EdtBugeditP

class Module(BaseModule):

    """Classe utilisée pour gérer des rapports de bug et suggestion.

    """

    def __init__(self, importeur):
        """Constructeur du module"""
        BaseModule.__init__(self, importeur, "rapport", "secondaire")
        self.rapports = {}
        self.commandes = []
        self.traces = {}

    def init(self):
        """Méthode d'initialisation du module"""
        # On récupère les rapports
        rapports = self.importeur.supenr.charger_groupe(Rapport)
        for rapport in rapports:
            self.rapports[rapport.id] = rapport

        if self.rapports:
            Rapport.id_actuel = max(self.rapports.keys()) + 1
        else:
            Rapport.id_actuel = 1

        # On lie la méthode joueur_connecte avec l'hook joueur_connecte
        # La méthode joueur_connecte sera ainsi appelée quand un joueur
        # se connecte
        self.importeur.hook["joueur:connecte"].ajouter_evenement(
                self.joueur_connecte)
        self.importeur.hook["joueur:erreur"].ajouter_evenement(
                self.sauver_traceback)
        # Abonne le module aux stats
        self.importeur.hook["stats:infos"].ajouter_evenement(
                self.stats_rapports)

        BaseModule.init(self)

    def ajouter_commandes(self):
        """Ajout des commandes dans l'interpréteur"""
        self.commandes = [
            commandes.bug.CmdBug(),
            commandes.orthographe.CmdOrthographe(),
            commandes.rapport.CmdRapport(),
        ]

        for cmd in self.commandes:
            self.importeur.interpreteur.ajouter_commande(cmd)

        # Ajout des éditeurs 'bugedit*'
        self.importeur.interpreteur.ajouter_editeur(EdtBugedit)
        self.importeur.interpreteur.ajouter_editeur(EdtBugeditP)

    def creer_rapport(self, titre, createur=None, ajouter=True):
        """Crée un rapport."""
        rapport = Rapport(titre, createur)
        if ajouter:
            self.ajouter_rapport(rapport)

        return rapport

    def ajouter_rapport(self, rapport):
        """Ajoute un rapport."""
        if not rapport.source:
            self.rapports[rapport.id] = rapport
        else:
            self.rapports[rapport.source.id] = rapport
            rapport.id = rapport.source.id
            rapport.source.detruire()
            rapport.source = None

    def joueur_connecte(self, joueur):
        """On avertit du nombre de rapports qui lui sont assignés."""
        rapports = [r for r in self.rapports.values() if r.ouvert and \
                r.assigne_a is joueur]
        if rapports:
            joueur << format_nb(len(rapports), "{nb} rapport{s} vous " \
                    "{est} actuellement assigné{s}.")

    def sauver_traceback(self, joueur, commande, trace):
        """Enregistre le traceback dans le module."""
        self.traces[joueur] = (commande, trace)
        joueur.envoyer_tip("Entrez %bug% pour " \
                "signaler ce bug aux administrateurs.")

    def stats_rapports(self, infos):
        """Ajoute les stats concernant les rapports."""
        tous_rapports = list(self.rapports.values())
        msg = "|tit|Rapports :|ff|"
        for type_rapport in "bug", "évolution", "suggestion":
            e = "" if type_rapport == "bug" else "e"
            rapports = [r for r in tous_rapports if r.type == type_rapport]
            ouverts = [r for r in rapports if r.ouvert]
            assignes = [r for r in rapports if r.assigne_a is not None
                    and r.ouvert]

            msg += "\n  {:<10} : {} ouvert{e}s".format(
                    type_rapport.capitalize() + "s", len(ouverts), e=e)
            if len(rapports):
                msg += " ({:>3}%)".format(
                        int(len(ouverts) / len(rapports) * 100))
            msg += ", {} assigné{e}s, {} en tout".format(
                    len(assignes), len(rapports), e=e)

        infos.append(msg)
