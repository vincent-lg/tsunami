# -*-coding:Utf-8 -*

# Copyright (c) 2010-2017 LE GOFF Vincent
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


"""Fichier contenant le paramètre 'poudre' de la commande 'canon'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmPoudre(Parametre):

    """Commande 'canon poudre'.

    """

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "poudre", "powder")
        self.schema = "(<nombre>) <nom_objet>"
        self.aide_courte = "charge le canon en poudre"
        self.aide_longue = \
            "Cette commande permet de charger le canon en poudre. " \
            "Vous devez pour cela posséder un sac de poudre (soit " \
            "entre vos mains, soit dans un sac que vous portez). Le " \
            "sac de poudre sera prélevé pour charger le canon mais " \
            "tout le sac ne sera pas utilisé, sauf si vous le précisez. " \
            "Par défaut, une once de poudre est prélevée du sac et sert " \
            "à charger le canon, mais vous pouvez préciser, avant " \
            "le nom du sac, une valeur plus grande d'onces (par exemple " \
            "%canon% %canon:poudre% |ent|5 sac de poudre|ff| pour charger " \
            "le canon avec 5 onces de poudre). En fonction de la puissance " \
            "et la capacité du canon, la quantité de poudre nécessaire " \
            "varie (elle est aussi fonction du poids du boulet utilisé)."

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
        nombre = dic_masques["nombre"] and dic_masques["nombre"].nombre or 1
        sac_poudre, qtt, conteneur = list(dic_masques[ \
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

        if not sac_poudre.est_de_type("sac de poudre"):
            personnage << "|err|{} n'est pas un sac de poudre.|ff|".format(
                    sac_poudre.nom_singulier.capitalize())
            return

        if sac_poudre.onces_contenu < nombre:
            personnage << "|err|{} ne contient pas autant d'onces de " \
                    "poudre.|ff|".format(sac_poudre.get_nom())
            return

        if canon.max_onces <= canon.onces:
            personnage << "|err|{} est déjà chargé jusqu'à la " \
                    "gueule.|ff|".format(canon.nom)
            return

        if nombre > canon.max_onces - canon.onces:
            nombre = canon.max_onces - canon.onces

        if nombre == 1:
            msg = "une once de poudre dans {}.".format(canon.nom)
        else:
            msg = "{} onces de poudre dans {}.".format(nombre, canon.nom)

        canon.onces += nombre
        sac_poudre.onces_contenu -= nombre
        personnage << "Vous versez " + msg
        salle.envoyer("{} verse " + msg, personnage)
