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
