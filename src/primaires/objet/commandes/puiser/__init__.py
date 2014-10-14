# -*-coding:Utf-8 -*

# Copyright (c) 2012 NOEL-BARON Léo
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


"""Package contenant la commande 'puiser'."""

from primaires.interpreteur.commande.commande import Commande

class CmdPuiser(Commande):

    """Commande 'puiser'"""

    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "puiser", "draw")
        self.nom_categorie = "objets"
        self.schema = "<nom_objet>"
        self.aide_courte = "puise de l'eau"
        self.aide_longue = \
                "Cette commande remplit d'eau un conteneur adapté, si vous " \
                "vous trouvez dans une salle avec de l'eau à portée de main " \
                "(rive, salle aquatique, ou contenant une fontaine)."

    def ajouter(self):
        """Méthode appelée lors de l'ajout de la commande à l'interpréteur"""
        nom_objet = self.noeud.get_masque("nom_objet")
        nom_objet.proprietes["conteneurs"] = \
                "(personnage.equipement.inventaire, )"
        nom_objet.proprietes["types"] = "('conteneur de potion', )"

    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        personnage.agir("prendre")
        conteneur = dic_masques["nom_objet"].objet
        salle = personnage.salle

        fontaine = salle.a_detail_flag("fontaine")
        if not fontaine and salle.terrain.nom not in ("rive",
                "aquatique", "subaquatique"):
            personnage << "|err|Il n'y a pas d'eau potable par ici.|ff|"
            return
        if conteneur.potion is not None:
            personnage << "|err|{} contient déjà du liquide.|ff|".format(
                    conteneur.get_nom())
            return

        eau = importeur.objet.creer_objet(importeur.objet.prototypes["eau"])
        conteneur.potion = eau
        personnage << "Vous puisez {}.".format(
                conteneur.get_nom())
        personnage.salle.envoyer("{{}} puise {}.".format(
                conteneur.get_nom()), personnage)
