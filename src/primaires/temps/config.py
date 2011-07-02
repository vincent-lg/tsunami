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


"""Ce fichier contient la configuration par défaut du module 'temps'."""

cfg_temps = r"""
# Ce fichier contient la configuration du module temps.
# Il s'agit du temps qui passe, non de la météo.
# Dans ce fichier, vous pouvez décrire les différentes saisons, les mois
# de l'année, la vitesse à laquelle le temps s'écoule, le formatage de la
# date et de l'heure...

## Périodes temporelles
# Saisons
# Ici sont listées les saisons.
# Leur ordre d'apparition est déduit de l'écoulement des mois (voir plus bas).
saisons = [
    "hiver",
    "printemps",
    "été",
    "automne",
]

# Mois
# Les mois sont donnés dans un dictionnaire sous la forme :
#     nom_du_mois: nom_de_la_saison
mois = {
    "janvier": "hiver",
    "février": "hiver",
    "mars": "hiver",
    "avril": "printemps",
    "mai": "printemps",
    "juin": "printemps",
    "juillet": "été",
    "août": "été",
    "septembre": "été",
    "octobre": "automne",
    "novembre": "automne",
    "décembre": "automne",
}

# Nombre de jours par mois
# Si tous vos jours ont un nom, le nombre de jours est indifférent.
# Mais si vos noms de jours sont vides, le nombre est alors utilisé
# Par exemple : votre nombre de jours est 30 par mois et vos noms de jours
# ne sont pas définis. Le premier jour sera 1, le second 2, le troisième 3...
nombre_jours = 30

# Noms des jours
# Laissez une liste vide si vos jours portent simplement un numéro.
# Dans ce cas, c'est le nombre de jours par mois qui intervient.
noms_jours = []

## Date et heure initiale
# Si aucune date n'est définie, on règle la date sous la forme d'un tuple
# ne contenant que des nombres :
# (année, mois, jour, heure, minute)
# Exemple : (2011, 7, 2, 12, 7)
# pour samedi 2 juillet 2011, 12:07
reglage_initial = (1785, 5, 12, 10, 0)

## Ecoulement du temps
# Le temps s'écoule à quelle vitesse dans l'univers ?
# La réponse doit être donnée sous la forme d'une chaîne de caractère contenant
# - le numérateur
# - un slash /
# - le dénominateur
# Exemple : "3/4"
# Le numérateur est le nombre d'heures réelles qui s'écoulent
# Le numérateur est le nombre d'heures de l'univers qui s'écoulent en parallèle
# Par exemple, si vous définissez l'écoulement ainsi :
#vitesse_ecoulement = "1/5"
# 5 heures de l'univers s'écoulent pendant une heure réelle
vitesse_ecoulement = "1/1"

## Formattage de la date et l'heure
# Formatage de la date
# Le formatage doit être donné sous la forme d'une chaîne de caractère
# contenant plusieurs symboles :
# {no_j} : le numéro du jour
# {nm_j} : le nom du jour
# {no_m} : le numéro du mois
# {nm_m} : le nom du mois
# {nm_s} : # le nom de la saison
# {no_a} : le numéro de l'année
formatage_date = "{no_j} {nm_m} {no_a}"

# Formatage de l'heure
# Le formatage doit être donné sous la forme d'une chaîne de caractère
# contenant plusieurs symboles :
# {no_h} : le nombre d'heures
# {nm_h} : le nom de l'heure (comme huit heures)
# {no_m} : le nombre de minutes
# {nm_m} : le nom de minutes (cinquante-quatre)
# {no_q} : l'heure sous la forme de quart d'heure (00:45)
# {nm_q} : l'heure sous la forme de nom de quart d'heure (minuit moins le quart)
formatage_heure = "{no_h}:{no_m}"

"""
