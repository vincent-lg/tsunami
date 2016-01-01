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


"""Ce fichier contient la configuration par défaut du module 'systeme'."""

cfg_droits = r"""
# Ce fichier contient la configuration des droits du module systeme.
# Il permet de paramétrer les options de sécurité du module systeme.
# Ce module permettant l'accès aux commandes systèmes de Kassie, configurer
# ces options est recommandé.
# Pour plus d'informations, consultez la documentation :
# http://redmine.kassie.fr/projects/documentation/wiki/Deploiement
# ou consultez le fichier doc/Deploiement.txt

## Commande systeme

# Active ou inactive
# Vous pouvez ici activer ou désactiver la commande système/system.
# Mettez la variable à False pour désactiver la commande ou à True sinon.
cmd_systeme = True

# Adresses IP autorisées
# Vous pouvez configurer ici une liste d'adresse IP ayant le droit
# d'utiliser la commande système/system. Notez que si la variable
# cmd_systeme est à True, un client connecté en local aura toujours
# le droit d'exécuter système/system. Cela veut dire que l'adresse
# IP 127.0.0.1 est toujours implicite dans la liste ci-dessous.
# Rajoutez les adresses IP des personnes en qui vous pouvez avoir
# confiance.
cmd_systeme_ip = []

"""
