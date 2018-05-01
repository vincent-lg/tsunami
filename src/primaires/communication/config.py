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


"""Ce fichier contient la configuration du module communication."""

cfg_com = r"""
# Ce fichier contient la configuration du module primaire communication.
# Il définit les couleurs de quelques commandes et des options pour les canaux.
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
#   |cyc| - cyan clair
#   |bc|  - blanc

## Coloration des commandes

# Commande tell / parler, reply / repondre
couleur_tell = "|vrc|"

## Canaux automatiquement créés

# Ces canaux sont créés au lancement du moteur s'ils n'existent pas.
# Vous pouvez en ajouter ou en supprimer à votre guise. Les flags
# utilisables sont : PRIVE, MUET, INVISIBLE, IMM_AUTOCONNECT et
# PERSO_AUTOCONNECT. Ces deux derniers permettent de connecter automatiquement
# un Immortel lors de sa promotion ou tout joueur lors de sa création.

liste_canaux = (
    # Nom  | Couleur | Flags
    ("hrp" , "|cyc|" , PERSO_AUTOCONNECT),
    ("imm" , "|jn|"  , PRIVE | INVISIBLE | IMM_AUTOCONNECT),
)

## Canal info

# Ce canal automatiquement créé relaie dans l'univers les informations
# générales. Vous pouvez paramétrer quelques-uns de ses attributs.

# Couleur
couleur_info = "|gr|"

# Résumé
resume_info = "canal d'information"

"""
