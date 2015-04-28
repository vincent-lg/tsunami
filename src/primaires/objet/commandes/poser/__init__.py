# -*-coding:Utf-8 -*

# Copyright (c) 2010 LE GOFF Vincent
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


"""Package contenant la commande 'poser'."""

from primaires.interpreteur.commande.commande import Commande
from primaires.objet.conteneur import SurPoids

class CmdPoser(Commande):

    """Commande 'poser'"""

    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "poser", "drop")
        self.nom_categorie = "objets"
        self.schema = "(<nombre>) <nom_objet> " \
                "(dans/into <conteneur:nom_objet>)"
        self.aide_courte = "pose un objet"
        self.aide_longue = \
                "Cette commande permet de poser un ou plusieurs objets."

    def ajouter(self):
        """Méthode appelée lors de l'ajout de la commande à l'interpréteur"""
        nom_objet = self.noeud.get_masque("nom_objet")
        nom_objet.proprietes["conteneurs"] = \
                "(personnage.equipement.inventaire_simple.iter_objets_qtt(" \
                "True), )"
        nom_objet.proprietes["quantite"] = "True"
        nom_objet.proprietes["conteneur"] = "True"
        conteneur = self.noeud.get_masque("conteneur")
        conteneur.prioritaire = True
        conteneur.proprietes["conteneurs"] = \
                "(personnage.equipement.inventaire_simple, " \
                "personnage.salle.objets_sol)"

    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        personnage.agir("poser")
        nombre = 1
        if dic_masques["nombre"]:
            nombre = dic_masques["nombre"].nombre
        objets = list(dic_masques["nom_objet"].objets_qtt_conteneurs)[:nombre]
        dans = dic_masques["conteneur"]
        dans = dans.objet if dans else None

        pose = 0
        poses = []
        for objet, qtt, conteneur in objets:
            if not objet.peut_prendre:
                personnage << "Vous ne pouvez pas prendre {} avec vos " \
                        "mains...".format(objet.nom_singulier)
                return

            if nombre < qtt:
                qtt = nombre

            if dans and not (dans.est_de_type("conteneur") and \
                    dans.accepte_type(objet) and dans.peut_contenir(
                    objet, qtt)) and not (dans.est_de_type("machine") and \
                    dans.machine_conteneur and dans.peut_contenir(objet, qtt)):
                personnage << "|err|{} ne peut pas contenir {}.|ff|".format(
                        dans.get_nom(), objet.get_nom(qtt))
                return

            if dans and dans.est_de_type("machine"):
                dans.script["entrepose"]["avant"].executer(
                        personnage=personnage, machine=dans, objet=objet)

            if not objet.e_existe:
                continue

            conteneur.retirer(objet, qtt)

            if dans:
                if hasattr(dans, "conteneur"):
                    try:
                        dans.conteneur.ajouter(objet, qtt)
                    except SurPoids as err:
                        personnage << "|err|" + str(err) + ".|ff|"
                        personnage << "|err|{} tombe sur le sol.|ff|".format(
                                objet.get_nom(qtt))
                        personnage.salle.objets_sol.ajouter(objet, qtt)
                        return
            else:
                personnage.salle.objets_sol.ajouter(objet, qtt)

            pose += qtt
            poses.append(objet)
            if pose >= nombre:
                break
            nombre -= qtt
            if nombre <= 0:
                break

        if dans:
            if dans.est_de_type("machine"):
                dans.script["entrepose"]["après"].executer(
                        personnage=personnage, machine=dans, objets=poses)
            else:
                if getattr(dans, "meuble_support", False):
                    connecteur = "sur"
                else:
                    connecteur = "dans"

                personnage << "Vous déposez {} {connecteur} {}.".format(
                        objet.get_nom(pose), dans.nom_singulier,
                        connecteur=connecteur)
                personnage.salle.envoyer("{{}} dépose {} {connecteur} " \
                            "{}.".format(objet.get_nom(pose),
                            dans.nom_singulier, connecteur=connecteur),
                            personnage)
        else:
            personnage << "Vous posez {}.".format(objet.get_nom(pose))
            personnage.salle.envoyer("{{}} pose {}.".format(
                        objet.get_nom(pose)), personnage)

            prototype = objet
            if hasattr(objet, "prototype"):
                prototype = objet.prototype

            prototype.poser(objet, personnage, pose)
