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


"""Fichier contenant le paramètre 'choisir' de la commande 'orbe'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmChoisir(Parametre):

    """Commande 'orbe choisir'."""

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "choisir", "choose")
        self.tronquer = True
        self.schema = "<nom_objet>"
        self.aide_courte = "choisit un orbe"
        self.aide_longue = \
            "Cette commande est utile quand vous possédez plusieurs " \
            "orbes. Pour sélectionner celui que vous voulez utiliser " \
            "(c'est-à-dire, celui grâce auquel vous pourrez " \
            "communiquer), entrez cette commande suivie simplement " \
            "d'un fragment du nom de l'objet que vous possédez."

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
        objets = list(dic_masques["nom_objet"].objets_qtt_conteneurs)
        objets = [c[0] for c in objets]
        orbe = objets[0]
        if not orbe.est_de_type("orbe"):
            personnage << "|err|{} n'est pas un orbe.|ff|".format(
                    orbe.get_nom().capitalize())
            return

        importeur.communication.orbes.defauts[personnage] = orbe
        personnage << "Votre orbe par défaut est désormais {}.".format(
                orbe.get_nom())
