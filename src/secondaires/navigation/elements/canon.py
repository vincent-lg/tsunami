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


"""Fichier contenant la classe Canon, détaillée plus bas."""

from datetime import datetime
from math import *

from vector import *

from bases.objet.attribut import Attribut
from primaires.perso.exceptions.stat import DepassementStat
from primaires.salle.salle import Salle
from primaires.vehicule.vecteur import Vecteur
from secondaires.navigation.constantes import est_capturable
from .base import BaseElement

# Charge minimum pour que le projectile part
CHARGE_MIN = 2

class Canon(BaseElement):

    """Classe représentant un canon fixe sur un navire.

    Les canons sont soit :
    *   Des éléments statiques (définis ici)
    *   Des objets amovibles.

    """

    nom_type = "canon"

    def __init__(self, cle=""):
        """Constructeur d'un type"""
        BaseElement.__init__(self, cle)
        # Attributs propres aux canons
        self.max_onces = 5
        self._attributs = {
            "h_angle": Attribut(lambda: 0),
            "v_angle": Attribut(lambda: 0),
            "projectile": Attribut(lambda: None),
            "onces": Attribut(lambda: 0),
            "en_cours": Attribut(lambda: False),
            "dernier_tir": Attribut(lambda: None),
        }

    def facteur_charge(self):
        """Retourne le facteur de charge, en pourcent."""
        if self.max_onces == 0:
            return 0

        return self.onces / self.max_onces * 100

    def message_charge(self):
        """Retourne le message correspondant à la charge du canon."""
        messages = [
            (5, "Une explosion assez discrète se fait entendre"),
            (20, "Une explosion assez sonore retentit"),
            (50, "Une explosion assez forte fait frémir le navire"),
            (75, "Une violente détonation fait trembler le navire"),
            (95, "Une détonnation assourdissante fait trembler le " \
                    "bois sous vos pieds"),
        ]

        facteur = self.facteur_charge()
        for t_facteur, message in messages:
            if facteur <= t_facteur:
                return message + "."

        return messages[-1][1] + "."

    def vecteur(self):
        """Retourne le vecteur anticipé de la direction du projectile.

        On se base sur la charge et le poids du projectile pour estimer
        la distance à laquelle le projectile peut être tiré. On se base
        sur l'alignement pour estimer la direction du projectile.

        Sans le nuancer avec la direction du navire et sa position, ce
        vecteur ne peut pas être utilisé.

        """
        # D'abord, on calcule la longueur du vecteur (sa norme)
        vec_nul = Vector(0, 0, 0)
        if self.onces == 0:
            return vec_nul

        if self.projectile is None:
            return vec_nul

        facteur = self.facteur_charge() / 100
        norme = (facteur * 12) / (self.projectile.poids_unitaire / 3)

        # À présent, oriente le vecteur en fonction de l'angle du canon
        vecteur = Vector(1, 0, 0)
        vecteur.mag = norme
        vecteur.around_z(radians(self.h_angle))
        return vecteur

    def cible(self):
        """Retourne la cible du canon.

        La cible est soit :
            Une salle (salle de navire ou non)
            Une côte d'une étendue
            None si rien n'est trouvé comme cible.

        """
        # On calcul le vecteur du boulet
        direction = self.vecteur()

        # On le nuance avec la direction du navire
        salle = self.parent
        if salle is None:
            return (direction, None)

        navire = salle.navire
        if navire is None:
            return (direction, None)

        direction.around_z(radians(navire.direction.direction))
        direction = direction + navire.opt_position
        # On récupère toutes les salles avec coordonnées
        cibles = importeur.salle._coords.copy()
        if navire.etendue:
            etendue = navire.etendue
            for o_coords, obstacle in etendue.obstacles.items():
                cibles[(o_coords + (etendue.altitude, ))] = obstacle

        # On cherche les salles entre origine et destination
        o_vec = Vector(*salle.coords.tuple())
        d_vec = direction
        o_coords = salle.coords.tuple()
        d_coords = (direction.x, direction.y, direction.z)
        points = []
        o_x, o_y, o_z = o_coords
        d_x, d_y, d_z = d_coords
        for coords, point in cibles.items():
            if point is salle:
                continue

            x, y, z = coords
            if in_rectangle(o_x, o_y, o_z, d_x, d_y, d_z, x, y, z, 0.5):
                points.append(((x, y, z), point))

        # On parcourt les points
        trajectoire = []
        for coords, point in points:
            p_vec = Vector(*coords)
            d = o_vec.distance(d_vec, p_vec)
            if d <= 0.5:
                trajectoire.append((coords, point))

        def distance(couple):
            x, y, z = couple[0]
            return mag(x, y, z, o_x, o_y, o_z)

        trajectoire = sorted(trajectoire, key=distance)
        if trajectoire:
            return (direction, trajectoire[0][1])

        return (direction, None)

    def pre_charger(self, personnage):
        """Méthode appelée avant de charger le canon.

        Les paramètres à préciser sont :
            personnage -- le personnage qui veut charger le canon

        """
        personnage.etats.ajouter("charger_canon")
        personnage << "Vous commencez à charger {}.".format(
                self.nom)
        personnage.salle.envoyer("{{}} commence à charger {}.".format(
                self.nom), personnage)
        return 10

    def post_charger(self, personnage, boulet):
        """Méthode appelée quand le boulet est chargé."""
        if "charger_canon" not in personnage.etats:
            return

        personnage.etats.retirer("charger_canon")
        self.projectile = boulet
        personnage << "Vous chargez {} dans {}.".format(
                boulet.get_nom(), self.nom)
        personnage.salle.envoyer("{{}} charge {} dans {}.".format(
                boulet.get_nom(), self.nom), personnage)

    def tirer(self, auteur=None):
        """Le canon tire son projectile."""
        salle_auteur = getattr(auteur, "salle", None)
        if self.onces == 0:
            return

        if self.projectile is None:
            return

        vecteur, cible = self.cible()
        if self.parent and self.parent.navire:
            vecteur = self.parent.navire.opt_position - vecteur

        distance = vecteur.mag
        temps = distance / 15
        msg = self.message_charge()
        if self.parent:
            self.parent.envoyer(msg)
        projectile = self.projectile
        self.projectile = None
        self.onces = 0
        self.dernier_tir = datetime.now()
        if temps <= 0.5:
            self.endommager(projectile, cible, auteur=salle_auteur)
        else:
            importeur.diffact.ajouter_action("canon_" + str(id(self)),
                    temps, self.endommager, projectile, cible,
                    auteur=salle_auteur)
            self.en_cours = True

    def endommager(self, projectile, cible, auteur=None):
        """Endommage la cible."""
        self.en_cours = False
        adverse = self.parent.navire
        if cible is None:
            if auteur:
                auteur.envoyer("{} se perd sans faire de dégâts.".format(
                        projectile.nom_singulier.capitalize()))

            importeur.objet.supprimer_objet(projectile.identifiant)
            return None

        if isinstance(cible, Salle):
            navire = getattr(cible, "navire", None)
            equipage = getattr(navire, "equipage", None)
            points = equipage and equipage.points_actuels or None
            titre = cible.titre
            cible.envoyer(
                    "|rg|" + projectile.nom_singulier.capitalize() + \
                    " détonne près de vous !|ff|")
            degats = projectile.degats
            if degats > 0:
                for personnage in cible.personnages:
                    try:
                        personnage.stats.vitalite -= degats
                    except DepassementStat:
                        personnage.mourir()
                        personnage << "Vous vous écroulez sous l'effet " \
                                "de la douleur.|ff|"
                        personnage.salle.envoyer("{} s'effondre sous " \
                                "l'effet de la douleur.", personnage)

            projectile.script["atteint"].executer(objet=projectile,
                    salle=cible)

            # Inflige des dégâts au navire
            if navire and not navire.immobilise:
                navire.envoyer("|rg|{}  détonne {}.|ff|".format(
                        projectile.nom_singulier.capitalize(),
                        cible.titre_court), exceptions=[cible], prompt=False)

                cible.noyer(int(degats / 2))
                cible.navire.equipage.ajouter_ennemi(adverse)

            futurs = equipage and equipage.points_actuels or None
            if points is not None and futurs is not None and not \
                    est_capturable(navire, points) and est_capturable(
                    navire, futurs):
                for personnage in adverse.personnages:
                    personnage.envoyer_tip("Vous pouvez maintenant " \
                            "aborder et conquérir {}.".format(
                            navire.desc_survol))
        else:
            titre = cible.desc_survol

        if auteur:
            auteur.envoyer("{} atteint {} !".format(
                    projectile.nom_singulier.capitalize(), titre.lower()))
        importeur.objet.supprimer_objet(projectile.identifiant)

    def construire(self, parent):
        """Construit l'élément basé sur le parent."""
        if parent.sabord_min:
            self.h_angle = parent.sabord_min

    def get_description_ligne(self, personnage):
        """Retourne une description d'une ligne de l'élément."""
        cote = " tribord"
        h_angle = self.h_angle
        if h_angle == 0:
            cote = ""
        elif h_angle < 0:
            cote = " bâbord"
            h_angle = -h_angle

        return self.nom.capitalize() + " est orienté de {}°{}.".format(
                h_angle, cote)

    def regarder(self, personnage):
        """personnage regarde self."""
        msg = BaseElement.regarder(self, personnage)
        cote = " tribord"
        h_angle = self.h_angle
        if h_angle == 0:
            cote = ""
        elif h_angle < 0:
            cote = " bâbord"
            h_angle = -h_angle

        msg += "\nIl est orienté sur {}°{}.".format(h_angle, cote)
        msg += "\n" + self.msg_charge()
        msg += "\n" + self.msg_projectile()
        return msg

    def msg_charge(self):
        """Retourne le message de charge du canon."""
        facteur = self.facteur_charge()
        messages = [
            (0, "Ce canon ne contient pas la moindre once de poudre"),
            (5, "Ce canon contient quelques grains de poudre"),
            (10, "Ce canon est chargé très légèrement en poudre"),
            (20, "Ce canon est sensiblement chargé en poudre"),
            (30, "Ce canon est chargé au tiers en poudre"),
            (40, "Ce canon est chargé à un peu plus du tiers en poudre"),
            (50, "Ce canon est chargé à à peu près la moitié en poudre"),
            (60, "Ce canon est chargé à près des deux tiers en poudre"),
            (75, "Ce canon est chargé à près des trois quarts en poudre"),
            (85, "Ce canon est presque entièrement chargé en poudre"),
            (100, "Ce canon est chargé en poudre jusqu'à la gueule"),
        ]

        for hauteur, message in messages:
            if facteur <= hauteur:
                return message + "."

        return messages[0][1] + "."

    def msg_projectile(self):
        """Retourne le message du projectile."""
        if self.projectile:
            return "Ce canon est chargé avec {}.".format(
                    self.projectile.get_nom())

        return "Ce canon ne contient aucun projectile."
