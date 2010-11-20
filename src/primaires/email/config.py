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


"""Ce fichier contient la configuration par défaut du module 'email'."""

cfg_email = r"""
# Ce fichier contient la configuration globale du serveur d'e-mail.
# C'est ici que vous autorisez le module 'email' à envoyer des mails, que
# vous précisez le nom d'hôte utilisé pour envoyer les messages

## Autorisation
# Si vous mettez cette donnée à False, le serveur d'e-mail sera considéré
# comme inactif. Le module primaire 'email' ne pourra donc pas envoyer
# d'e-mails.
# Notez tout de même qu'il est préférable d'avoir un serveur mail configuré
# sur le serveur hébergeant le projet.
serveur_mail = True

## Nom d'hôte
# Modifiez cette donnée pour spécifier le nom d'hôte de votre serveur
# d'e-mail. Si vous précisez "exemple.com" en nom d'hôte, les messages envoyés
# depuis l'alias "info" seront envoyés depuis l'adresse "info@exemple.com".
# Si vous précisez une chaîne vide en nom d'hôte, aucun mail ne pourra être
# envoyé. Si le serveur d'e-mail est considéré comme actif (voir plus haut)
# et que le nom d'hôte est une chaîne vide, une erreur sera loggée.
nom_hote = ""

# Adresse mail de l'administrateur
adminMail = "admin@kassie.fr"

"""
