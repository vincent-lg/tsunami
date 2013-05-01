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


"""Package contenant la commande 'bander'.

"""

from primaires.interpreteur.commande.commande import Commande
from primaires.objet.conteneur import SurPoids

class CmdBander(Commande):

    """Commande 'bander'.

    """

    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "charger", "bend")
        self.nom_categorie = "combat"
        self.schema = "<jet:nom_objet> (avec/with <projectile:nom_objet>)"
        self.aide_courte = "charge une arme de jet"
        self.aide_longue = \
            "Cette commande permet de charger une arme de jet que " \
            "vous équipez. Elle prend en paramètre obligatoire le " \
            "nom de l'arme. Si rien n'est précisé ensuite, le système " \
            "cherchera le bon projectile dans vos conteneurs équipés " \
            "et le placera automatiquement sur l'arme de jet. Sinon, " \
            "vous pouvez préciser après le nom de l'arme de jet le " \
            "mot-clé |cmd|avec|ff| (ou |cmd|with|ff| en anglais) suivi " \
             "du nom du projectile. Vous devez dans tous les cas " \
             "posséder le projectile indiqué."

    def ajouter(self):
        """Méthode appelée lors de l'ajout de la commande à l'interpréteur"""
        arme_de_jet = self.noeud.get_masque("jet")
        arme_de_jet.proprietes["conteneurs"] = \
            "(personnage.equipement.equipes, )"
        projectile = self.noeud.get_masque("projectile")
        projectile.proprietes["conteneurs"] = \
                "(personnage.equipement.inventaire_simple.iter_objets_qtt(" \
                "True), )"
        projectile.proprietes["quantite"] = "True"
        projectile.proprietes["conteneur"] = "True"

    def interpreter(self, personnage, dic_masques):
        """Interprétation de la commande"""
        personnage.agir("charger")
        arme_de_jet = dic_masques["jet"].objet
        if not arme_de_jet.est_de_type("arme de jet"):
            personnage << "|err|Ceci n'est pas une arme de jet.|ff|"
            return

        if dic_masques["projectile"]:
            projectiles = list(dic_masques["projectile"].objets_qtt_conteneurs)
            projectile, qtt, conteneur = projectiles[0]
            if not projectile.est_de_type("projectile"):
                personnage << "|err|Ceci n'est pas un projectile.|ff|"
                return
        else:
            projectile = conteneur = None
            for objet in personnage.equipement.inventaire:
                if objet.est_de_type("projectile") and objet.cle in \
                        arme_de_jet.projectiles_autorises:
                    projectile = objet
                    conteneur = objet.contenu
                    break

            if projectile is None or conteneur is None:
                personnage << "|err|Aucun projectile pour cette arme " \
                        "de jet ne peut être trouvée sur vous.|ff|"
                return

        if projectile.cle not in arme_de_jet.projectiles_autorises:
            personnage << "|err|Vous ne pouvez utiliser {} avec " \
                    "{}.|ff|".format(arme_de_jet.get_nom(),
                    projectile.get_nom())

        personnage << "Vous commencez à recharger {}.".format(
                arme_de_jet.get_nom())
        personnage.cle_etat = "charger"
        yield 1
        personnage.cle_etat = ""

        # Si l'arme de jet est déjà chargée
        if arme_de_jet.projectile:
            ancien_projectile = arme_de_jet.projectile
            try:
                personnage.ramasser(objet=ancien_projectile)
            except SurPoids:
                personnage.salle.objets_sol.ajouter(objet=ancien_projectile)
                personnage << "{} glisse à terre.".format(
                        ancien_projectile.get_nom().capitalize())
            else:
                personnage << "Vous récupérez {}.".format(
                        ancien_projectile.get_nom())

            arme_de_jet.projectile = None

        conteneur.retirer(projectile)
        arme_de_jet.script["charge"].executer(personnage=personnage,
                arme=arme_de_jet, projectile=projectile)
        arme_de_jet.projectile = projectile
        personnage << "Vous bandez {} avec {}.".format(
                arme_de_jet.get_nom(), projectile.get_nom())
        personnage.salle.envoyer("{{}} bande {} avec {}.".format(
                arme_de_jet.get_nom(), projectile.get_nom()), personnage)
