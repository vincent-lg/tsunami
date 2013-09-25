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


"""Package contenant la commande 'rengainer'."""

from primaires.interpreteur.commande.commande import Commande

class CmdRengainer(Commande):

    """Commande 'rengainer'"""

    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "rengainer", "sheathe")
        self.nom_categorie = "objets"
        self.schema = "<nom_objet> " \
                "(dans/into <conteneur:nom_objet>)"
        self.aide_courte = "rengaine une arme"
        self.aide_longue = \
                "Cette commande vous permet de rengainer une arme " \
                "que vous équipez ou possédez sur vous. Le premier " \
                "paramètre est le nom de l'arme. Vous pouvez préciser " \
                "le nom d'un fourreau après le mot-clé |ent|dans|ff| " \
                "(|ent|into|ff| en anglais). Notez que tous les types " \
                "d'arme ne peuvent pas être placées dans n'importe " \
                "quel fourreau. Le poids de l'arme entre également en " \
                "compte. Une fois rengainée, l'arme sera visible dans " \
                "le fourreau, soit en le regardant, soit directement " \
                "dans votre équipement. Certains fourreaux dissimulent " \
                "volontairement les objets qu'ils contiennent, ce qui " \
                "vous permet de dissimuler vos armes à portée de main " \
                "sans que les autres personnages puissent les voir " \
                "sur vous."

    def ajouter(self):
        """Méthode appelée lors de l'ajout de la commande à l'interpréteur"""
        nom_objet = self.noeud.get_masque("nom_objet")
        nom_objet.proprietes["conteneurs"] = \
                "(personnage.equipement.inventaire.iter_objets_qtt(" \
                "True), )"
        nom_objet.proprietes["quantite"] = "True"
        nom_objet.proprietes["conteneur"] = "True"
        conteneur = self.noeud.get_masque("conteneur")
        conteneur.proprietes["conteneurs"] = \
                "(personnage.equipement.equipes, )"

    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        personnage.agir("rengainer")
        arme, qtt, conteneur_arme = list(dic_masques[
                "nom_objet"].objets_qtt_conteneurs)[0]
        if not arme.est_de_type("arme"):
            personnage << "|err|Vous ne pouvez mettre {} au " \
                    "fourreau.|ff|".format(arme.get_nom())
            return

        if dic_masques["conteneur"]:
            fourreau = dic_masques["conteneur"].objet
        else:
            # On recherche un fourreau disponible
            fourreaux = [membre.equipe[-1] for membre in \
                    personnage.equipement.membres if len(membre.equipe) > 0]
            fourreaux = [objet for objet in fourreaux if objet and \
                    objet.est_de_type("armure")]
            fourreaux = [fourreau for fourreau in fourreaux if \
                    fourreau.fourreau and fourreau.au_fourreau is None]
            fourreaux = [fourreau for fourreau in fourreaux if \
                    fourreau.poids_max_fourreau >= arme.poids_unitaire]
            fourreaux = [fourreau for fourreau in fourreaux if \
                    arme.nom_type in fourreau.types_fourreau]
            if len(fourreaux) == 0:
                personnage << "|err|Aucun fourreau n'est prêt à " \
                        "recevoir {}.|ff|".format(arme.get_nom())
                return

            fourreau = fourreaux[0]

        if not fourreau.est_de_type("armure") or not fourreau.fourreau:
            personnage << "|err|{} n'est pas un fourreau.|ff|".format(
                    fourreau.nom_singulier.capitalize())
            return

        if fourreau.au_fourreau is not None:
            personnage << "|err|{} contient déjà une arme.|ff|".format(
                    fourreau.nom_singulier.capitalize())
            return

        if arme.nom_type not in fourreau.types_fourreau or \
                arme.poids_unitaire > fourreau.poids_max_fourreau:
            personnage << "|err|{} ne peut accueillir {}.|ff|".format(
                    fourreau.nom_singulier.capitalize(), arme.get_nom())
            return

        conteneur_arme.retirer(arme, 1)
        fourreau.au_fourreau = arme
        personnage << "Vous rengainez {} dans {}.".format(
                arme.get_nom(), fourreau.nom_singulier)
        personnage.salle.envoyer("{{}} rengaine {} dans {}.".format(
                arme.get_nom(), fourreau.nom_singulier), personnage)
