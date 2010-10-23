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

"""Modèle du fichier de configuration du corps.

Dans ce fichier se trouve, dans une chaîne de caractère enregistrée dans la
variable 'pere',  le fichier de configuration globale par défaut.
Si des options doivent être ajoutées, elles le sont ici et seront directement
répercutées dans le fichier de configuration utilisé. Les anciennes données ne
seront naturellement pas écrasées par cette nouvelle configuration.

NOTE IMPORTANTE: les données présentes dans ce fichier sont interprétées comme
des données Python. Si vous voulez mettre une chaîne de caractère, n'oubliez
pas de l'entourer de guillemets ou d'apostrophes. Si vous voulez décrire un
chemin Windows avec des anti-slashs '\', n'oubliez pas de les échapper.

Exemple :
chemin = "C:\\kassie\\logs"

"""

pere = r"""
# Ce fichier contient des informations générales sur le projet. Il
# peut être édité manuellement. Si ces informations sont modifiées pendant
# l'exécution du projet, pour les prendre en compte il faudra demander au corps
# de recharger ces informations.

## Configuration de la connexion

# Numéro de port
# Cette option est ignorée si un port est précisé en ligne de commande
port = 4000

# Nombre maximum de clients en attente
# C'est le nombre de connexions en attente, non encore acceptées
# Il est inutile de mettre un nombre trop élevé (5 suffit sauf contraintes
# particulières)
nb_clients_attente = 5

# Nombre maximum de connectés
# Mettre à -1 pour un nombre infini de connectés
nb_max_connectes = -1


## Chemins d'accès

# Bien entendu, il est impossible de configurer ici le chemin vers les
# fichiers de configuration. Pour changer ces données, il faut directement
# éditer 'src/bases/anaconf' en changeant la valeur de la variable 'REP_CONFIG'
# ou bien passer ce chemin en argument de la ligne de commande

# Chemin vers les logs
# Si aucune valeur n'est précisée après le signe '=', c'est la configuration
# du module qui est prise en compte
# Voir la variable 'REP_LOGS' dans le fichier 'src/primaires/log/__init__.py'
# Si un chemin est précisé en argument de la ligne de commande, il est
# de toute façon prioritaire
chemin_logs = 

# Chemin vers les fichiers-données
# Si aucune valeur n'est précisée après le signe '=', c'est la configuration
# du module qui est prise en compte
# Voir la variable 'REP_ENRS' dans le fichier
# 'src/primaires/supenr/__init__.py'
# Si un chemin est précisé en argument de la ligne de commande, il est
# de toute façon prioritaire
chemin_enregistrement = 

"""
