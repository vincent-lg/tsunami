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
from random import random
from vector import *

from abstraits.obase import BaseObj
from primaires.perso.exceptions.stat import DepassementStat
from primaires.vehicule.force import Force
from primaires.vehicule.vecteur import *
from primaires.vehicule.vehicule import Vehicule
from secondaires.navigation.equipage import Equipage
from .cale import Cale
from .constantes import *
from .element import Element
from .salle import SalleNavire
from .vent import INFLUENCE_MAX
from .visible import Visible
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
    obs_recif = ()
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
        self.cale = Cale(self)
        self.canots = []
        self.compteur = 0
        self.pavillon = None
        self.donnees = {}

        if modele:
            modele.vehicules.append(self)
            self.cle = importeur.navigation.dernier_ID(modele.cle)
            self.construire_depuis_modele()

        self._construire()

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
    def centre(self):
        """Retourne la salle au centre du navire."""
        return self.salles.get((0, 0, 0))

    @property
    def vent(self):
        """Retourne le vecteur du vent le plus proche.

        Il s'agit en fait d'un condensé des vents allentours.

        """
        vec_nul = Vector(0, 0, 0)

        if self.etendue is None:
            return vec_nul

        # On récupère les vents le plus proche
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
        return get_vitesse_noeuds(self.vitesse.norme)

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

    @property
    def point_accostage(self):
        """Retourne le point d'accostage.

        Si le navire a une passerelle dépliée, retourne la salle.
        Si le navire a des amarres, retourne la salle à laquelle
        il est amarré.

        """
        if not self.accoste:
            return None

        amarre = self.amarre
        passerelle = self.elt_passerelle
        if amarre and amarre.attachee:
            return amarre.attachee
        if passerelle and passerelle.baissee:
            return passerelle.baissee_vers

        return None

    @property
    def salles_endommagees(self):
        """Retourne la liste des salles endommagées.

        Une salle est endommagée si elle a une voie d'eau ou
        un certain poids d'eau.

        """
        return [s for s in self.salles.values() if \
                s.voie_eau == COQUE_OUVERTE or s.poids_eau > 0]

    @property
    def personnages(self):
        """Retourne TOUS les personnages présents sur le navire."""
        personnages = []
        for salle in self.salles.values():
            personnages.extend(salle.personnages)

        return personnages

    @property
    def orientation(self):
        """Retourne l'orientation du navire.

        L'orientation est un nombre entier : si il est positif, il
        indique que le navire tourne vers tribord. Si il est négatif,
        il indique que le navire tourne vers bâbord. Si il est nul,
        le navire ne tourne pas. Cette orientation est directement
        calculée depuis le gouvernail et les rames.

        """
        gouvernail = self.gouvernail
        orientation = 0
        if gouvernail:
            orientation = gouvernail.orientation

        # Intégration des rames
        for rame in self.rames:
            if rame.tenu is not None and rame.orientation != 0:
                orientation += rame.orientation * 5 / self.taille

        return int(orientation)

    @property
    def aff_nom(self):
        return self.nom_personnalise or "aucun"

    @property
    def nom_etendue(self):
        return self.etendue and self.etendue.cle or "aucune"

    @property
    def nom_proprietaire(self):
        return self.proprietaire and self.proprietaire.nom or "aucun"

    @property
    def nb_voies_eau(self):
        """Retourne le nombre de voies d'eau du navire."""
        nb = 0
        for salle in self.salles.values():
            if salle.noyable:
                if salle.voie_eau == COQUE_OUVERTE:
                    nb += 1

        return nb

    def a_le_droit(self, personnage, poste="capitaine", si_present=False):
        """Retourne True si le personnage a le droit, False sinon.

        Le droit est calculé selon plsuieurs critères :
            Si le personnage est immortel, retourne True
            Si le personnage est le propriétaire, retourne True

        """
        if personnage.est_immortel():
            return True

        if personnage is self.proprietaire or \
                        (si_present and getattr(self.proprietaire.salle,
                        "navire", None) is self):
            return True

        return self.equipage.est_au_poste(personnage, poste)

    def get_vitesse_rames(self, vitesses):
        """Retourne la vitesse en distance (norme) de vecteur.

        Une liste de vitesses doit être précisée en paramètre,
        représentant une liste de chaînes dont chaque chaîne est un
        nom de vitesse (par exemple, "lente"). Pour chaque vitesse,
        on récupère son facteur tel qe défini dans les constantes
        et le facteur multiplicateur défini dans le modèle.

        """
        rames = self.rames
        facteur = 0
        facteur_rames = self.modele.facteur_rames
        for vitesse in vitesses:
            facteur_vitesse = VIT_RAMES[vitesse]
            facteur += (facteur_rames * facteur_vitesse) / len(rames)

        return facteur

    def get_vitesse_voiles(self, voiles, vent):
        """Retourne la vitesse imprimée par les voiles spécifiées.

        Normalement, on ne tient compte que des voiles hissées qui
        doivent être précisées dans une lsite. Mais cette liste peut
        contenir des objets None. Dans ce cas, on se rapporte à la
        taille de la liste et la question posée à cette méthode est
        simplement "calcul la distance parcourue si le navire avait
        tant de voiles hissées".

        """
        direction = self.opt_direction
        if not any(voiles):
            fact_voile = len(voiles)
        else:
            fact_voile = sum(v.facteur_orientation(self, vent) \
                    for v in voiles)

        fact_voile = fact_voile / len(self.voiles) * 0.7

        allure = (get_direction(direction) - get_direction(vent)) % 360
        if ALL_DEBOUT < allure < (360 - ALL_DEBOUT):
            facteur = self.vent_debout()
        elif ALL_PRES < allure < (360 - ALL_PRES):
            facteur = self.pres()
        elif ALL_BON_PLEIN < allure < (360 - ALL_BON_PLEIN):
            facteur = self.bon_plein()
        elif ALL_LARGUE < allure < (360 - ALL_LARGUE):
            facteur = self.largue()
        elif ALL_GRAND_LARGUE < allure < (360 - ALL_GRAND_LARGUE):
            facteur = self.grand_largue()
        else:
            facteur = self.vent_arriere()

        return facteur * fact_voile * vent.mag

    def get_max_distance_au_centre(self):
        """Retourne la distance maximum par rapport au centre du navire."""
        distances = []
        for x, y, z in self.salles.keys():
            distances.append(sqrt(x ** 2 + y ** 2 + z ** 2))

        return max(distances)

    def get_nom_pour(self, personnage):
        return self.desc_survol

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
            n_salle.interieur = salle.interieur
            n_salle.poste = salle.poste
            n_salle.noyable = salle.noyable
            n_salle.sabord_min = salle.sabord_min
            n_salle.sabord_max = salle.sabord_max
            n_salle.cales = salle.cales

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
                    t_sortie = n_salle.sorties.ajouter_sortie(dir,
                            sortie.nom, sortie.article, c_salle,
                            sortie.correspondante)
                    if sortie.porte:
                        t_sortie.ajouter_porte()

    def reparer(self):
        """Répare intégralement le navire."""
        for salle in self.salles.values():
            if salle.noyable:
                if salle.voie_eau != COQUE_INTACTE:
                    salle.voie_eau = COQUE_INTACTE
                if salle.poids_eau != 0:
                    salle.poids_eau = 0

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
                        rames.relacher()
                        rames.tenu = None
                        personnage.etats.retirer("tenir_rames")
            else:
                if rames.vitesse != "immobile":
                    rames.vitesse = "immobile"
                if rames.orientation != 0:
                    rames.orientation = 0

    def valider_coordonnees(self):
        """Pour chaque salle, valide ses coordonnées."""
        for salle in self.salles.values():
            if not salle.coords.valide:
                salle.coords.valide = True

    def vent_debout(self):
        """Retourne le facteur de vitesse par l'allure vent debout."""
        return self.modele.facteurs_orientations["vent debout"]

    def pres(self):
        """Retourne le facteur de vitesse par l'allure de près."""
        return self.modele.facteurs_orientations["au près"]

    def bon_plein(self):
        """Retourne le facteur de vitesse par l'allure de bon plein."""
        return self.modele.facteurs_orientations["bon plein"]

    def largue(self):
        """Retourne le facteur de vitesse par l'allure de largue."""
        return self.modele.facteurs_orientations["largue"]

    def grand_largue(self):
        """Retourne le facteur de vitesse par l'allure de grand largue."""
        return self.modele.facteurs_orientations["grand largue"]

    def vent_arriere(self):
        """Retourne le facteur de vitesse par l'allure par vent arrière."""
        return self.modele.facteurs_orientations["vent arrière"]

    def maj_salles(self):
        d = self.direction.direction + 90
        for vec, salle in self.salles.items():
            vec = Vecteur(*vec)
            vec = self.position + vec.tourner_autour_z(d)
            salle.coords.x = vec.x
            salle.coords.y = vec.y
            salle.coords.z = vec.z

    def avancer(self, temps_virtuel):
        """Fait avancer le navire si il n'est pas immobilisé."""
        x = self.position.x
        y = self.position.y
        z = self.position.z
        etendue = self.etendue
        vit_or = vit_fin = self.vitesse_noeuds
        origine = self.opt_position
        vitesse = self.opt_vitesse
        
        # Si le navire est à fond plat
        if self.modele.fond_plat and not etendue.eau_douce and \
                etendue.profondeur > 4 and random() < 0.07:
            print(self, "chavire")
            self.envoyer("|err|Une vague plus haute que les autres " \
                    "fait chavirer l'embarcation !|ff|")
            self.sombrer()
            return
        
        if not self.immobilise:
            # On contrôle les collisions
            # On cherche toutes les positions successives du navire
            if self.controller_collision(vitesse * temps_virtuel):
                return

            Vehicule.avancer(self, temps_virtuel)
            if self.controller_collision():
                # On annule le déplacement
                self.position.x = x
                self.position.y = y
                self.position.z = z
                self.maj_salles()
                return

            vit_fin = self.vitesse_noeuds
            n_position = self.opt_position

            # Si le navire a croisé un lien, change d'étendue
            autre = etendue.croise_lien((origine.x, origine.y),
                    (n_position.x, n_position.y))
            if autre:
                print(self, "change d'étendue:", autre)
                if autre.profondeur < self.modele.tirant_eau:
                    self.envoyer("Un grincement sonore, la quille " \
                            "touche le fond.")
                    # On annule le déplacement
                    self.position.x = x
                    self.position.y = y
                    self.position.z = z
                    self.maj_salles()
                    return
                
                self.etendue = autre
                self.position.z = autre.altitude
                autre.script["entre"].executer(centre=self.centre,
                        cle=self.cle, origine=etendue.cle)

            # Enregistre la distance parcourue au compteur
            distance = (n_position - origine).mag
            self.compteur += distance * CB_BRASSES

        if vit_or <= 0.01 and vit_fin >= 0.05:
            if vit_fin < 0.2:
                self.envoyer("Vous sentez le navire accélérer en douceur.")
            elif vit_fin >= 0.2:
                self.envoyer("Vous sentez le navire prendre rapidement " \
                        "de la vitesse.")

        self.en_collision = False

    def controller_collision(self, destination=None, direction=None,
            collision=True, marge=0.5, debug=False):
        """Contrôle les collisions entre la position actuel et la destination.

        Si la direction est précisée, le navire vire (la direction
        est à préciser en degré).

        """
        if destination and direction:
            raise ValueError("La destination et direction sont précisés.")

        origine = self.opt_position
        destination = destination or Vector(0, 0, 0)
        direction_absolue = self.direction.direction + 90
        if direction:
            direction_absolue += direction

        vecteurs = []
        for salle in self.salles.values():
            t_vecteur = Vector(*salle.coords.tuple())
            vecteurs.append((t_vecteur, salle))

        # On récupère les points proches du navire
        etendue = self.etendue
        centre = self.get_max_distance_au_centre()
        diametre = destination.mag + centre + 1
        points = tuple(etendue.get_points_proches(origine.x, origine.y,
                diametre).items())
        points += importeur.navigation.points_navires(self)
        if debug:
            print("Etendue={}, centre={}, diamètre={}, nb_points={}".format(
                    etendue.cle, centre, diametre, len(points)))

        # Si l'étendue a un point sur le segment
        # (position -> position + vitesse) alors collision
        for vecteur, t_salle in vecteurs:
            if direction:
                projetee = Vector(t_salle.r_x, t_salle.r_y, t_salle.r_z)
                projetee.around_z(radians(direction_absolue))
                projetee = origine + projetee
            else:
                projetee = vecteur + destination

            b_arg = [vecteur.x, vecteur.y, vecteur.z, projetee.x,
                    projetee.y, projetee.z]
            for coords, point in points:
                if debug:
                    print("De x={} y={} vers x={} y={} comparé à " \
                            "x={} y={}".format(round(vecteur.x, 2),
                            round(vecteur.y, 2), round(projetee.x, 2),
                            round(projetee.y, 2), round(coords[0], 2),
                            round(coords[1], 2)))
                v_point = Vector(coords[0], coords[1], etendue.altitude)
                arg = b_arg + list(coords) + [etendue.altitude, marge]
                rectangle = in_rectangle(*arg)
                d_marge = vecteur.distance(projetee, v_point)
                if debug:
                    print("in_rectangle={}, distance={}".format(
                            rectangle, d_marge))
                if rectangle and d_marge < marge:
                    if collision:
                        importeur.navigation.nav_logger.warning(
                                "Collision entre {} et {}".format(
                                t_salle, point))
                        self.collision(t_salle, point)
                    return True

        return False

    def collision(self, salle, contre=None):
        """Méthode appelée lors d'une collision avec un point."""
        Vehicule.collision(self, salle)
        vitesse = self.vitesse_noeuds
        print("Collision", contre)
        if contre in type(self).obs_recif:
            if vitesse < 0.05:
                pass
            else:
                self.envoyer("Le craquement du bois se brisant vous emplit " \
                        "les oreilles.")
                salle.noyer(vitesse * 20)
        elif vitesse < 0.1:
            pass
        elif vitesse < 0.4:
            self.envoyer("Un léger choc ébranle le navire.")
        elif vitesse < 1.5:
            self.envoyer("Un choc violent ébranle l'ensemble du navire !")
        else:
            self.envoyer("Le craquement du bois se brisant vous emplit " \
                    "les oreilles.")
            salle.noyer(vitesse * 20)
        self.vitesse.x = 0
        self.vitesse.y = 0
        self.vitesse.z = 0
        self.acceleration.x = 0
        self.acceleration.y = 0
        self.acceleration.z = 0

        # On prévient l'équipage
        if self.equipage:
            self.equipage.reagir_collision(salle, contre)

    def virer(self, n=1):
        """Vire vers tribord ou bâbord de n degrés.

        Si n est inférieure à 0, vire vers bâbord.
        Sinon, vire vers tribord.

        """
        if self.controller_collision(direction=n):
            self.envoyer("Un léger choc se répercute sous vos pieds.")
            return

        x, y, z = self.direction.tuple
        self.direction.tourner_autour_z(n)
        self.maj_salles()
        if self.controller_collision():
            # On annule la translation
            self.envoyer("Un léger choc se répercute sous vos pieds.")
            self.direction.x = x
            self.direction.y = y
            self.direction.z = z
            self.maj_salles()

    def envoyer(self, message):
        """Envoie le message à tous les personnages présents dans le navire."""
        for salle in self.salles.values():
            salle.envoyer(message)

    def envoyer_autour(self, messages, rayon, exclure_navire=True):
        """Envoie le message dans les salles autour du navire.

        Par défaut, cette méthode envoie le message aux salles
        autour du navire sans comprendre le navire-même.

        Paramètres à préciser :

            messages -- le ou les messages à envoyer
            rayon -- le rayon maximum (en salles)
            exclure_navire -- exclut ou non le navire-même

        Le premier paramètre peut être soit une chaîne qui sera envoyée
        à chaque salle autour du navire, peu importe sa distance, ou
        bien un dictionnaire sous la forme :

            {
                distance1: "message",
                distance2: "message2",
                ...
            }

        Par exemple :

            messages = {
                5: "C'est tout près",
                10: "C'est un peu plus loin",
                15, "C'est très loin",
            }
            navire.envoyer_autour(messages, 20)
            # Si la salle est à moins de 5 salles du navire, envoie le
            # premier message, ainsi de suite pour les autres.

        Enfin, les messages peuvent contenir des chaînes de remplacement :

          * distance : une estimation de la distance en brasses
          * sortie : le nom de la sortie séparant la salle du navire
          * sortie_complete : le nom complet de la sortie

        Exemple :

          navire.envoyer("Vous entendez un PLOUF vers {sortie_complete} " \
                "à {distance}."

        """
        # On regroupe les messages
        if isinstance(messages, str):
            messages = {rayon: messages}

        # On réunit les salles concernées
        exclues = list(self.salles.values()) if exclure_navire else []
        centre = self.position
        c_x, c_y, c_z = centre.x, centre.y, centre.z
        salles = []

        for salle in importeur.salle._coords.values():
            if salle in exclues:
                continue

            x, y, z = salle.coords.x, salle.coords.y, salle.coords.z
            vecteur = Vecteur(c_x - x, c_y - y, c_z - z)
            if vecteur.norme <= rayon:
                salles.append((vecteur, salle))

        # Trie en fonction de la distance
        salles = sorted(salles, key=lambda couple: couple[0].norme)

        # Envoie le message
        for vecteur, salle in salles:
            sortie = salle.get_sortie(vecteur, None)
            nom_distance = get_nom_distance(vecteur)
            norme = vecteur.norme

            # Cherche le bon message
            for distance, message in sorted(tuple(messages.items())):
                if norme <= distance:
                    salle.envoyer(message.format(distance=nom_distance,
                            sortie=sortie.nom,
                            sortie_complete=sortie.nom_complet))
                    break

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

    def mettre_en_cale_seche(self):
        """Essaye de mettre le navire en cale sèche."""
        # Cherche le chantier navale
        etendue = self.etendue
        chantier = None
        for t_chantier in importeur.navigation.chantiers.values():
            if t_chantier.etendue is etendue:
                chantier = t_chantier
                break

        if chantier is None:
            raise ValueError("Impossible de trouver le chantier " \
                    "navale correspondant à l'étendue d'eau.")

        # Replie la passerelle si il y a une passerelle
        elt_passerelle = self.elt_passerelle
        if elt_passerelle:
            elt_passerelle.replier()

        self.etendue = None
        chantier.cales_seches.append(self)

        for salle in self.salles.values():
            salle.coords.valide = False

    @staticmethod
    def peut_boire(personnage, objet=None):
        """Retourne une valeur si le personnage peut boire ici."""
        salle = personnage.salle
        navire = getattr(salle, "navire", None)
        if objet is None:
            if navire and navire.etendue and navire.etendue.eau_douce:
                return True
            elif navire and navire.cale.eau_douce > 0 and navire.a_le_droit(
                    personnage, si_present=True):
                navire.cale.boire()
                return True
            return False
        else:
            if objet.est_de_type("tonneau d'eau"):
                return Navire.boire
            return False

    @staticmethod
    def boire(personnage, objet):
        """Fait boire le personnage.

        Ou essayer.

        """
        if objet.est_de_type("tonneau d'eau"):
            if objet.gorgees_contenu > 0:
                if personnage.estomac <= 2.9:
                    if personnage.soif > 0:
                        personnage.soif -= 8
                    personnage.estomac += 0.25
                    objet.gorgees_contenu -= 1
                    personnage << "Vous buvez {}.".format(objet.get_nom())
                    personnage.salle.envoyer("{} boit " + objet.get_nom() + \
                            ".", personnage)
                else:
                    e = "e" if personnage.est_feminin() else ""
                    personnage << "Vous êtes plein{e} ; une gorgée de plus " \
                            "et vous éclaterez.".format(e=e)
            else:
                personnage << "|err|Ce tonneau d'eau est vide.|ff|"
    def regarder(self, personnage):
        """Le personnage regarde le navire."""
        salle = personnage.salle
        navire = salle.navire
        etendue = navire.etendue
        portee = get_portee(salle)
        visible = Visible.observer(personnage, portee, 5)
        navires = [couple[1][1] for couple in visible.points.items()]
        if self not in navires:
            personnage << "|err|Vous ne pouvez voir ce navire d'ici.|ff|"
            return

        salle.envoyer("{{}} regarde {}.".format(self.desc_survol.lower()),
                personnage)
        centre = self.salles[0, 0, 0]
        msg = "Vous regardez " + self.desc_survol + " :\n\n"
        msg += self.modele.description.regarder(personnage, centre)

        if navire:
            # On ajoute la direction du navire concurrent
            direction = navire.direction.direction
            direction = round((self.direction.direction - direction) / 5) * 5
            if direction <= -180 or direction >= 180:
                msg_dir = "sur 180°"
            elif direction < 0:
                msg_dir = "sur {}° bâbord".format(-direction)
            elif direction == 0:
                msg_dir = "sur 0°"
            else:
                msg_dir = "sur {}° tribord".format(direction)

            msg += "\nCe navire se dirige " + msg_dir + "."

        personnage << msg

    def sombrer(self):
        """Fait sombrer le navire."""
        importeur.hook["navire:sombre"].executer(navire=self)

        self.envoyer("Un grincement déchirant et le navire s'enfonce sous " \
                "l'eau !")
        importeur.navigation.ecrire_suivi("{} sombre.".format(self.cle))

        messages = {
                5: "Un grand fracas, un grincement final, un navire sombre " \
                   "vers {sortie_complete} à {distance}.",
                12: "Vous entendez un grand fracas vers {sortie_complete}, " \
                    "il semble qu'un navire sombre.",
                30: "Vous entendez un craquement vers {sortie_complete}, il " \
                    "semble qu'un navire sombre.",
        }

        self.envoyer_autour(messages, 30)

        # Donne une récompense aux ennemis
        if self.equipage:
            cles = [n.cle for n in self.equipage.ennemis]
            importeur.navigation.nav_logger.info("{} sombre " \
                    "(ennemis={})".format(self.cle, cles))
            self.equipage.recompenser_ennemis()
        else:
            importeur.navigation.nav_logger.info("{} sombre".format(self.cle))

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

    def enlever_canot(self, canot):
        """Cette méthode enlève le canot et le met à bord.

        Le canot est un autre navire (supposément un petit). Il
        est placé dans les canots du bord et pourra être descendu ailleurs.

        """
        if not canot.modele.canot:
            raise ValueError("{} n'est pas un canot".format(canot))

        for salle in canot.salles.values():
            if salle.personnages:
                raise ValueError("{} a des personnages".format(salle))

        canot.etendue = None
        for salle in canot.salles.values():
            salle.coords.valide = False

        self.canots.append(canot.cle)

    def detruire(self):
        """Destruction du self."""
        # Replie la passerelle si il y a une passerelle
        elt_passerelle = self.elt_passerelle
        if elt_passerelle:
            elt_passerelle.replier()

        for salle in list(self.salles.values()):
            importeur.salle.supprimer_salle(salle.ident)

        self.equipage.detruire()
        self.cale.detruire()
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
                rames.tenu.etats.retirer("tenir_rames")
                rames.tenu = None
                rames.vitesse = "immobile"
                rames.centrer()

        navire.faire_ramer()
        rames = [r for r in navire.rames if r.tenu is not None]
        vecteur = vec_nul
        if voiles:
            facteur = navire.get_vitesse_voiles(voiles, vent)
            vecteur = direction * facteur

        # Calcul des rames
        if rames:
            vitesses = [rame.vitesse for rame in rames]
            facteur = navire.get_vitesse_rames(vitesses)
            vecteur = vecteur + direction * facteur

        return Vecteur(vecteur.x, vecteur.y, vecteur.z)
