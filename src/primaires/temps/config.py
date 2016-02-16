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
# Les mois sont donnés dans une liste de paires sous la forme :
#   ("nom du mois", "nom de la saison"),
mois = [
    ("janvier", "hiver"),
    ("février", "hiver"),
    ("mars", "hiver"),
    ("avril", "printemps"),
    ("mai", "printemps"),
    ("juin", "printemps"),
    ("juillet", "été"),
    ("août", "été"),
    ("septembre", "été"),
    ("octobre", "automne"),
    ("novembre", "automne"),
    ("décembre", "automne"),
]

# Nombre de jours par mois
# Si tous vos jours ont un nom, le nombre de jours est indifférent.
# Mais si vos noms de jours sont vides, le nombre est alors utilisé
# Par exemple : votre nombre de jours est 30 par mois et vos noms de jours
# ne sont pas définis. Le premier jour sera 1, le second 2, le troisième 3...
nombre_jours = 30

# Noms des jours
# Laissez la liste vide si vos jours portent simplement un numéro.
# Dans ce cas, c'est le nombre de jours par mois qui intervient.
noms_jours = []

# Alternance jour / nuit
# Pour chaque saison, précisez l'heure du lever et du coucher de soleil.
alternance_jn = [
    ("hiver", 8, 20),
    ("printemps", 7, 21),
    ("été", 6, 22),
    ("automne", 7, 21),
]

## Date et heure initiales

# Si aucune date n'est définie, on règle la date sous la forme d'un tuple
# ne contenant que des nombres :
# (année, mois, jour, heure, minute)
# Exemple : (2012, 12, 21, 0, 0)
# pour vendredi 21 décembre 2012, 00:00
reglage_initial = (1785, 5, 12, 10, 0)

## Ecoulement du temps

# A quelle vitesse s'écoule le temps dans l'univers ?
# La réponse doit être donnée sous la forme d'une chaîne de caractère contenant
# - le numérateur
# - un slash /
# - le dénominateur
# Exemple : "3/4"
# Le numérateur est le nombre d'heures réelles qui s'écoulent
# Le dénominateur est le nombre d'heures de l'univers qui s'écoulent
# en parallèle.
# Par exemple, si vous définissez l'écoulement ainsi :
# vitesse_ecoulement = "1/5"
# 5 heures de l'univers s'écoulent pendant une heure réelle
vitesse_ecoulement = "1/4"

## Formatage de la date et l'heure

# Formatage de la date
# Le formatage doit être donné sous la forme d'une chaîne de caractère
# contenant plusieurs symboles :
# {no_j} : le numéro du jour
# {nm_j} : le nom du jour
# {no_m} : le numéro du mois
# {nm_m} : le nom du mois
# {nm_s} : le nom de la saison
# {no_a} : le numéro de l'année
formatage_date = "{no_j} {nm_m} {no_a}"

# Formatage de l'heure
# Le formatage doit être donné sous la forme d'une chaîne de caractère
# contenant plusieurs symboles :
# {no_h} : le nombre d'heures
# {nm_h} : le nom de l'heure (comme huit heures)
# {no_m} : le nombre de minutes
# {nm_m} : le nom des minutes (cinquante-quatre)
# {no_q} : l'heure sous la forme de quart d'heure (00:45)
# {nm_q} : l'heure sous la forme de nom de quart d'heure (minuit et quart)
formatage_heure = "{no_h}:{no_m}"

## Affichage physique de l'heure

# Il s'agit de la manifestation concrète du temps qui passe : la plus
# évidente de ces manifestations est bien sûr le soleil qui se déplace dans
# le ciel, mais dans un univers plus fantaisiste on pourrait imaginer d'autres
# marques d'écoulement du temps.

# Une heure avant le lever du soleil
pre_lever = "Une ligne pâle borde l'horizon est, trahissant l'éminence de " \
    "l'aube."
# L'heure qui suit le lever du soleil
post_lever = "Le soleil se hisse au-dessus de l'horizon est, perçant " \
    "l'atmosphère matinale."
# Jusqu'à midi
matinee = "Le soleil matinal poursuit sa lente ascension vers le zénith."
# Midi
midi = "Plus brillant que jamais, le soleil luit au plus haut de sa " \
    "trajectoire."
# Jusqu'une heure avant le coucher du soleil
apres_midi = "Lentement mais sûrement, le soleil descend vers l'horizon ouest."
# Une heure avant le coucher du soleil
pre_coucher = "Les derniers rayons du soleil déclinant embrasent l'atmosphère."
# L'heure qui suit le coucher du soleil
post_coucher = "Les premières étoiles s'allument dans la nuit encore claire."
# Jusqu'une heure avant le lever du soleil le lendemain
nuit = "La voûte céleste vous surplombant est sombre, piquetée d'étoiles " \
    "lointaines."

# Messages de lever et coucher de soleil
msgs_lever = (
        "Le soleil se lève à l'est.",
)

msgs_coucher = (
        "Le soleil se couche à l'ouest.",
)

# Synchronisation avec le temps réel
# Cette valeur permet de spécifier si le temps IRL et le temps IG
# doivent être synchronisés. Activer cette option permet d'avoir un
# temps dans le jeu parfaitement aligné avec le temps réel, suivant
# l'écoulement configuré, mais ce réglage peut occasionner une
# certaine latence si le MUD n'est pas lancé en permanence.
synchroniser = False

"""
