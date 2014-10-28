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
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""Package contenant la commande 'éteindre'."""

from datetime import datetime

from corps.fonctions import lisser
from primaires.interpreteur.commande.commande import Commande

class CmdEteindre(Commande):

    """Commande 'éteindre'"""

    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "éteindre", "extinguish")
        self.nom_categorie = "objets"
        self.schema = "<nom_objet>"
        self.aide_courte = "éteint une lumière"
        self.aide_longue = \
                "Cette commande vous permet d'éteindre une lumière. " \
                "Vous devez préciser en paramètre le nom de l'objet. " \
                "Vous pourrez ensuite la rallumer si besoin, si il " \
                "vous reste de la mèche (ou autre combustible)."

    def ajouter(self):
        """Méthode appelée lors de l'ajout de la commande à l'interpréteur"""
        nom_objet = self.noeud.get_masque("nom_objet")
        nom_objet.proprietes["conteneurs"] = \
                "(personnage.equipement.inventaire, )"

    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        objet = dic_masques["nom_objet"].objet
        personnage.agir("eclairer")
        if not objet.est_de_type("lumière"):
            personnage << "|err|{} n'est pas une lumière.|ff|".format(
                    objet.get_nom().capitalize())
            return

        if not objet.allumee_depuis:
            e = "" if objet.masculin else "e"
            personnage << "{} n'est pas allumé{e}.".format(
                    objet.get_nom(), e=e)
            return

        mtn = datetime.now()
        secondes = (mtn - objet.allumee_depuis).total_seconds()
        if objet.duree is None:
            objet.duree = 0

        objet.duree += secondes / 60
        objet.allumee_depuis = None
        objet.script["éteint"].executer(objet=objet, personnage=personnage)
