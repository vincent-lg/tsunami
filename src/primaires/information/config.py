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


"""Ce fichier contient la configuration du module information."""

cfg_info = r"""
# Ce fichier contient la configuration du module primaire information.

## Aide en jeu
# Configurez ici le message d'accueil de l'aide en jeu (commande help/aide).
accueil_aide = \
    "|tit|----------= Aide en jeu =----------|ff|\n" \
    "Bienvenue dans l'aide du jeu. Ci-dessous se trouve une liste des " \
    "sujets\nd'aide disponibles ; vous pouvez consulter chacun d'entre eux " \
    "avec la\ncommande d'aide. Cette liste n'est cependant pas exhaustive : " \
    "certains\nsujets sont organisés de manière hiérarchique et peuvent " \
    "être parcourus à\nla manière d'un cours, au fur et à mesure. De plus, " \
    "chaque sujet est aussi\naccessible par divers mots-clés. N'hésitez " \
    "pas à tenter des recherches."

## Système de tips
# Le système de tip permet d'envoyer des messages courts d'aide
# contextuelle, permettant à un nouveau joueur d'apprendre les principales
# commandes et de découvrir l'univers. Si ce système est activé, la
# première fois qu'un joueur entrera dans un magasin par exemple,
# il recevra un message lui donnant des indications sur "comment
# consulter la liste des produits en vente". Ce système est une
# façon simple et non intrusive pour apprendre les commandes usuelles
# et peut également être contrôlé par le scripting pour introduire
# l'univers. Vous pouvez l'activer ou le désactiver ici.
tips = on

"""
