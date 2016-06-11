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


"""Fichier contenant la classe SalleNavire, détaillée plus bas."""

from collections import OrderedDict

from primaires.perso.exceptions.stat import DepassementStat
from primaires.salle.salle import Salle
from primaires.salle.sortie import Sortie
from secondaires.navigation.constantes import *
from secondaires.navigation.visible import Visible

# Constantes
NOMS_SORTIES = OrderedDict()
NOMS_SORTIES["sud"] = "arrière"
NOMS_SORTIES["ouest"] = "bâbord"
NOMS_SORTIES["nord"] = "avant"
NOMS_SORTIES["est"] = "tribord"
NOMS_SORTIES["bas"] = "bas"
NOMS_SORTIES["haut"] = "haut"

ARTICLES = {
    "bâbord": "",
    "tribord": "",
    "avant": "l'",
    "arrière": "l'",
    "bas": "le",
    "haut": "le",
}

NOMS_CONTRAIRES = {
    "nord": "sud",
    "ouest": "est",
    "est": "ouest",
    "sud": "nord",
    "haut": "bas",
    "bas": "haut",
}

class SalleNavire(Salle):

    """Classe représentant une salle de navire.

    Une salle de navire est une salle standard comportant quelques
    informations supplémentaires, comme les éléments dérfinis dans cette
    salle ou le navire qu'elles composent.

    """

    _nom = "salle_navire"
    _version = 1
    def __init__(self, zone, mnemonic, r_x=0, r_y=0, r_z=0, modele=None,
            navire=None):
        """Constructeur du navire."""
        Salle.__init__(self, zone, mnemonic, valide=False)
        self.navire = navire
        self.modele = modele
        self.titre_court = ""
        self.elements = []
        self.mod_elements = []
        self.r_x = r_x
        self.r_y = r_y
        self.r_z = r_z
        self.noyable = True
        self.voie_eau = COQUE_INTACTE
        self.poids_eau = 0
        self.sabord_min = 0
        self.sabord_max = 0
        self.cales = []
        self.poste = ""

    @property
    def r_coords(self):
        """Retourne les coordonnées relatives de la salle."""
        return (self.r_x, self.r_y, self.r_z)

    @property
    def passerelle(self):
        """Retourne la passerelle de la salle ou None."""
        elts = [e for e in self.elements if e.nom_type == "passerelle"]
        if elts:
            return elts[0]

        return None

    @property
    def ancre(self):
        """Retourne l'ancre de la salle ou None."""
        elts = [e for e in self.elements if e.nom_type == "ancre"]
        if elts:
            return elts[0]

        return None

    @property
    def amarre(self):
        """Retourne l'ancre de la salle ou None."""
        elts = [e for e in self.elements if e.nom_type == "amarre"]
        if elts:
            return elts[0]

        return None

    @property
    def voiles(self):
        """Retourne les voiles de la salle."""
        return [e for e in self.elements if e.nom_type == "voile"]

    @property
    def gouvernail(self):
        """Retourne le gouvernail de la salle ou None."""
        elts = [e for e in self.elements if e.nom_type == "gouvernail"]
        if elts:
            return elts[0]

        return None

    @property
    def loch(self):
        """Retourne le loch de la salle ou None."""
        elts = [e for e in self.elements if e.nom_type == "loch"]
        if elts:
            return elts[0]

        return None

    @property
    def rames(self):
        """Retourne les rames de la salle ou None."""
        elts = [e for e in self.elements if e.nom_type == "rames"]
        if elts:
            return elts[0]

        return None

    @property
    def str_cales(self):
        return ", ".join(sorted(self.cales))

    @property
    def proprietaires(self):
        """Retourne les propriétaires de la salle (cabine ?)."""
        if self.poste and self.navire and self.navire.equipage:
            proprietaires = self.navire.equipage.get_matelots_au_poste(
                    self.poste, joueurs=True)
            proprietaire = self.navire.proprietaire
            if proprietaire not in proprietaires:
                proprietaires.insert(0, proprietaire)

            return proprietaires

        return []

    def get_element(self, cle):
        """Retourne l'élément de type indiqué ou None."""
        elts = [e for e in self.elements if e.nom_type == cle]
        if elts:
            return elts[0]

        return None

    def get_etendue(self):
        return self.navire and self.navire.etendue or None

    def peut_affecter(self, cle_affection):
        """La salle self peut-elle être affectée par l'affection ?"""
        if cle_affection == "neige":
            return False

        return Salle.peut_affecter(self, cle_affection)

    def sabord_oriente(self, direction=None):
        """Retourne True si le sabord est orienté dans la direction.

        La direction peut être None, dans ce cas la méthode vérifie
        si un sabord existe.

        """
        if self.sabord_min is None or self.sabord_min < 0:
            return False

        if self.sabord_min + self.sabord_max == 0:
            return False

        if direction is None:
            return True

        sabord_min = (self.sabord_min - self.sabord_max) % 360
        sabord_max = (self.sabord_min + self.sabord_max) % 360
        if direction > 180:
            direction -= 360
        if sabord_min > 180:
            sabord_min -= 360
        if sabord_max > 180:
            sabord_max -= 360

        if direction < sabord_min or direction > sabord_max:
            return False

        return True

    def ajouter_element(self, element):
        """Ajoute un élément dans la salle."""
        self.mod_elements.append(element)

    def retirer_element(self, cle):
        """Retire l'élément indiqué."""
        for i, elt in enumerate(self.mod_elements):
            if elt.nom_type == cle:
                del self.mod_elements[i]
                return

        raise ValueError("l'élément {} n'a pas pu être trouvé".format(
                element))

    def noyer(self, degats):
        """Noie la salle (si noyable).

        Les dégâts doivent être un nombre supérieur à 0 qui sera utilisé tel
        quel pour donner l'estimation du poids d'eau qui sera chargé dans la
        salle dès l'impact. La voie d'eau sera créée.

        """
        if not self.noyable:
            return

        if self.voie_eau == COQUE_COLMATEE:
            degats = int(degats * 1.5)

        self.voie_eau = COQUE_OUVERTE
        self.poids_eau += degats

    def colmater(self, personnage, calfeutrage):
        """Colmate la brèche dans la coque."""
        if calfeutrage.onces_contenu == 0:
            personnage << "|err|{} est vide.|ff|".format(
                    calfeutrage.get_nom())
            return

        talent = personnage.pratiquer_talent("calfeutrage")
        if self.voie_eau > 5 and self.voie_eau > talent * 10:
            personnage << "|err|L'eau est trop haute pour vous permettre " \
                    "de travailler.|ff|"
            return False

        end = 12
        try:
            personnage.stats.endurance -= end
        except DepassementStat:
            personnage << "|err|Vous êtes trop fatigué pour cela.|ff|"
            return False

        calfeutrage.onces_contenu -= 1
        self.voie_eau = COQUE_COLMATEE
        personnage << "Vous colmatez la brèche dans la coque avec {}.".format(
                calfeutrage.get_nom())
        self.envoyer("{{}} colmate la brèche dans la coque avec {}.".format(
                calfeutrage.get_nom()), personnage)
        importeur.navigation.ecrire_suivi("{} colmate une brèche en " \
                "{}.".format(personnage.nom_unique, self.ident))

    def ecoper(self, personnage, ecope):
        """Écope dans la salle."""
        poids_max = personnage.force
        if poids_max > ecope.poids_max:
            poids_max = ecope.poids_max

        if poids_max > self.poids_eau:
            poids_max = self.poids_eau

        end = int(poids_max)
        try:
            personnage.stats.endurance -= end
        except DepassementStat:
            personnage << "|err|Vous êtes trop fatigué pour cela.|ff|"
            return False

        self.poids_eau -= poids_max
        if self.poids_eau < 0:
            self.poids_eau = 0

        personnage << "Vous écopez avec {}.".format(ecope.get_nom())
        self.envoyer("{{}} écope avec {}.".format(
                ecope.get_nom()), personnage)

    def decrire_plus(self, personnage):
        """Ajoute les éléments observables dans la description de la salle."""
        msg = []
        for element in self.elements:
            msg.append(element.get_description_ligne(personnage))

        if self.noyable and self.voie_eau == COQUE_OUVERTE:
            msg.append("Une brèche dans la coque laisse entrer l'eau " \
                    "sans contrainte.")
        elif self.noyable and self.voie_eau == COQUE_COLMATEE:
            msg.append("Une brèche hâtivement colmatée peut se voir ici.")
        if self.noyable and self.poids_eau > 1:
            if self.poids_eau < 10:
                msg.append("Une mare d'eau se trouve ici.")
            elif self.poids_eau < 25:
                msg.append("L'eau est à présent au niveau de vos chevilles.")
            elif self.poids_eau < 70:
                msg.append("Le pont disparaît sous l'eau qui atteint " \
                        "à présent vos genoux.")
            else:
                msg.append("Le bois est presque invisible sous le poids " \
                        "de l'eau envahissante.")
        return "\n".join(msg)

    def get_elements_observables(self, personnage):
        """Retourne la liste des éléments observables."""
        elts = Salle.get_elements_observables(self, personnage)
        for element in self.elements:
            elts.append(element)

        # Cherche les navires visibles
        portee = get_portee(personnage.salle)
        visible = Visible.observer(personnage, portee, 5)
        for angle, (vecteur, point) in visible.points.items():
            if hasattr(point, "get_nom_pour"):
                elts.append(point)

        return elts

    def accepte_discontinu(self):
        """Retourne True si cette salle supporte les chemins discontinu."""
        return True

    def get_sortie(self, vecteur, destination):
        """Retourne une sortie en fonction du vecteur donné."""
        if self.navire is None:
            return Salle.get_sortie(self, vecteur, destination)

        direction = (vecteur.direction - self.navire.direction.direction) % \
                360
        if 45 <= direction < 65:
            nom = "avant-tribord"
            article = "l'"
        elif 65 <= direction < 115:
            nom = "tribord"
            article = ""
        elif 115 <= direction < 165:
            nom = "arrière-tribord"
            article = "l'"
        elif 165 <= direction < 205:
            nom = "arrière"
            article = "l'"
        elif 205 <= direction < 245:
            nom = "arrière-bâbord"
            article = "l'"
        elif 245 <= direction < 295:
            nom = "bâbord"
            article = ""
        elif 295 <= direction < 335:
            nom = "avant-bâbord"
            article = "l'"
        else:
            nom = "avant"
            article = "l'"

        sortie = Sortie(vecteur.nom_direction, nom, article,
                destination, "", self)
        sortie.longueur = vecteur.norme
        return sortie

    def peut_entrer(self, personnage):
        """Si la salle est réservée à un poste."""
        if self.poste and self.navire:
            return self.navire.a_le_droit(personnage, self.poste)

        return True
