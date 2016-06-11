# -*-coding:Utf-8 -*

# Copyright (c) 2010-2016 LE GOFF Vincent
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


"""Fichier contenant le paramètre 'placer' de la commande 'cale'."""

import traceback

from primaires.interpreteur.masque.parametre import Parametre

class PrmPlacer(Parametre):

    """Commande 'cale placer'.

    """

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "placer", "in")
        self.schema = "(<nombre>) <nom_objet>"
        self.aide_courte = "place des marchandises en cale"
        self.aide_longue = \
            "Cette commande vous permet de placer certaines marchandises " \
            "en cale. Vous devez disposez des marchandises sur vous. " \
            "Notez que le terme marchandise est utilisé de façon large " \
            "ici (vous pouvez déposer des boulets de canon ou de la " \
            "poudre). Le premier paramètre est optionnel et il s'agit " \
            "du nombre d'objets. Le second paramètre est le nom (ou " \
            "fragment du nom) de l'objet à mettre en cale."

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
        personnage.agir("poser")
        salle = personnage.salle
        if not hasattr(salle, "navire") or salle.navire is None or \
                salle.navire.etendue is None:
            personnage << "|err|Vous n'êtes pas sur un navire.|ff|"
            return

        navire = salle.navire
        cale = navire.cale
        nombre = 1
        if dic_masques["nombre"]:
            nombre = dic_masques["nombre"].nombre

        objets = list(dic_masques["nom_objet"].objets_qtt_conteneurs)[:nombre]
        objets = [c[0] for c in objets]
        objet = objets[0]
        if not cale.accepte(salle, objet.nom_type):
            personnage << "|err|Vous ne pouvez pas faire cela d'ici.|ff|"
            return

        try:
            nombre = cale.ajouter_objets(objets)
        except ValueError as err:
            print(traceback.format_exc())
            personnage << "|err|" + str(err) + "|ff|"
        else:
            personnage << "Vous mettez en cale {}.".format(objet.get_nom(
                    nombre))
