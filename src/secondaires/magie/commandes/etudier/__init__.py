# -*-coding:Utf-8 -*

# Copyright (c) 2013 LE GOFF Vincent
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


"""Package contenant la commande 'étudier'."""

from primaires.interpreteur.commande.commande import Commande

class CmdEtudier(Commande):

    """Commande 'étudier'.

    """

    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "étudier", "study")
        self.schema = "<nom_objet>"
        self.aide_courte = "étudie un grimoire"
        self.aide_longue = \
            "Cette commande vous permet d'étudier un grimoire. Les " \
            "grimoires permettent d'apprendre des sorts. Vous devez " \
            "pour cela l'avoir dans votre inventaire et l'étudier avec " \
            "cette commande. Si vous n'êtes pas du bon élément pour " \
            "étudier ce grimoire, vous récupérerez les points de " \
            "tribut du sort."


    def ajouter(self):
        """Méthode appelée lors de l'ajout de la commande à l'interpréteur"""
        nom_objet = self.noeud.get_masque("nom_objet")
        nom_objet.proprietes["conteneurs"] = \
                "(personnage.equipement.inventaire_simple.iter_objets_qtt(" \
                "True), )"
        nom_objet.proprietes["quantite"] = "True"
        nom_objet.proprietes["conteneur"] = "True"

    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        objets = list(dic_masques["nom_objet"].objets_qtt_conteneurs)[0]
        grimoire, qtt, conteneur = objets
        personnage.agir("etudiersort")

        if not grimoire.est_de_type("grimoire"):
            personnage << "|err|{} n'est pas un grimoire.|ff|".format(
                    grimoire.get_nom().capitalize())
            return

        proprietaire = getattr(grimoire, "proprietaire", None)
        if proprietaire is not personnage:
            personnage << "|err|Vous n'êtes pas le propriétaire de " \
                    "ce grimoire.|ff|"
            return

        sort = grimoire.sort
        if sort.cle in personnage.sorts and sort.cle not in \
                personnage.sorts_verrouilles:
            personnage << "|err|Vous connaissez déjà ce sort.|ff|"
            return

        points = sort.points_tribut
        if personnage.points_tribut < points:
            personnage << "|err|Vous n'avez pas assez de points de " \
                    "tribut pour étudier ce grimoire.|ff|"
            return

        if sort.elements[0] != personnage.element:
            personnage.points_tribut += points
            s = "s" if points > 1 else ""
            personnage.envoyer("Vous étudiez {{}} et récupérez {} point{s} " \
                    "de tribut.".format(points, s=s), grimoire.get_nom())
        else:
            if sort.cle not in personnage.sorts:
                personnage.sorts[sort.cle] = 1
                niveau = 1
            else:
                niveau = personnage.sorts[sort.cle]
                if sort.cle in personnage.sorts_verrouilles:
                    personnage.sorts_verrouilles.remove(sort.cle)
            msg = \
                "Vous étudiez {}.\n" \
                "Vous connaissez à présent le sort {} à {}% !".format(
                grimoire.get_nom(), sort.nom, niveau)
            personnage << msg
            personnage.points_tribut -= points

        conteneur.retirer(grimoire)
        importeur.objet.supprimer_objet(grimoire.identifiant)
