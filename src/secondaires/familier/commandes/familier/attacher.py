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


"""Fichier contenant le paramètre 'attacher' de la commande 'familier'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmAttacher(Parametre):

    """Commande 'familier attacher'."""

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "attacher", "tie")
        self.tronquer = True
        self.schema = "<nom_familier>"
        self.aide_courte = "attache un familier"
        self.aide_longue = \
            "Cette commande permet d'attacher un familier à une barre " \
            "d'attache disponible dans la salle. Le familier attaché ne " \
            "pourra pas bouger. Il doit être harnaché (d'une bride " \
            "ou corde) et il doit y avoir une barre d'attache libre " \
            "dans la salle. Attention cependant : un familier attaché ne " \
            "se nourrira pas. Ne le laissez pas attaché trop " \
            "longtemps ou bien surveillez son statut de temps à " \
            "autre pour être sûr qu'il ne dépérit pas."

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        salle = personnage.salle
        # On récupère le familier
        familier = dic_masques["nom_familier"].familier
        fiche = familier.fiche
        pnj = familier.pnj
        personnage.agir("attacherfamilier")
        if personnage.equipement.cb_peut_tenir() < 1:
            personnage << "|err|Il vous faut au moins une main libre.|ff|"
            return

        laisse = familier.get_harnachement("laisse", "bride")
        if laisse is None:
            personnage.envoyer("|err|{} n'est pas convenablement " \
                    "harnaché.|ff|", pnj)
            return

        pris = []
        for perso in salle.personnages:
            if "attache" in perso.etats:
                etat = personnage.etats.get("attache")
                pris.append(etat.barre_attache)

        libres = []
        for objet in salle.objets_sol:
            if objet.est_de_type("barre d'attache") and objet not in pris:
                libres.append(objet)

        if len(libres) == 0:
            personnage << "|err|Il n'y a aucune barre d'attache " \
                    "disponible ici.|ff|"
            return

        libre = libres[0]
        pnj.etats.ajouter("attache", libre)
        personnage.envoyer_lisser("Vous attachez {{}} à {}.".format(
                libre.get_nom()), pnj)
        personnage.salle.envoyer_lisser("{{}} attache {{}} à {}.".format(
                libre.get_nom()), personnage, pnj)
