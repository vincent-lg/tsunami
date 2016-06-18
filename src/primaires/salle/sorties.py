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


"""Fichier contenant la classe Sorties, détaillée plus bas;"""

from collections import OrderedDict

from abstraits.obase import *
from primaires.format.fonctions import supprimer_accents
from .sortie import Sortie

NOMS_SORTIES = OrderedDict()
NOMS_SORTIES["sud"] = None
NOMS_SORTIES["sud-ouest"] = None
NOMS_SORTIES["ouest"] = None
NOMS_SORTIES["nord-ouest"] = None
NOMS_SORTIES["nord"] = None
NOMS_SORTIES["nord-est"] = None
NOMS_SORTIES["est"] = None
NOMS_SORTIES["sud-est"] = None
NOMS_SORTIES["bas"] = None
NOMS_SORTIES["haut"] = None

NOMS_ABREGES = { # équivalent des noms abrégés
    "sud-ouest": "s-o",
    "nord-ouest": "n-o",
    "nord-est": "n-e",
    "sud-est": "s-e",
}

NOMS_ABREGES_OP = {
    "s-o": "sud-ouest",
    "so": "sud-ouest",
    "n-o": "nord-ouest",
    "no": "nord-ouest",
    "n-e": "nord-est",
    "ne": "nord-est",
    "s-e": "sud-est",
    "se": "sud-est",
}

NOMS_OPPOSES = {
    "est": "ouest",
    "sud-est": "nord-ouest",
    "sud": "nord",
    "sud-ouest": "nord-est",
    "ouest": "est",
    "nord-ouest": "sud-est",
    "nord": "sud",
    "nord-est": "sud-ouest",
    "bas": "haut",
    "haut": "bas",
}

NOMS_SORTIES_ALPHA = (
    "sud",
    "ouest",
    "nord",
    "est",
    "sud-ouest",
    "nord-ouest",
    "nord-est",
    "sud-est",
    "bas",
    "haut",
)

class Sorties(BaseObj):

    """Conteneur des sorties.
    Elle contient l'ensemble des sorties d'une salle, sous la forme de X (maximum
    10) objets Sortie.

    Voir : ./sortie.py

    """

    def __init__(self, parent=None):
        """Constructeur du conteneur"""
        BaseObj.__init__(self)
        self.parent = parent
        self._sorties = OrderedDict(NOMS_SORTIES)

        # On passe le statut en CONSTRUIT
        self._construire()

    def __getnewargs__(self):
        return ()

    def __getitem__(self, nom):
        """Retourne la sortie correspondante"""
        return self._sorties[nom]

    def __setitem__(self, nom, sortie):
        """Se charge principalement de lever une exception si
        'nom' n'est pas dans 'NOMS_SORTIES'.

        """
        if nom not in NOMS_SORTIES.keys():
            raise ValueError("le nom {} n'est pas accepté en identifiant " \
                    "de sortie".format(repr(nom)))

        self._enregistrer()
        self._sorties[nom] = sortie

    def __iter__(self):
        """Retourne chaque sortie dans l'ordre du dictionnaire."""
        sorties = [s for s in self._sorties.values() if s is not None]
        return iter(list(sorties))

    def __contains__(self, direction):
        return direction in self._sorties and self._sorties[direction] \
                is not None

    def __len__(self):
        """Retourne le nombre de sorties existantes."""
        sorties = [s for s in self._sorties.values() if \
                s and s.salle_dest]
        return len(sorties)

    @property
    def sorties_par_alpha(self):
        """Retourne la liste des sorties triées par ordre alphabétique."""
        sorties = list(self._sorties.values())
        sorties = [s for s in sorties if s and s.salle_dest]
        sorties = sorted(sorties, key=lambda sortie: NOMS_SORTIES_ALPHA.index(
                sortie.direction))
        return sorties

    def ajouter_sortie(self, direction, *args, **kwargs):
        """Ajoute une sortie.
        Le nom doit être un des noms sorties prévu et caractérise une direction.
        Les paramètres *args seront transmis au constructeur de Sortie

        ATTENTION : si une sortie existe déjà dans la direction spécifiée,
        elle sera écrasée par la nouvelle.

        """
        sortie = Sortie(direction, *args, parent=self.parent, **kwargs)
        self[direction] = sortie
        return sortie

    def supprimer_sortie(self, direction):
        """Supprime la sortie"""
        self[direction] = None

    def iter_couple(self):
        """Retourne un dictionnaire ordonné contenant les sorties
        Les sorties sont classées dans l'ordre d'auto-complétion.
        est, sud, ouest, nord
        sud-ouest, nord-ouest...

        """
        sorties = OrderedDict()
        for nom in NOMS_SORTIES_ALPHA:
            sortie = self[nom]
            if sortie:
                sorties[sortie.nom] = sortie

        return sorties.items()

    def get(self, nom, defaut=None):
        """Retourne la sortie si trouvé ou defaut."""
        try:
            return self._sorties[nom]
        except KeyError:
            return defaut

    def get_sortie_par_nom(self, nom, cachees=True, abrege=False):
        """Récupère la sortie par son nom.

        ATTENTION : la méthode __getitem__ semble faire la même chose.
        En fait, __getitem__ accepte des noms de direction immuables
        (comme 'est', 'sud-est', 'sud', 'sud-ouest'...) alors que la
        méthode courante accepte des noms de sortie (comme 'porte'
        par exemple).

        """
        nom = supprimer_accents(nom).lower()
        if abrege and nom in NOMS_ABREGES_OP:
            nom = NOMS_ABREGES_OP[nom]

        for sortie in self.sorties_par_alpha:
            s_nom = supprimer_accents(sortie.nom).lower()
            if not sortie.cachee or cachees:
                if abrege and s_nom.startswith(nom):
                    return sortie
                elif s_nom == nom:
                    return sortie

        raise KeyError("le nom de sortie {} est inconnu".format(nom))

    def get_sortie_par_nom_ou_direction(self, nom):
        """Récupère la sortie par son nom ou sa direction indifféremment.

        """
        for nom_sortie, sortie in self._sorties.items():
            if nom_sortie == nom or (sortie and sortie.nom == nom):
                return sortie

        raise KeyError("le nom de sortie {} est inconnu".format(nom))

    def sortie_existe(self, nom):
        """Retourne True si la sortie mène quelque part"""
        try:
            return self.get_sortie_par_nom_ou_direction(nom) is not None
        except ValueError:
            return False

    def get_nom_abrege(self, nom):
        """Retourne le nom abrégé correspondant"""
        if nom in NOMS_ABREGES.keys():
            nom = NOMS_ABREGES[nom]
        return nom

    def get_nom_long(self, nom, alerter=True):
        """Retourne le nom long correspondant au nom court entré.

        Si le nom n'est pas un nom de direction et que alerter est à True,
        lève une exception KeyError.

        """
        for long, abr in NOMS_ABREGES.items():
            if abr == nom:
                return long

        if nom not in NOMS_SORTIES.keys() and alerter:
            raise KeyError("La sortie {} n'existe pas".format(
                    nom))

        return nom

    def get_nom_oppose(self, nom):
        """Retourne le nom de la sortie opposée à 'nom'"""
        return NOMS_OPPOSES[nom]

    def detruire(self):
        """Destruction des sorties."""
        for sortie in self._sorties.values():
            if sortie:
                sortie.detruire()

        BaseObj.detruire(self)
