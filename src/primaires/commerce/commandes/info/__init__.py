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


"""Package contenant la commande 'info'."""

from primaires.interpreteur.commande.commande import Commande

class CmdInfo(Commande):

    """Commande 'info'"""

    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "info", "info")
        self.nom_categorie = "objets"
        self.schema = "<objet:id_objet_magasin|nom_objet_magasin>"
        self.aide_courte = "affiche des informations surn un produit"
        self.aide_longue = \
            "Cette commande permet d'afficher des informations sur un " \
            "produit vendu par un magasin. Vous pouvez utiliser, comme pour " \
            "la commade %acheter%, soit le nom d'un objet en vente soit son " \
            "|ent|#<numéro>|ff|, comme |ent|#1|ff|. Pour un objet, vous " \
            "pourrez regarder le produit avant de l'acheter, ce qui peut " \
            "parfois être utile. Cette commande donne différentes " \
            "informations en fonction du type de produit en vente."

    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        personnage.agir("regarder")
        salle = personnage.salle
        if salle.magasin is None:
            personnage << "|err|Il n'y a pas de magasin ici.|ff|"
            return


        magasin = salle.magasin
        if magasin.vendeur is None:
            personnage << "|err|Aucun vendeur n'est présent pour l'instant.|ff|"
            return
        no_ligne = dic_masques["objet"].no_ligne
        service, qtt = magasin.inventaire[no_ligne]
        personnage << service.regarder(personnage)
