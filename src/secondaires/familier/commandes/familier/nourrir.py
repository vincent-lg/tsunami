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
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT master OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""Fichier contenant le paramètre 'nourrir' de la commande 'familier'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmNourrir(Parametre):

    """Commande 'familier nourrir'."""

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "nourrir", "feed")
        self.tronquer = True
        self.schema = "<nom_familier> <nom_objet>"
        self.aide_courte = "nourrit un familier"
        self.aide_longue = \
            "Cette commande permet de nourrir un familier, en lui " \
            "donnant à manger un objet que vous possédez dans votre " \
            "inventaire. Les familiers ne mangent pas tous la même " \
            "chose, bien entendu. Cette commande est utile pour garder " \
            "un familier en vie même quand vous vous trouvez à un " \
            "endroit où il ne peut trouver de la nourriture par lui-même. " \
            "Le premier paramètre est le nom du familier. Le second " \
            "paramètre est un extrait du nom de l'objet à donner " \
            "à ce familier, se trouvant dans votre inventaire. Par " \
            "exemple, %familier% %familier:nourrir%|cmd| médor pomme " \
            "rouge|ff|."

    def ajouter(self):
        """Méthode appelée lors de l'ajout de la commande à l'interpréteur"""
        nom_objet = self.noeud.get_masque("nom_objet")
        nom_objet.proprietes["conteneurs"] = \
                "(personnage.equipement.inventaire_simple, )"

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        # On récupère le familier
        familier = dic_masques["nom_familier"].familier
        fiche = familier.fiche
        pnj = familier.pnj
        objets = list(dic_masques["nom_objet"].objets_conteneurs)[0]
        objet, conteneur = objets
        personnage.agir("ingérer")
        peut_manger = False
        for aliment in fiche.peut_manger:
            if aliment.startswith("+") and objet.est_de_type(aliment[1:]):
                peut_manger = True
                break
            elif objet.cle == aliment:
                peut_manger = True
                break

        if not peut_manger:
            personnage.envoyer("|err|{{}} ne veut pas manger {}.|ff|".format(
                    objet.get_nom()), pnj)
            return

        if personnage.equipement.cb_peut_tenir() < 1:
            personnage << "|err|Il vous faut au moins une main de libre.|ff|"
            return

        if familier.faim > 0:
            personnage.envoyer("Vous donnez {} à {{}}.".format(
                    objet.get_nom()), pnj)
            message_mange = getattr(objet, "message_mange", "")
            pnj << "Vous mangez {}.\n{}".format(objet.get_nom(),
                    message_mange).strip()
            nourrissant = getattr(objet, "nourrissant", objet.poids * 4) * 5
            familier.diminuer_faim(nourrissant)
            pnj.salle.envoyer("{{}} mange {}.".format(objet.get_nom()),
                    pnj)
            if "mange" in objet.script.evenements:
                objet.script["mange"].executer(personnage=pnj, objet=objet)
            objet.contenu.retirer(objet)
            importeur.objet.supprimer_objet(objet.identifiant)
        else:
            personnage.envoyer("|err|{} ne peut apparemment pas " \
                    "manger davantage.|ff|", pnj)
