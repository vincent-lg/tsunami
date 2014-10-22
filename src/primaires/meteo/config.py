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

## Température dynamiqu
# Si cette donnée est à True, alors la température sera
# calculée automatiquement (en fonction de la température saisonière
# comme décrit plus bas ou des modifieurs de zone). Si cette donnée
# est à False, alors la température statique (voire plus bas) est
# choisie comme température globale.
temperature_dynamique = True

## Température statique
# Si la température dynamique (voire au-dessus) est désactivée, alors
# cette donnée doit contenir la température globale de l'univers (les
# modifieurs de zone seront appliqués comme d'habitude).
temperature_statique = 0

## Température saisonnières
# Cette donnée permet de fixer les marges minimums et maximums des
# températures saisonières. Il s'agit par exemple de définir qu'au
# mois de janvier, la température globale est entre 2 et 7°.
# La donnée est la forme d'une liste de tuples : chaque tuple, de
# deux éléments, indique la marge minimum suivie de la marge maximum
# du mois. La position dans la liste détermine le mois en question
# (le mois de janvier par exemple sera en premier, puis viendra
# février, ainsi de suite).
temperatures = [
    (1, 7),
    (0, 9),
    (2, 12),
    (5, 18),
    (8, 21),
    (14, 26),
    (18, 31),
    (22, 37),
    (20, 34),
    (12, 26),
    (2, 14),
    (-1, 8),
]

"""
