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


"""Ce fichier contient la configuration par défaut du module 'salle'."""

cfg_salle = r"""
# Ce fichier contient la configuration globale du module primaire 'salle'.
# Vous y trouverez plusieurs options de configuration liées aux salles,
# documentées ci-dessous.

## Salle d'arrivée
# Cette salle est celle dans laquelle tout joueur nouvellement créé sera
# placé. Elle sera créée par défaut si elle n'existe pas ou n'a pas pu
# être chargée.
# Précisez l'identifiant de la salle sous la forme 'zone:mnémonic'.
# Par exemple : "depart:1"
salle_arrivee = "depart:1"

## Salle de retour
# Cette salle est celle dans laquelle un joueur se retrouve si la salle
# dans laquelle il était au moment de se déconnecter a été effacée ou est
# introuvable.
# Tout comme la salle d'arrivée, précisez l'identifiant sous la forme
# 'zone:mnémonic'.
salle_retour = "depart:1"

## Feux
# Vous pouvez ici paramétrer les messages affichés dans les salles lorsqu'un
# feu y brûle. Le message est fonction de la puissance du feu (entre 1 et 100),
# (10, message) signifiant que le message sera affiché jusqu'à 10.
messages_feu = (
    (1, "Un tas de cendres éparses diffuse une douce chaleur."),
    (5, "Un feu de camp expire ses dernières flammes, essouflé."),
    (8, "Un petit feu ronfle de temps en temps et lance quelques étincelles."),
    (15, "Un beau feu de camp crépite gaiement et darde ses flammes vers le ciel."),
    (25, "Un feu crépitant flamboie avec ardeur, débordant d'étincelles."),
    (30, "Les flammes d'un feu de camp montent et menacent d'échapper du foyer."),
    (45, "Un début d'incendie menace, envahissant peu à peu les lieux."),
    (60, "Un brasier enthousiaste flamboie ici et vous roussit le poil."),
    (75, "Une fournaise étouffante vous prend à la gorge et menace de vous consummer."),
    (100, "Un véritable bûcher se dresse tout autour de vous, sans espoir de survie."),
)

"""
