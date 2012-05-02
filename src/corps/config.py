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

Dans ce fichier se trouve, dans une chaîne de caractères enregistrée dans la
variable 'pere',  le fichier de configuration globale par défaut.
Si des options doivent être ajoutées, elles le sont ici et seront directement
répercutées dans le fichier de configuration utilisé. Les anciennes données ne
seront naturellement pas écrasées par cette nouvelle configuration.

NOTE IMPORTANTE: les données présentes dans ce fichier sont interprétées comme
des données Python. Si vous voulez mettre une chaîne de caractères, n'oubliez
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

## Configuration générale

# Nom de votre MUD
nom = "Kassie"

## Configuration de la connexion

# Serveur en ligne :
# Cette option permet de paramétrer le serveur comme étant lancé ou non.
# Si le serveur n'est pas lancé, le MUD se contente de créer ses fichiers
# de configuration, charger ses modules, les initialiser mais ne charge pas
# la partie réseau et s'arrête aussitôt après. Sauf cas particulier, laissez
# cette option à True.
serveur = True

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

# Contrôle de la boucle synchro
# La boucle synchro met par défaut un peu plus de 100 ms à s'exécuter.
# Pendant ce temps, les nouveaux clients en attente sont connectés,
# les nouvelles commandes envoyées sont traitées et certaines opérations
# cycliques sont également effectuées (obtension des statistiques,
# traitement des actions différées...). Deux valeurs permettent
# de contrôler le temps que met chaque boucle synchro en moyenne :
# le temps d'attente des connexions et le temps d'attente de réception.
# Vous pouvez ici modifier leur valeur (en seconde).
# Note : plus les valeurs de ces données sont basses, plus la boucle
# sera rapide. En contre-partie, le système sera mis à plus forte
# contribution.
tps_attente_connexion = 0.05
tps_attente_reception = 0.05


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

## Configuration des modules

# Cette rubrique permet de spécifier un ordre d'instanciation,
# de configuration, d'initialisation et de destruction des modules.
# Cette configuration mélange les modules primaires et secondaires sans
# distinction.
# Note: inutile de spécifier tous les modules dans les listes. Ceux qui
# ne sont pas précisés seront traités dans le désordre, après ceux spécifiés.
# Tous les modules sont automatiquement chargés.
# En revanche, les modules placés dans la liste 'modules_a_ignorer' ne
# sont pas instanciés, mais supprimés de l'importeur.

# Ordre d'instanciation des modules
modules_a_instancier = ['supenr']

# Ordre de configuration des modules
modules_a_configurer = ['supenr']

# Ordre d'initialisation des modules
modules_a_initialiser = ['supenr', 'interpreteur']

# Ordre de destruction des modules
# ATTENTION ! Ces modules ne seront pas ceux détruits en premier mais bien
# ceux à détruire en dernier, après les autres modules non spécifiés.
modules_a_detruire = []

# Liste des modules à ignorer (ils ne seront pas instanciés, mais quand même
# chargés)
modules_a_ignorer = []

"""
