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


"""Package contenant la commande 'dégainer'."""

from primaires.interpreteur.commande.commande import Commande

class CmdDegainer(Commande):

    """Commande 'dégainer'"""

    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "degainer", "unsheathe")
        self.nom_categorie = "objets"
        self.schema = "<nom_objet>"
        self.aide_courte = "dégaine une arme"
        self.aide_longue = \
                "Cette commande vous permet de dégainer une arme " \
                "que vous possédez dans un fourreau équipé. Le premier " \
                "et unique paramètre est le nom du fourreau (pas " \
                "le nom de l'arme). Vous devez posséder une main de " \
                "libre au minimum pour faire cette action. L'arme " \
                "dégainée sera automatiquement équipée."

    def ajouter(self):
        """Méthode appelée lors de l'ajout de la commande à l'interpréteur"""
        nom_objet = self.noeud.get_masque("nom_objet")
        nom_objet.proprietes["conteneurs"] = \
                "(personnage.equipement.equipes, )"
        nom_objet.proprietes["heterogene"] = "True"

    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        personnage.agir("degainer")
        fourreau_trouve = False
        for fourreau in dic_masques["nom_objet"].objets:
            if fourreau.est_de_type("armure") and fourreau.fourreau:
                fourreau_trouve = True
                break
        if not fourreau_trouve:
            personnage << "|err|{} n'est pas un fourreau.|ff|".format(
                    dic_masques["nom_objet"].objet.nom_singulier)
            return

        arme = fourreau.au_fourreau
        if arme is None:
            personnage << "|err|Ce fourreau ne contient aucune arme.|ff|"
            return

        libre = None
        for membre in personnage.equipement.membres:
            if membre.peut_equiper(arme):
                libre = membre
                break

        if libre is None:
            personnage << "|err|Vous ne disposez d'aucune main de libre.|ff|"
            return

        fourreau.au_fourreau = None
        libre.equipe.append(arme)
        arme.contenu = personnage.equipement.equipes
        personnage << "Vous dégainez {}.".format(arme.get_nom())
        personnage.salle.envoyer("{{}} dégaine {}.".format(arme.get_nom()),
                personnage)
