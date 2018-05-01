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


"""Ce fichier contient la configuration du format pgsql d'exportaide."""

TEXTE_CFG = r"""
# Ce fichier contient la configuration du format 'pgsql' d'exportaide.

## Host
# Précisez l'adresse IP ou l'hôte de connexion auquel se connecter.
host = "127.0.0.1"

## Port
# Précisez ici le port de connexion à la base de données
port = 5432

## Nom d'utilisateur
# Précisez ici le nom d'utilisateur utilisé pour se connecter
dbuser = "postgres"

## Mot de passe
# Précisez ici le mot de passe de l'utilisateur
# Si aucun mot de passe n'est nécessaire, laissez une chaîne vide ("")
dbpass = ""

## Nom de la base de données
# Précisez le nom de la base de données
dbname = "dev"

## URL d'accès aux commandes
# Entrez l'URL (absolue, commençant par /) du chemin menant au détail
# d'une commande. Notez que cette adresse sera également utilisée
# pour afficher la liste des commandes.
adresse_commandes = "/aide/commandes/"

"""
