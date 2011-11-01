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


"""Fichier contenant la configuration de  base des niveaux."""

cfg_niveaux = r"""
# Ce fichier permet de configurer le nombre de niveaux et d'expériences
# disponibles dans votre MUD.
# Notez qu'une courbe en x ** 2 (X carré) est utilisé pour modéliser
# votre grille d'expérience. Si ce modèle ne vous convient pas,
# vous pouvez modifier le calcul dans src/perso/niveaux.py, méthode
# calculer_grille.

## Nombre de niveaux
# Cette variable modifie le nombre de niveaux.
# Elle doit être supérieure ou égale à 2.
nb_niveaux = 10

## Expérience minimum
# Cette variable détermine l'expérience pour passer du niveau 1 au niveau 2.
xp_min = 1

## Expérience maximum
# Cette variable détermine l'expérience entre l'avant-dernier et le
# dernier niveau.
# Avec ces trois informations, le système calcule une progression.
xp_max = 100

"""
