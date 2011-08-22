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


"""Ce fichier contient la configuration du module météorologique."""

cfg_meteo = r"""
# Ce fichier décrit le comportement de la météorologie dans l'univers.

# Message affiché lorsqu'il fait beau
beau_temps = "L'atmosphère est claire, le ciel pur, libre de tout nuage."

# Nombre maximum de perturbations météorologiques simultanées
# Choisissez-le en fonction de la taille de votre univers ; la taille
# moyenne d'une perturbation est d'environ 15 cases.
nb_pertu_max = 3

# Sens du vent chaque mois
vents = [
    ("janvier", "nord"),
    ("février", "nord-est"),
    ("mars", "est"),
    ("avril", "sud-est"),
    ("mai", "sud"),
    ("juin", "sud-ouest"),
    ("juillet", "ouest"),
    ("août", "nord-ouest"),
    ("septembre", "nord"),
    ("octobre", "nord-est"),
    ("novembre", "est"),
    ("décembre", "sud-est"),
]

"""
