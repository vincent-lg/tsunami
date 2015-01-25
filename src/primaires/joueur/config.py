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


"""Ce fichier contient la configuration par défaut du module 'joueur'."""

cfg_joueur = r"""
# Ce fichier contient la configuration du module primaire joueur.
# Il contient diverses options en rapport avec la création d'un personnage.

## Taille du nom

# Cette variable correspond à la taille minimale d'un nom de personnage :
taille_min = 3

# Taille maximale d'un nom :
taille_max = 15

## Groupe par défaut
# Quand un joueur se crée, dans quel groupe doit-il être placé ?
# Rappel : les groupes déterminent les droits des joueurs à utiliser
# certaines commandes, ainsi que certains flags.
# Par défaut, trois groupes existent : "pnj", "joueur" et "administrateur"
# Les joueurs sont placés par défaut dans le groupe "joueur".
groupe_par_defaut = "joueur"

## Configuration du joueur système
# Le joueur système est un joueur créé par le système qui peut être amené
# à effectuer des tâches d'administration automatisées.
# On ne doit pas pouvoir se logger sur ce joueur, mais il peut servir
# à envoyer de façon automatisée des messages.
# Par exemple, quand une erreur survient lors de l'interprétation du scripting,
# c'est le joueur système qui envoie le message au bâtisseur pour l'en avertir.
# La variable ci-dessous configure le nom du compte système :
compte_systeme = "systeme"

# Nom du joueur système :
joueur_systeme = "système"

## Choix des contextes de création d'un joueur
# Quand un client veut créer un joueur, il passe par plusieurs
# étapes (appelées contextes) qui lui permettent de sélectionner
# différentes informations sur le joueur (son nom, race, genre,
# etc). Vous pouvez changer l'ordre des contextes de création dans
# cette configuration en éditant la liste suivante. Précisez le nom
# des contextes tels qu'indiqués ci-dessous :
# "choix_genre" : choix du genre (doit venir après "choix_race")
# "choix_race" : choix de la race
# "langue_cmd" : choix de la langue des commandes
# "nouveau_nom" : choix du nom du joueur
# "presenter_tips" : présentation des messages tips à suivre
ordre_creation = ["nouveau_nom", "langue_cmd", "choix_race", "choix_genre"]

"""
