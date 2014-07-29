# -*-coding:Utf-8 -*

# Copyright (c) 2012 EILERS Christoff
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


"""Package contenant la commande 'boire'."""

from primaires.interpreteur.commande.commande import Commande

class CmdBoire(Commande):

    """Commande 'boire'"""

    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "boire", "drink")
        self.nom_categorie = "objets"
        self.schema = "(<nom_objet>)"
        self.aide_courte = "boit une potion"
        self.aide_longue = \
                "Cette commande permet de boire un liquide (potion " \
                "ou autre) depuis un conteneur. Sans argument, vous buvez " \
                "l'eau à portée s'il y en a (près d'une rivière ou autre " \
                "étendue d'eau). Sur un navire, cette commande vous " \
                "permet de boire directement depuis l'eau, si elle est " \
                "douce, ou de boire une partie de vos réserves d'eau " \
                "douce, si il y en a dans la cale."

    def ajouter(self):
        """Méthode appelée lors de l'ajout de la commande à l'interpréteur"""
        nom_objet = self.noeud.get_masque("nom_objet")
        nom_objet.proprietes["conteneurs"] = \
                "(personnage.equipement.inventaire, )"

    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        personnage.agir("ingerer")
        salle = personnage.salle

        if dic_masques["nom_objet"] is None:
            # On regarde si il n'y a pas une fontaine dans les détails
            fontaine = salle.a_detail_flag("fontaine")
            peut = importeur.hook["objet:peut_boire"].executer(personnage)
            if any(peut) or fontaine or salle.terrain.nom in ("rive",
                    "aquatique", "subaquatique"):
                if personnage.estomac <= 2.9:
                    personnage << "Vous buvez à grandes gorgées."
                    personnage.salle.envoyer("{} boit à grandes gorgées.",
                            personnage)
                    if personnage.soif > 0:
                        personnage.soif -= 8
                    personnage.estomac += 0.25
                else:
                    e = "e" if personnage.est_feminin() else ""
                    personnage << "Vous êtes plein{e} ; une gorgée de plus " \
                            "et vous éclaterez.".format(e=e)
            else:
                personnage << "|err|Il n'y a pas d'eau par ici.|ff|"
            return

        objet = dic_masques["nom_objet"].objet
        peut = importeur.hook["objet:peut_boire"].executer(personnage, objet)
        if any(peut):
            peut[0](personnage, objet)
            return

        if hasattr(objet, "potion"):
            if objet.potion is None:
                personnage << "Il n'y a rien à boire là-dedans."
                return

            if personnage.estomac + objet.potion.poids_unitaire <= 3:
                personnage << objet.potion.message_boit
                personnage.salle.envoyer("{} boit " + objet.get_nom() + ".",
                        personnage)
                personnage.soif -= objet.potion.remplissant * 5
                if personnage.soif < 0:
                    personnage.soif = 0
                personnage.estomac += objet.potion.poids_unitaire
                objet.potion.script["boit"].executer(personnage=personnage,
                        objet=objet)
                importeur.objet.supprimer_objet(objet.potion.identifiant)
                objet.potion = None
            else:
                e = "e" if personnage.est_feminin() else ""
                personnage << "Vous êtes plein{e} ; une gorgée de plus " \
                        "et vous éclaterez.".format(e=e)
            return

        personnage << "|err|Vous ne pouvez boire cela.|ff|"
