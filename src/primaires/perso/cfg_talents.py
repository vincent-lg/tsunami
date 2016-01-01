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


"""Fichier contenant la configuration de  base des talents."""

cfg_talents = r"""
# Ce fichier permet de configurer des données concernant l'apprentissage des
# talents. Notez que les talents ne sont pas configurables ici mais en dur,
# dans le code.

## Coefficient d'apprentissage des talents
# Cette donnée permet d'influencer la difficulté d'apprentissage des talents.
# Le calcul est : difficulte ** coef * 100
# Où :
# * difficulte est la difficulté d'apprentissage du talent (entre 0 et 1)
# * coef est la valeur que vous configurée ici
# Pour en savoir plus, consultez le code
# (primaires/perso/templates/talents.py - méthode estimer_difficulte)
# [NOTE]
# Un coefficient entier correspond à une harmonisation des difficultés vers
# le bas (aplatissement de la courbe pour les petites valeurs) et donc une
# hausse globale du niveau du jeu ; à l'inverse, un coefficient fractionnaire
# (1/2, 1/3...) harmonise vers le haut et baisse la difficulté du jeu.
coefficient_apprentissage = 2

"""
