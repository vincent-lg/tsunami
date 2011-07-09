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


"""Ce fichier contient la configuration par défaut du module 'scripting'."""

cfg_scripting = r"""
# Ce fichier contient la syntaxe du scripting.
# Vous pouvez configurer ici tous les éléments de la syntaxe et ainsi,
# configurer votre propre langage de script en fonction de vos préférences.
# NOTE IMPORTANTE : les informations de cette configuration sont données
# sous la forme d'expressions régulières. Si vous ne connaissez pas ce
# langage, évitez de les modifier.

## Identifiant
# Un identifiant est une variable contenant une certaine valeur.
# Cette variable peut être prédéfinie par l'évènement (l'objet qu'on ramasse,
# le PNJ auquel on parle...) ou bien définie au cours du script
# par affectation.
identifiant = r"[A-Za-z][A-Za-z0-9_]*"

## Types de données
# Les différents types admis
# Chaîne de caractères :
chaine = r"\".+\""

# Nombre :
nombre = r"-?[0-9]+(\.[0-9]+)?"

## Affectation
# L'affectation est l'instruction qui permet d'affecter une valeur à un
# identifiant. Exemple :
# variable = 5 (on affecte la valeur 5 à la variable 'variable')
# Vous pouvez utiliser :
# {identifiant} : un identifiant
# {type_de_donnee} : un type de donnée
#                    (entier, flottant, chaîne ou un autre identifiant)
affectation = r"{identifiant} ?= ?{type_de_donnee}"

## Fonctions
# Une fonction permet d'exécuter une opération précise (donner à un joueur
# un objet, dire un message, attaquer, lancer un sort...)
# Une fonction a généralement un nom et une liste d'arguments qui peut être
# vide.

# Arguments
# Séparateur entre les arguments :
sep = r", ?"

# Nom d'une fonction
nom_fonction = r"[a-z]{3,}"

# Délimiteur gauce de la liste des paramètres (parenthèse gauche en Python)
delimiteur_gauche = r"\("

# Délimiteur droit de la liste des paramètres (parenthèse droite en Python)
delimiteur_droit = r"\)"

## Conditions
# Une condition permet de faire une suite d'action dans certains cas
# Elle possède quatre mot-clés :
# if : si test
# sinon si : elif test
# sinon : else
# finsi : ce mot-clé n'a pas d'équivalent en Python qui réagit à l'indentation
si = "si {condition}:"
sinonsi = "sinon si {condition}:"
sinon = "sinon:"
finsi = "finsi"

# Opérateurs booléens
# Les opérateurs booléens sont "et", "ou"
# Ils permettent de relier des tests
# Comme si test1 et test2...
et = "et"
ou = "ou"

# Opérateurs de comparaison
# Ce sont les opérateurs utilisés pour tester une comparaison entre deux
# valeurs. Exemple : si a = b...
egal = "="
inferieur_ou_egal = "<="
inferieur = "<"
superieurou_egal = ">="
superieur = ">"
different = "!="

"""
