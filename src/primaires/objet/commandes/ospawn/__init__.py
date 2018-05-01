# -*-coding:Utf-8 -*

# Copyright (c) 2010-2017 LE GOFF Vincent
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


"""Package contenant la commande 'ospawn'.

"""

from primaires.interpreteur.commande.commande import Commande

class CmdOspawn(Commande):

    """Commande 'ospawn'.

    """

    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "ospawn", "ospawn")
        self.groupe = "administrateur"
        self.nom_categorie = "batisseur"
        self.schema = "(<nombre>) <ident_prototype_objet> " \
                "(dans/into <conteneur:ident_prototype_objet>)"
        self.aide_courte = "fait apparaître des objets dans la salle"
        self.aide_longue = \
            "Cette commande permet de faire apparaître des objets dans " \
            "la salle où vous vous trouvez. Elle prend en paramètre " \
            "obligatoire le prototype depuis lequel créer l'objet. Vous " \
            "pouvez également préciser le nombre des objets à faire " \
            "apparaître avant le prototype. Enfin, vous pouvez " \
            "préciser, après le prototype, le mot-clé |ent|dans|ff| (ou " \
            "|ent|into|ff| en anglais) et une clé de conteneur pour faire " \
            "apparaître un objet dans un conteneur qui sera créé. Cette " \
            "alternative ne fonctionne que pour les potions et conteneurs " \
            "de potion."

    def interpreter(self, personnage, dic_masques):
        """Interprétation de la commande"""
        prototype = dic_masques["ident_prototype_objet"].prototype
        salle = personnage.salle
        nb_obj = 1
        if dic_masques["nombre"] is not None:
            nb_obj = dic_masques["nombre"].nombre
        if dic_masques["conteneur"]:
            conteneur = dic_masques["conteneur"].prototype

            # On traite ce cas à part
            if not prototype.est_de_type("potion"):
                personnage << "|err|L'objet {} n'est pas de type " \
                        "potion.|ff|".format(prototype.cle)
                return

            if not conteneur.est_de_type("conteneur de potion"):
                personnage << "|err|L'objet {} n'est pas de type " \
                        "conteneur de potion.|ff|".format(conteneur.cle)
                return

            i = 0
            while i < nb_obj:
                objet = importeur.objet.creer_objet(conteneur)
                salle.objets_sol.ajouter(objet)
                objet.potion = importeur.objet.creer_objet(prototype)
                i += 1
        else:
            i = 0
            while i < nb_obj:
                objet = type(self).importeur.objet.creer_objet(prototype)
                salle.objets_sol.ajouter(objet)
                i += 1

        personnage << "Vous faites apparaître {} du néant.".format(
                objet.get_nom(nb_obj))
        salle.envoyer("{{}} fait apparaître {} du néant.".format(
                objet.get_nom(nb_obj)), personnage)
