# -*-coding:Utf-8 -*

# Copyright (c) 2013 LE GOFF Vincent
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   raise of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this raise of conditions and the following disclaimer in the documentation
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


"""Fichier contenant le paramètre 'charger' de la commande 'canon'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmCharger(Parametre):

    """Commande 'canon charger'.

    """

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "charger", "load")
        self.schema = "<nom_objet>"
        self.aide_courte = "charge le canon"
        self.aide_longue = \
            "Cette commande permet de charger un canon avec le projectile " \
            "spécifié en paramètre. Vous devez posséder sur vous (dans " \
            "vos mains ou l'un des sacs que vous possédez) le projectile " \
            "spécifié. Si le canon est déjà chargé, l'ancien projectile " \
            "tombera simplement au sol."

    def ajouter(self):
        """Méthode appelée lors de l'ajout de la commande à l'interpréteur"""
        nom_objet = self.noeud.get_masque("nom_objet")
        nom_objet.proprietes["conteneurs"] = \
                "(personnage.equipement.inventaire_simple.iter_objets_qtt(" \
                "True), )"
        nom_objet.proprietes["quantite"] = "True"
        nom_objet.proprietes["conteneur"] = "True"

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        salle = personnage.salle
        personnage.agir("manip_canon")
        projectile, qtt, conteneur = list(dic_masques[ \
                "nom_objet"].objets_qtt_conteneurs)[0]
        canon = None
        if hasattr(salle, "navire"):
            for element in salle.elements:
                if element.nom_type == "canon":
                    canon = element
                    break

        if canon is None:
            personnage << "|err|Aucun canon ne se trouve ici.|ff|"
            return

        if not projectile.est_de_type("boulet de canon"):
            personnage << "|err|{} n'est pas un boulet de canon.|ff|".format(
                    projectile.nom_singulier.capitalize())
            return

        a_projectile = canon.projectile
        if a_projectile:
            salle.objets_sol.ajouter(a_projectile)

        conteneur.retirer(projectile)
        yield canon.pre_charger(personnage)
        canon.post_charger(personnage, projectile)
