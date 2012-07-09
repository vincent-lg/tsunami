# -*-coding:Utf-8 -*

# Copyright (c) 2012 LE GOFF Vincent
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


"""Ce fichier contient la configuration par défaut du module 'tresor'."""

cfg_tresor = r"""
# Ce fichier contient la configuration globale de la monnaie et du trésor.

## Nom d'unité
# Le nom de l'unité permet d'indiquer l'unité dans laquelle sera exprimée
# la valeur du trésor. Si l'unité est un simple signe, vous pouvez le
# préciser simplement, entre guillemets. Si l'unité est un nom (comme
# euro, dollar), vous devez le préciser d'un espace (" euro" par exemple).
unite = " unités monétaires"

## Nombre de jours de fluctuation
# Les statistiques donnent également la fluctuation du marché. En vérité,
# il s'agit simplement de l'augmentation ou la baisse de la valeur monétaire
# injectée dans l'univers. Cette statistique se base sur les statistiques
# actuelles et celles il y a X jours. Vous pouvez changer le nombre
# de jours sur lequel porte cette étude.
# Notez qu'un ombre de jours trop faible (1 ou 2) demande une consultation
# régulière, alors qu'un nombre trop élevé aura du mal à mettre
# en évidence la fluctuation rapide du marché. On parle ici de jours IRL ;
# une semaine est conseillée.
nb_jours_fluctuation = 7

"""
