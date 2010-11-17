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


"""Ce fichier contient la configuration par défaut du module 'format'"""

cfg_charte = r"""
# Ce fichier contient la configuration du module primaire format.
# Il paramètre la "charte graphique" du moteur (raccourcis de formatage et
# quelques options).
# /!\ Ces valeurs sont nécessaires au bon fonctionnement du moteur !
# Les couleurs disponibles :
#   |nr|  - noir
#   |rg|  - rouge
#   |vr|  - vert
#   |mr|  - marron
#   |bl|  - bleu
#   |mg|  - magenta
#   |cy|  - cyan
#   |gr|  - gris
#   |grf| - gris foncé
#   |rgc| - rouge clair
#   |vrc| - vert clair
#   |jn|  - jaune
#   |blc| - bleu clair
#   |mgc| - magenta clair
#   |cyb| - cyan clair
#   |bc|  - blanc

# Couleur des commandes
# Les commandes dans les messages envoyées au client, seront signalées par la
# couleur paramétrée ci-dessous, à condition de les entourer des raccourcis
# |cmd| et |ff|. Par exemple :
# 'Entrez votre |cmd|mot de passe|ff| pour vous identifier."
couleur_cmd = "|grf|"

# Couleur des titres
couleur_titre = "|mr|"

# Couleur des messages importants
# Deux niveaux de messages, les messages de warning et les messages d'erreur.
# Raccourcis correspondantes : |att| et |err|
couleur_attention = "|vr|"
couleur_erreur = "|rg|"

# Si vous voulez ajouter des raccourcis de mise en forme, complétez ce fichier
# (sans oublier de documenter) et les dicos dans primaires.interpreteur.contexte
# et primaires.format.message. Ensuite yapuka utiliser vos raccourcis tout neufs
# dans un quelconque contexte.

# Couleur du prompt
# Ceci est la couleur du prompt, surtout utilisée lors de l'inscription.
couleur_prompt = "|cy|"

# Préfixe du prompt
# Ce préfixe est placé devant le prompt, surtout lors de l'inscription.
prefixe_prompt = "* "

"""
