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


"""Fichier contenant la classe Navire, détaillée plus bas."""

from math import fabs, radians, sqrt

from vector import *

from abstraits.obase import BaseObj
from primaires.perso.exceptions.stat import DepassementStat
from primaires.vehicule.force import Force
from primaires.vehicule.vecteur import *
from primaires.vehicule.vehicule import Vehicule
from secondaires.navigation.equipage import Equipage
from .constantes import *
from .element import Element
from .salle import SalleNavire
from .vent import INFLUENCE_MAX
from .constantes import END_VIT_RAMES, TERRAINS_QUAI

# Constantes
FACTEUR_MIN = 0.1

class Navire(Vehicule):

    """Classe représentant un navire ou une embarcation.

    Un navire est un véhicule se déplaçant sur une éttendue d'eau,
    propulsé par ses voiles ou des rameurs.

    Le navire est un véhicule se déplaçant sur un repère en 2D.

    Chaque navire possède un modèle (qui détermine ses salles, leurs
    descriptions, la position des éléments, leur qualité, l'aérodynamisme
    du navire...). Chaque navire est lié à son modèle en se créant.

    """

    enregistrer = True
    def __init__(self, modele):
        """Constructeur du navire."""
        Vehicule.__init__(self)
        self.propulsion = Propulsion(self)
        self.forces.append(self.propulsion)
        self.etendue = None
        self.equipage = Equipage(self)
        self.immobilise = False
        self.modele = modele
        self.proprietaire = None
        self.nom_personnalise = ""

        # Dernier lien (dl)
        self.dl_x = 0
        self.dl_y = 0

        if modele:
            modele.vehicules.append(self)
            self.cle = importeur.navigation.dernier_ID(modele.cle)
            self.construire_depuis_modele()

    def __getnewargs__(self):
        return (None, )

    def __repr__(self):
        return "<Navire {}>".format(self.cle)

    @property
    def taille(self):
        """Retourne la taille du navire déduit de son nombre de salles."""
        return len(self.salles)

    @property
    def elements(self):
        """Retourne un tuple des éléments."""
        elts = []
        for salle in self.salles.values():
            elts.extend(salle.elements)

        return tuple(elts)

    @property
    def voiles(self):
        """Retourne les éléments voiles du navire."""
        elts = self.elements
        return tuple(e for e in elts if e.nom_type == "voile")

    @property
    def passerelle(self):
        """Retourne True si la passerelle du navire est dépliée."""
        elts = [e for e in self.elements if e.nom_type == "passerelle"]
        if not elts:
            return False

        e = elts[0]
        return e.baissee

    @property
    def gouvernail(self):
        """Retourne le gouvernail si le navire en contient un."""
        for salle in self.salles.values():
            gouvernail = salle.gouvernail
            if gouvernail:
                return gouvernail

        return None

    @property
    def amarre(self):
        """Retourne l'amarre si le navire en contient."""
        for salle in self.salles.values():
            element = salle.get_element("amarre")
            if element:
                return element

        return None

    @property
    def ancre(self):
        """Retourne la première ancre si le navire en contient."""
        for salle in self.salles.values():
            element = salle.get_element("ancre")
            if element:
                return element

        return None

    @property
    def elt_passerelle(self):
        """Retourne la passerelle si le navire en contient."""
        for salle in self.salles.values():
            element = salle.get_element("passerelle")
            if element:
                return element

        return None

    @property
    def rames(self):
        """Retourne les paires de rames contenues dans le navire."""
        rames = []
        for salle in self.salles.values():
            t_rames = salle.rames
            if t_rames:
                rames.append(t_rames)

        return rames

    @property
    def vent(self):
        """Retourne le vecteur du vent le plus proche.

        Il s'agit en fait d'un condensé des vents allentours.

        """
        vec_nul = Vector(0, 0, 0)

        if self.etendue is None:
            return vec_nul

        # On récupère le vent le plus proche
        vents = importeur.navigation.vents_par_etendue.get(
                self.etendue.cle, [])

        if not vents:
            return vec_nul

        # On calcul un vecteur des vents restants
        vecteur_vent = Vector(0, 0, 0)
        for vent in vents:
            v_x, v_y = vent.position.x, vent.position.y
            x, y = self.position.x, self.position.y
            distance = mag(v_x, v_y, 0, x, y, 0)
            if distance < vent.longueur:
                facteur = 1
            elif distance < vent.longueur ** 2:
                facteur = 0.6
            else:
                facteur = 0.3

            vitesse = Vector(vent.vitesse.x, vent.vitesse.y, vent.vitesse.z)
            vecteur_vent = vecteur_vent + vitesse * facteur

        return vecteur_vent

    @property
    def nom_allure(self):
        """Retourne le nom de l'allure."""
        vent = self.vent
        allure = (self.direction.direction - get_direction(vent)) % 360
        if ALL_DEBOUT < allure < (360 - ALL_DEBOUT):
            return "vent debout"
        elif ALL_PRES < allure < (360 - ALL_PRES):
            return "au près"
        elif ALL_BON_PLEIN < allure < (360 - ALL_BON_PLEIN):
            return "bon plein"
        elif ALL_LARGUE < allure < (360 - ALL_LARGUE):
            return "largue"
        elif ALL_GRAND_LARGUE < allure < (360 - ALL_GRAND_LARGUE):
            return "grand largue"
        else:
            return "vent arrière"

    @property
    def vitesse_noeuds(self):
        """Retourne la vitesse en noeuds."""
        vit_ecoulement = importeur.temps.cfg.vitesse_ecoulement
        vit_ecoulement = eval(vit_ecoulement)
        distance = self.vitesse.norme
        distance = distance * CB_BRASSES / 1000
        distance = distance / (TPS_VIRT / DIST_AVA)
        distance *= vit_ecoulement
        return distance * 3600

    @property
    def nom(self):
        return self.modele.nom

    @property
    def desc_survol(self):
        """Retourne le nom du modèle et le nom personnalisé."""
        nom = self.nom
        if self.nom_personnalise:
            nom += " nommé"
            if not self.modele.masculin:
                nom += "e"

            nom += " " + self.nom_personnalise

        return nom

    @property
    def poids_max(self):
        return self.modele.poids_max

    @property
    def poids(self):
        poids = 0
        for salle in self.salles.values():
            poids += salle.poids_eau

        return poids

    @property
    def graph(self):
        """Retourne le graph défini par le modèle."""
        return self.modele.graph

    @property
    def opt_position(self):
        """Retourne la position optimisée (Vector)."""
        coords = (self.position.x, self.position.y, self.position.z)
        return Vector(*coords)

    @property
    def opt_vitesse(self):
        """Retourne la vitesse optimisée (Vector)."""
        coords = (self.vitesse.x, self.vitesse.y, self.vitesse.z)
        return Vector(*coords)

    @property
    def opt_direction(self):
        """Retourne la direction optimisée (Vector)."""
        coords = (self.direction.x, self.direction.y, self.direction.z)
        return Vector(*coords)

    @property
    def accoste(self):
        """Retourne si le navire accoste quelque part.

        Un navire accoste si:
            Il a des amarres rattachées au quai ou
            Il a une ancre jetée et une passerelle dépliée.

        """
        amarre = self.amarre
        ancre = self.ancre
        passerelle = self.elt_passerelle
        if amarre and amarre.attachee:
            return True
        if ancre and ancre.jetee and passerelle and passerelle.baissee:
            return True

        return False

    def get_max_distance_au_centre(self):
        """Retourne la distance maximum par rapport au centre du navire."""
        distances = []
        for x, y, z in self.salles.keys():
            distances.append(sqrt(x ** 2 + y ** 2 + z ** 2))

        return max(distances)

    def construire_depuis_modele(self):
        """Construit le navire depuis le modèle."""
        modele = self.modele
        # On recopie les salles
        for r_coords, salle in modele.salles.items():
            n_salle = self.salles.get(r_coords)
            if n_salle is None:
                n_salle = SalleNavire(self.cle, salle.mnemonic,
                        salle.r_x, salle.r_y, salle.r_z, modele, self)
            n_salle.titre = salle.titre
            n_salle.titre_court = salle.titre_court
            n_salle.description = salle.description
            n_salle.details = salle.details
            n_salle.noyable = salle.noyable

            # On recopie les éléments
            for t_elt in salle.mod_elements:
                t_elts = [e for e in n_salle.elements if e.prototype is t_elt]
                if not t_elts:
                    elt = Element(t_elt, n_salle)
                    n_salle.elements.append(elt)

            if not r_coords in self.salles:
                self.salles[r_coords] = n_salle
            if n_salle not in importeur.salle.salles.values():
                importeur.salle.ajouter_salle(n_salle)

        # On recopie les sorties
        for salle in modele.salles.values():
            n_salle = self.salles[salle.r_coords]
            for dir, sortie in salle.sorties._sorties.items():
                if sortie and sortie.salle_dest:
                    c_salle = self.salles[sortie.salle_dest.r_coords]
                    n_salle.sorties.ajouter_sortie(dir, sortie.nom,
                            sortie.article, c_salle,
                            sortie.correspondante)

    def faire_ramer(self):
        """Cette méthode fait ramer les personnages du navire.

        Elle consomme l'endurance qu'ils doivent dépenser en fonction de
        la vitesse des rames manipulées.

        """
        for rames in self.rames:
            if rames.tenu:
                personnage = rames.tenu
                vitesse = rames.vitesse
                end = END_VIT_RAMES[vitesse]
                if end > 0:
                    try:
                        personnage.stats.endurance -= end
                    except DepassementStat:
                        personnage << "Vous lâchez les rames d'épuisement."
                        personnage.salle.envoyer("{} lâche les rames " \
                                "d'épuisement.", personnage)
                        rames.centrer()
                        rames.vitesse = "immobile"
                        rames.tenu = None
                        personnage.cle_etat = ""

    def valider_coordonnees(self):
        """Pour chaque salle, valide ses coordonnées."""
        for salle in self.salles.values():
            if not salle.coords.valide:
                salle.coords.valide = True

    def vent_debout(self):
        """Retourne le facteur de vitesse par l'allure vent debout."""
        return -0.3

    def pres(self):
        """Retourne le facteur de vitesse par l'allure de près."""
        return 0.5

    def bon_plein(self):
        """Retourne le facteur de vitesse par l'allure de bon plein."""
        return 0.8

    def largue(self):
        """Retourne le facteur de vitesse par l'allure de largue."""
        return 1.2

    def grand_largue(self):
        """Retourne le facteur de vitesse par l'allure de grand largue."""
        return 0.9

    def vent_arriere(self):
        """Retourne le facteur de vitesse par l'allure par vent arrière."""
        return 0.7

    def maj_salles(self):
        d = self.direction.direction + 90
        i = self.direction.inclinaison
        operation = lambda v: self.position + v.tourner_autour_z(d).incliner(i)
        for vec, salle in self.salles.items():
            vec = Vecteur(*vec)
            vec = operation(vec)
            salle.coords.x = vec.x
            salle.coords.y = vec.y
            salle.coords.z = vec.z

    def avancer(self, temps_virtuel):
        """Fait avancer le navire si il n'est pas immobilisé."""
        vit_or = vit_fin = self.vitesse_noeuds
        origine = self.opt_position
        vitesse = self.opt_vitesse
        if not self.immobilise:
            # On contrôle les collisions
            # On cherche toutes les positions successives du navire
            vecteurs = []
            angle_radians = radians((self.direction.direction + 90) % 360)
            for coords, salle in self.salles.items():
                t_vecteur = Vector(*coords)
                t_vecteur.around_z(angle_radians)
                vecteurs.append((origine + t_vecteur, salle))

            # On récupère les points proches du navire
            etendue = self.etendue
            centre = self.get_max_distance_au_centre()
            points = tuple(etendue.get_points_proches(origine.x, origine.y,
                    vitesse.mag * temps_virtuel + centre).items())
            points += importeur.navigation.points_navires(self)
            # Si l'étendue a un point sur le segment
            # (position -> position + vitesse) alors collision
            for vecteur, t_salle in vecteurs:
                projetee = vecteur + vitesse * temps_virtuel
                b_arg = [vecteur.x, vecteur.y, vecteur.z, projetee.x, \
                        projetee.y, projetee.z]
                for coords, point in points:
                    v_point = Vector(*coords)
                    arg = b_arg + list(coords) + [etendue.altitude, 0.5]
                    if in_rectangle(*arg) and vecteur.distance(
                            projetee, v_point) < 0.5:
                        self.collision(t_salle, point)
                        self.vitesse.x = 0
                        self.vitesse.y = 0
                        self.vitesse.z = 0
                        self.acceleration.x = 0
                        self.acceleration.y = 0
                        self.acceleration.z = 0
                        return

            Vehicule.avancer(self, temps_virtuel)
            vit_fin = self.vitesse_noeuds
            n_position = self.opt_position

            # Si le navire a croisé un lien, change d'étendue
            for coords, autre in etendue.liens.items():
                x, y = coords
                if autre is etendue or (round(x) == self.dl_x and \
                        round(y) == self.dl_y):
                    continue

                v_point = Vector(*coords)
                if in_rectangle(origine.x, origine.y, origine.z,
                        n_position.x, n_position.y, n_position.z,
                        x, y, etendue.altitude, 0.5) and origine.distance(
                        n_position, v_point) <= 0.5:
                    # C'est un lien, on change d'étendue
                    # Les autres liens ne sont pas pris en compte
                    self.etendue = autre
                    self.position.z = autre.altitude
                    print("On change d'étendue pour", self, self.etendue.cle)
                    self.dl_x = round(x)
                    self.dl_y = round(y)
                    break

        if round(self.position.x) != self.dl_x or round(self.position.y) \
                != self.dl_y:
            self.dl_x, self.dl_y = 0, 0

        if vit_or <= 0.01 and vit_fin >= 0.05:
            if vit_fin < 0.2:
                self.envoyer("Vous sentez le navire accélérer en douceur.")
            elif vit_fin >= 0.2:
                self.envoyer("Vous sentez le navire prendre rapidement " \
                        "de la vitesse.")

        self.en_collision = False

    def collision(self, salle, contre=None):
        """Méthode appelée lors d'une collision avec un point."""
        Vehicule.collision(self, salle)
        vitesse = self.vitesse_noeuds
        if vitesse < 0.1:
            pass
        elif vitesse < 0.4:
            self.envoyer("Un léger choc ébranle le navire.")
        elif vitesse < 1.5:
            self.envoyer("Un choc violent ébranle l'ensemble du navire !")
        else:
            self.envoyer("Le craquement du bois se brisant vous emplit " \
                    "les oreilles.")
            salle.noyer(vitesse * 20)

    def virer(self, n=1):
        """Vire vers tribord ou bâbord de n degrés.

        Si n est inférieure à 0, vire vers bâbord.
        Sinon, vire vers tribord.

        """
        self.direction.tourner_autour_z(n)
        self.maj_salles()

    def envoyer(self, message):
        """Envoie le message à tous les personnages présents dans le navire."""
        for salle in self.salles.values():
            salle.envoyer(message)

    def synchroniser_modele(self):
        """Cette méthode force la synchronisation d'informations sur le modèle.

        On parcourt toutes les salles du modèle et recrée certaines
        informations commes les détails si nécessaire.

        """
        for m_coords, m_salle in self.modele.salles.items():
            salle = self.salles[m_coords]
            salle.titre = m_salle.titre
            for det_nom, m_detail in m_salle.details._details.items():
                details = salle.details._details
                if det_nom not in details:
                    detail = salle.details.ajouter_detail(det_nom,
                            modele=m_detail)
                else:
                    detail = details[det_nom]

                detail.synonymes = list(m_detail.synonymes)
                detail.titre = m_detail.titre
                detail.positions = dict(m_detail.positions)
                detail.est_visible = m_detail.est_visible
                detail.script = m_detail.script
                detail.peut_asseoir = m_detail.peut_asseoir
                detail.peut_allonger = m_detail.peut_allonger
                detail.facteur_asseoir = m_detail.facteur_asseoir
                detail.facteur_allonger = m_detail.facteur_allonger
                detail.connecteur = m_detail.connecteur
                detail.nb_places_assises = m_detail.nb_places_assises
                detail.nb_places_allongees = m_detail.nb_places_allongees

    def arreter(self):
        """Arrête le navire.

        Si le navire possède une ancre et passerelle, on la jète et la déplie.
        Sinon on essaye de l'amarrer.
        Cette méthode peut échouer sans erreur.

        """
        if self.ancre:
            self.ancre.jetee = True
            self.immobilise = True

        if self.elt_passerelle:
            passerelle = self.elt_passerelle
            passerelle.deplier()

        if self.amarre:
            amarre = self.amarre
            salle = amarre.parent
            navire = salle.navire
            etendue = navire.etendue
            distance = 2
            d_salle = None
            x, y, z = salle.coords.tuple()
            for coords, t_salle in etendue.cotes.items():
                if t_salle.nom_terrain not in TERRAINS_QUAI:
                    continue

                t_x, t_y, t_z = t_salle.coords.tuple()
                t_distance = mag(x, y, z, t_x, t_y, t_z)
                if t_distance < distance:
                    d_salle = t_salle
                    distance = t_distance

            if d_salle:
                amarre.attachee = d_salle
                navire.immobilise = True

    def sombrer(self):
        """Fait sombrer le navire."""
        self.envoyer("Un grincement déchirant et le navire s'enfonce sous " \
                "l'eau !")
        importeur.navigation.ecrire_suivi("{} sombre.".format(self.cle))

        # Replie la passerelle si il y a une passerelle
        elt_passerelle = self.elt_passerelle
        if elt_passerelle:
            elt_passerelle.replier()

        # Cherche la salle la plus proche du nauffrage
        x, y, z = self.position.tuple
        salles = [s for s in importeur.salle._coords.values() if \
                hasattr(s, "coords") and s.coords.z == z and s.nom_terrain in \
                TERRAINS_ACCOSTABLES]
        salle_choisie = min(salles, key=lambda s: mag(x, y, z, s.coords.x,
                s.coords.y, s.coords.z))
        for salle in self.salles.values():
            for personnage in salle.personnages:
                personnage.salle = salle_choisie
                try:
                    personnage.stats.vitalite = 0
                except DepassementStat:
                    personnage.mourir()

        importeur.navigation.supprimer_navire(self.cle)

    def detruire(self):
        """Destruction du self."""
        for salle in list(self.salles.values()):
            importeur.salle.supprimer_salle(salle.ident)

        self.modele.vehicules.remove(self)
        Vehicule.detruire(self)


class Propulsion(Force):

    """Force de propulsion d'un navire.

    Elle doit être fonction du vent, du nombre de voile et de leur
    orientation. Elle est également fonction des rames et rameurs.

    """

    def __init__(self, subissant):
        """Constructeur de la force."""
        Force.__init__(self, subissant)

    def __getnewargs__(self):
        return (None, )

    def calcul(self):
        """Retourne le vecteur de la force."""
        vec_nul = Vector(0, 0, 0)
        navire = self.subissant
        vent = navire.vent
        direction = navire.opt_direction
        voiles = navire.voiles
        voiles = [v for v in voiles if v.hissee]
        for rames in navire.rames:
            if rames.tenu and not rames.tenu.est_connecte():
                rames.tenu.cle_etat = ""
                rames.tenu = None

        navire.faire_ramer()
        rames = [r for r in navire.rames if r.tenu is not None]
        vecteur = vec_nul
        if voiles:
            fact_voile = sum(v.facteur_orientation(navire, vent) \
                    for v in voiles) / len(voiles) * 0.7
            allure = (get_direction(direction) - get_direction(vent)) % 360
            if ALL_DEBOUT < allure < (360 - ALL_DEBOUT):
                facteur = navire.vent_debout()
            elif ALL_PRES < allure < (360 - ALL_PRES):
                facteur = navire.pres()
            elif ALL_BON_PLEIN < allure < (360 - ALL_BON_PLEIN):
                facteur = navire.bon_plein()
            elif ALL_LARGUE < allure < (360 - ALL_LARGUE):
                facteur = navire.largue()
            elif ALL_GRAND_LARGUE < allure < (360 - ALL_GRAND_LARGUE):
                facteur = navire.grand_largue()
            else:
                facteur = navire.vent_arriere()

            vecteur = direction * facteur * fact_voile * vent.mag

        # Calcul des rames
        if rames:
            facts = [VIT_RAMES[rame.vitesse] for rame in rames]
            fact = 0.8
            for f in facts:
                fact *= f

            vecteur = vecteur + direction * fact

        return Vecteur(vecteur.x, vecteur.y, vecteur.z)
