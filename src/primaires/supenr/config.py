# -*-coding:Utf-8 -*

# Copyright (c) 2010-2017 LE GOFF Vincent
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


"""Ce fichier contient la configuration par défaut du module 'supenr'."""

cfg_supenr = r"""
# Ce fichier contient la configuration du module primaire supenr.
# Ce module est responsable de l'enregistrement de tout le MUD en
# mémoire. Deux modes d'enregistrement sont poroposés : 'pickle', le
# mode par défaut, qui enregistre toute la sauvegarde dans un fichier
# binaire grâce au module 'pickle'. Et 'mongo', qui essaye de se
# connecter à un serveur MongoDB (grâce à 'pymongo') pour enregistrer
# ses informations. Pour un MUD aux proportions assez modestes,
# 'pickle' est préférable car il est bien plus facile à déployer
# (il ne nécessite aucune bibliothèque supplémentaire). L'alternative
# 'mongo' permet cependant plus de contrôle sur la sauvegarde et est
# préférable si la taille de l'univers est assez importante.

## Mode d'enregistrement
# Choisissez 'pickle' ou 'mongo' ci-dessous. 'mongo' nécessite la
# bibliothèque 'pymongo' et la mise en place d'un serveur MongoDB.
# Si la connexion au serveur échoue, le système repasse automatiquement
# sur 'pickle' après avoir loggé l'erreur.
mode = 'pickle'

## Nom de la base MongoDB
# Cette option est utile si vous comptez utiliser le mode 'mongo'.
# Il s'agit simplement du nom de la base de données qui sera créée
# ou lue.
nom_mongodb = "tsunami"

"""
