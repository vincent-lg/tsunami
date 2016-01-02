# -*-coding:Utf-8 -*

# Copyright (c) 2010-2016 LE GOFF Vincent
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


"""Fichier contenant le paramètre 'renommer' de la commande 'orbe'."""

from primaires.format.fonctions import supprimer_accents
from primaires.interpreteur.masque.parametre import Parametre

class PrmRenommer(Parametre):

    """Commande 'orbe renommer."""

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "renommer", "rename")
        self.tronquer = True
        self.schema = "<nom_objet> comme/as <message>"
        self.aide_courte = "renomme un orbe"
        self.aide_longue = \
            "Cette commande permet de renommer un orbe, c'est-à-dire " \
            "changer le nom grâce auquel un autre orbe pourra le " \
            "contacter directement. En d'autre terme, un orbe sans " \
            "nom (ce qui est le cas par défaut) ne pourra pas recevoir " \
            "de message privé. Pour attribuer un nom à un orbe, ou " \
            "changer ce nom, précisez un fragment du nom de l'orbe " \
            "suivi du mot-clé |ent|comme|ff| (ou |ent|as|ff| en " \
            "anglais) puis du nouveau nom. Vous pouvez choisir le " \
            "nom que vous voulez, tant qu'il n'est pas déjà utilisé. " \
            "Gardez à l'esprit qu'il doit être court et que vous " \
            "aurez à le communiquer RP aux joueurs par lesquels vous " \
            "acceptez d'être contacté en RP. Changer le nom de l'orbe " \
            "après coup revient un peu à changer les serrures d'une " \
            "porte : vos anciens correspondants ne sauront pas comment " \
            "vous joindre. Aussi, il peut être utile de choisir un " \
            "nom court, logique et orienté RP que vous puissiez " \
            "transmettre une fois pour toute et ne changerez plus."

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
        message = dic_masques["message"].message
        orbe = objets[0]
        if not orbe.est_de_type("orbe"):
            personnage << "|err|{} n'est pas un orbe.|ff|".format(
                    pavillon.get_nom().capitalize())
            return

        nom = supprimer_accents(message).lower()
        if not supprimer_accents(nom).isalpha():
            personnage << "|err|Le nom {} est invalide.|ff|".format(nom)
            return

        orbes = importeur.objet.get_objets_de_type("orbe")
        noms = [o.nom_orbe for o in orbes]
        if nom in noms:
            personnage << "|err|Ce nom d'orbe est déjà utilisé.|ff|"
            return

        orbe.nom_orbe = nom
        personnage << "{} est à présent nommé {}.".format(orbe.nom_singulier,
                nom)
