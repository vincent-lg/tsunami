# -*-coding:Utf-8 -*

# Copyright (c) 2010-2016 LE GOFF Vincent
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


"""Fichier contenant le type 'arme de jet'."""

from primaires.interpreteur.editeur.entier import Entier
from primaires.interpreteur.editeur.selection import Selection
from bases.objet.attribut import Attribut
from .arme import Arme

class ArmeDeJet(Arme):

    """Type d'objet: arme de jet."""

    nom_type = "arme de jet"
    cle_talent = "maniement_arc"
    nom_talent = "maniement des armes de jet"
    difficulte_talent = 0.34
    def __init__(self, cle=""):
        """Constructeur de l'objet"""
        Arme.__init__(self, cle)
        self.peut_depecer = False
        self.force_necessaire = 5
        self.projectiles_autorises = []
        self.etendre_editeur("fo", "force minimum nécessaire", Entier, self,
                "force_necessaire", 1)
        cles_projectiles = [prototype.cle for prototype in \
                importeur.objet.prototypes.values() if prototype.est_de_type(
                "projectile")]
        self.etendre_editeur("pr", "projectiles autorisés", Selection,
                self, "projectiles_autorises", cles_projectiles)

        self._attributs = {
            "projectile": Attribut(),
        }

    @property
    def str_projectiles_autorises(self):
        return ", ".join(sorted(self.projectiles_autorises))

    def travailler_enveloppes(self, enveloppes):
        """Travail sur les enveloppes"""
        Arme.travailler_enveloppes(self, enveloppes)
        force = enveloppes["fo"]
        force.apercu = "{objet.force_necessaire}"
        force.prompt = "Force minimum nécessaire pour bander l'arme : "
        force.aide_courte = \
            "Entrez la |ent|force minimum nécessaire|ff| pour bander " \
            "l'arme\nou |cmd|/|ff| pour revenir à la fenêtre parente.\n\n" \
            "Force minimum actuelle : {objet.force_necessaire}"

        projectiles = enveloppes["pr"]
        projectiles.apercu = "{objet.str_projectiles_autorises}"
        projectiles.prompt = "Clé d'un projectile : "
        projectiles.aide_courte = \
            "Entrez une |ent|clé d'un projectile|ff| correspondant à " \
            "cette arme\nou |cmd|/|ff| pour revenir à la fenêtre " \
            "parente.\n\n" \
            "Entrez une clé pour l'ajouter ou pour la supprimer.\n\n" \
            "Projectiles actuels : {objet.str_projectiles_autorises}"
        cles_projectiles = [prototype.cle for prototype in \
                importeur.objet.prototypes.values() if prototype.est_de_type(
                "projectile")]
        projectiles.sup = (cles_projectiles, )

    def etendre_script(self):
        """Extension du scripting."""
        # Évènement charge
        evt_charge = self.script.creer_evenement("charge")
        evt_charge.aide_courte = "le personnage charge l'arme de jet"
        evt_charge.aide_longue = \
            "Cet évènement est appelé quand un personnage charge l'arme de " \
            "avec un projectile en utilisant la commande charger/bend. " \
            "Cet évènement est appelé avant que le retour de la commande ne " \
            "s'affiche aux joueurs, vous pouvez donc interrompre le " \
            "processus avec l'action interrompre."
        var_perso = evt_charge.ajouter_variable("personnage", "Personnage")
        var_perso.aide = "le personnage chargeant l'arme"
        var_arme = evt_charge.ajouter_variable("arme", "Objet")
        var_arme.aide = "l'arme de jet que l'on charge"
        var_projectile = evt_charge.ajouter_variable("projectile", "Objet")
        var_projectile.aide = "le projectile que l'on charge sur l'arme"

        # Évènement décoche
        evt_decoche = self.script.creer_evenement("décoche")
        evt_decoche.aide_courte = "un personnage décharge l'arme de jet"
        evt_decoche.aide_longue = \
            "Cet évènement est appelé quand un personnage décharge " \
            "l'arme de jet sur une cible, présente dans la salle ou " \
            "distante. Il est appelé après que le message informant les " \
            "personnages présents que la flèche s'envole est parti, mais " \
            "avant que la flèche ne parte de la salle où n'atteigne " \
            "la cible. Vous pouvez contrôler de façon plus fine la façon " \
            "dont la flèche est gérée en scriptant la flèche-même."
        var_perso = evt_decoche.ajouter_variable("personnage", "Personnage")
        var_perso.aide = "le personnage déchargeant l'arme"
        var_cible = evt_decoche.ajouter_variable("cible", "Personnage")
        var_cible.aide = "la cible désignée par le tir"
        var_arme = evt_decoche.ajouter_variable("arme", "Objet")
        var_arme.aide = "l'arme de jet que l'on décharge"
        var_projectile = evt_decoche.ajouter_variable("projectile", "Objet")
        var_projectile.aide = "le projectile qui est déchargé de l'arme"

    def objets_contenus(self, conteneur):
        """Retourne les objets contenus."""
        objets = []
        if conteneur.projectile:
            objet = conteneur.projectile
            objets.append(objet)
            if objet.unique:
                objets.extend(objet.prototype.objets_contenus(objet))

        return objets

    # Actions sur les objets
    def regarder(self, personnage):
        """Le personnage regarde l'objet"""
        msg = Arme.regarder(self, personnage)
        msg += "\n\n"
        if getattr(self, "projectile", None):
            msg += "Projectile :  {}.".format(self.projectile.get_nom())
        else:
            msg += "Aucun projectile n'est chargé sur cette arme."

        return msg
