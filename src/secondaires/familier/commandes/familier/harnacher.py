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


"""Fichier contenant le paramètre 'harnacher' de la commande 'familier'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmHarnacher(Parametre):

    """Commande 'familier harnacher'."""

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "harnacher", "harness")
        self.tronquer = True
        self.schema = "<nom_familier> <nom_objet>"
        self.aide_courte = "harnache un familier"
        self.aide_longue = \
            "Cette commande permet d'harnacher un familier, " \
            "c'est-à-dire de l'équiper avec un objet que vous possédez. " \
            "Ce peut être une bride, une selle ou autre. Certains " \
            "harnachements sont requis pour certaines actions (par " \
            "exemple, on ne peut mener un familier sans bride ou " \
            "corde). Vous devez préciser en premier paramètre le " \
            "nom du familier et en second paramètre un fragment " \
            "du nom de l'objet que vous souhaitez utiliser pour l'harnacher."

    def ajouter(self):
        """Méthode appelée lors de l'ajout de la commande à l'interpréteur"""
        nom_objet = self.noeud.get_masque("nom_objet")
        nom_objet.proprietes["conteneurs"] = \
                "(personnage.equipement.inventaire_simple, )"

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        # On récupère le familier
        familier = dic_masques["nom_familier"].familier
        fiche = familier.fiche
        pnj = familier.pnj
        objets = list(dic_masques["nom_objet"].objets_conteneurs)[0]
        objet, conteneur = objets
        personnage.agir("porter")
        if not objet.est_de_type("harnachement"):
            personnage << "{} n'est pas un harnachement.".format(
                    objet.get_nom().capitalize())
            return

        for harnachement in objet.types_harnachement:
            if harnachement not in fiche.harnachements:
                personnage.envoyer("|err|Vous ne pouvez harnacher {} sur " \
                        "{{}}|ff|.".format(objet.get_nom()), pnj)
                return

        if personnage.equipement.cb_peut_tenir() < 1:
            personnage << "|err|Il vous faut au moins une main libre.|ff|"
            return

        for membre in pnj.equipement.membres:
            if membre.peut_equiper(objet):
                objet.contenu.retirer(objet)
                membre.equiper(objet)
                personnage.envoyer("Vous harnachez {{}} avec {}.".format(
                        objet.get_nom()), pnj)
                personnage.salle.envoyer("{{}} harnache {{}} avec {}.".format(
                    objet.get_nom()), personnage, pnj)
                return

        personnage << "|err|Vous ne pouvez harnacher {}.|ff|".format(
                objet.get_nom())
