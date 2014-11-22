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


"""Fichier contenant les constantes de navigation."""

# Facteurs des allures
ALL_DEBOUT = 140
ALL_PRES = 125
ALL_BON_PLEIN = 105
ALL_LARGUE = 75
ALL_GRAND_LARGUE = 40

# Orientation des voiles
ANGLE_DEBOUT = 0
ANGLE_PRES = 8
ANGLE_BON_PLEIN = 20
ANGLE_LARGUE = 30
ANGLE_GRAND_LARGUE = 60
ANGLE_ARRIERE = 90

# Vitesse
TPS_VIRT = 3
DIST_AVA = 0.4
CB_BRASSES = 3.2 # combien de brasses dans une salle

# Vitesse des rames
VIT_RAMES = {
    "arrière": -0.5,
    "immobile": 0,
    "lente": 0.3,
    "moyenne": 0.7,
    "rapide": 1.1,
}

# Endurance consommée par vitesse
END_VIT_RAMES = {
    "arrière": 2,
    "immobile": 0,
    "lente": 1,
    "moyenne": 3,
    "rapide": 6,
}

# Terrains
TERRAINS_ACCOSTABLES = [
    "quai de pierre",
    "quai de bois",
    "plage de sable blanc",
    "plage de sable noir",
    "rocher",
]

TERRAINS_QUAI = [
    "quai de bois",
    "quai de pierre",
]

# Dégâts sur la coque
COQUE_INTACTE = 0
COQUE_COLMATEE = 1
COQUE_OUVERTE = 2

# Modification du vent en fonction de la météo
PERTURBATIONS = {
        "grele": 0.5,
        "neige": 0.3,
        "nuages": 0.1,
        "nuages_fins": -0.2,
        "nuages_neige": 0.1,
        "orage": 2,
        "pluie": 1.5,
        "tempete_neige": 3,
}


# Fonctions
def get_portee(salle):
    """Retourne la portée à laquelle on peut voir depuis la salle spécifiée."""
    navire = salle.navire
    etendue = navire.etendue
    alt = etendue.altitude
    hauteur = salle.coords.z - alt
    portee = 50 + 50 * hauteur
    if importeur.temps.temps.il_fait_nuit:
        portee = round(portee / 2)
        perturbation = importeur.meteo.get_perturbation(salle)
        if perturbation and perturbation.est_opaque():
            portee = round(portee / 3)

    return portee

def get_vitesse_noeuds(distance):
    """Retourne la vitesse en noeuds.

    La distance précisée en paramètre est la norme d'un vecteur de
    déplacement dans l'univers. La distance entre deux salles est de
    1. La vitesse en noeuds est calculée en utilisant la vitesse
    d'écoulement, telle que définie dans le module temps. Un noeud
    est un mille par heure : un mille est 1000 brasses et le nombre
    de brasses doit être utilisé pour connaître la distance. L'heure
    est une heure IG, donc la vitesse de l'écoulement du temps est
    nécessaire.

    """
    vit_ecoulement = importeur.temps.cfg.vitesse_ecoulement
    vit_ecoulement = eval(vit_ecoulement)
    distance = distance * CB_BRASSES / 1000
    distance = distance / (TPS_VIRT / DIST_AVA)
    distance *= vit_ecoulement
    return distance * 3600

def get_nom_distance(distance):
    """Retourne le nom de la distance du vecteur précisé.

    Cette fonction attend en argument une distance (un vecteur de
    la classe primaires.vehicule.vecteur.Vecteur). Elle retourne la
    distance en terme de brasses, encablures ou milles.

    """
    nb_brasses = round(distance.norme * CB_BRASSES)

    if nb_brasses > 100000: # Très grande distance
        msg_dist = "plus de cent milles"
    elif nb_brasses > 50000:
        msg_dist = "plus de cinquante milles"
    elif nb_brasses > 10000:
        nb = round(nb_brasses / 10000) * 10
        msg_dist = "près de {} milles".format(nb)
    elif nb_brasses > 2000:
        nb = round(nb_brasses / 1000)
        msg_dist = "près de {} milles".format(nb)
    elif nb_brasses > 1000:
        msg_dist = "près d'un mille"
    elif nb_brasses > 200:
        nb = round(nb_brasses / 100)
        msg_dist = "près de {} encablures".format(nb)
    elif nb_brasses > 100:
        msg_dist = "près d'une encablure"
    elif nb_brasses > 50:
        nb = round(nb_brasses / 10) * 10
        msg_dist = "près de {} brasses".format(nb)
    elif nb_brasses > 20:
        nb = round(nb_brasses / 5) * 5
        msg_dist = "près de {} brasses".format(nb)
    elif nb_brasses > 10:
        nb = round(nb_brasses / 2) * 2
        msg_dist = "près de {} brasses".format(nb)
    else:
        msg_dist = "près d'une brasse"

    return msg_dist
