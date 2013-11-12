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


"""Fichier contenant la classe SalleNavire, détaillée plus bas."""

from collections import OrderedDict

from primaires.salle.salle import Salle
from primaires.salle.sortie import Sortie
from secondaires.navigation.constantes import *

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
        self.sabord_min = None
        self.sabord_max = 0

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

    def get_element(self, cle):
        """Retourne l'élément de type indiqué ou None."""
        elts = [e for e in self.elements if e.nom_type == cle]
        if elts:
            return elts[0]

        return None

    def get_etendue(self):
        return self.navire and self.navire.etendue or None

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
        return sortie
