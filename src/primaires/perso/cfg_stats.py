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


"""fichier contenant la configuration de  base des stats des personnages."""

cfg_stats = r"""
# Ce fichier permet de configurer les stats des personnages.
# Dans ce fichier, vous pourrez par exemple définir qu'un personnage a
# une force, une agilité, une constitution, positionner certaines valeurs
# à défaut, définir des marges et des maximums.

# A noter que ce fichier n'est pas fait pour être modifié trop souvent.
# Une fois que des joueurs se sont créés dans votre univers, il n'est pas
# très bon de retirer ou modifier des stats (vous pouvez en revanche en
# ajouter sans problème).

# Si vous souhaitez supprimer des stats, il vous faudra vérifier
# soigneusement qu'elles ne sont pas impliquées dans des calculs dans le
# reste du MUD. Si par exemple vous supprimez la stat 'agilite', il vous
# faudra sûrement modifier le calcul de réussite pour le talent 'pêche'.

# Les calculs impliquant des stats doivent se trouver dans le fichier de
# configuration 'calcul.cfg' du module les utilisant. Vous n'avez donc pas
# besoin de toucher au code pour modifier ces calculs. En outre, cela vous
# permet, même en diffusant le code de votre MUD, de laisser le joueur curieux
# dans le doute quant aux calculs qui sont fait pour réussir un talent
# particulier.

## Tableaux des stats
# Les stats sont donnés sous la forme d'un tuple de lignes. Chaque ligne
# est un tuple contenant plusieurs informations, décrites ici.
# Inspirez-vous du modèle fourni.
# Pour supprimer une stat, supprimez sa ligne.
# Les informations à entrer, dans l'ordre, sont :
# * nom : le nom de la stat, sans espaces ni caractères spéciaux
#   C'est ce nom que vous allez utiliser dans le personnage. Vous pourrez
#   appeler sa valeur courante par 'personnage.nom_stat' (par exemple
#   'personnage.force')
# * symbole : le symbole donné à la stat. C'est ce symbole, précédé du signe
#   '%', que le joueur utilisera dans sa configuration de prompt
# * défaut : la valeur par défaut de la stat pour n'importe quel personnage
#   lambda
# * marge : la marge maximum. Cette marge ne peut pas être dépassée par la
#   stat (on peut par exemple souhaiter que la force ne puisse jamais
#   dépasser 100). Vous pouvez préciser -1 ici pour définir une marge
#   infinie.
#   Notez que la marge minimum est 0.
# * max : une chaîne représentant la stat à prendre comme stat maximum.
#   Ceci est indépendant de la marge. La vitalité (ou vie) est par
#   exemple limitée par la vitalité max (ou vie max). Dans le tableau
#   représentant cette stat, le nom de la stat maximum doit être donnée
# * flags : la liste des flags de la stat, séparés par le pipe ('|')
#   Quand une stat atteint un certain nombre, une exception peut être levée.
#   Cette exception peut être interceptée au niveau de la modification pour
#   permettre des messages plus personnalisés, en cas de la mort du
#   personnage par exemple.
#   Chaque stat peut lever une exception quand elle dépasse un certain seuil.
#   Si vous laissez la colonne stat vide, l'exception I0 sera appliquée
#   par défaut.
#   Les flags existants sont :
#   * NX  : la stat ne lève aucune exception lors de sa modification
#   * I0  : la stat lève une exception si elle est strinctement inférieure à 0
#   * IE0 : la stat lève une exception si elle est inférieure ou égale à 0
#   * SM  : la stat lève une exception si elle est supérieure au MAX
#   * SEM : la stat lève une exception si elle est supérieure ou égale au MAX
stats = (
    # Nom             # Symbole | # Défaut # Marge # Max              # Flags
    ( "vitalite_max"  , 'vx'    ,     50 , 10000 , ""               , ),
    ( "mana_max"      , 'mx'    ,     50 , 10000 , ""               , ),
    ( "endurance_max" , 'ex'    ,     50 , 10000 , ""               , ),
    ( "vitalite"      , 'v'     ,     50 , 10000 , "vitalite_max"   , IE0),
    ( "mana"          , 'm'     ,     50 , 10000 , "mana_max"       , ),
    ( "endurance"     , 'e'     ,     50 , 10000 , "endurance_max"  , ),
    ( "force"         , 'f'     ,      5 ,   100 , ""               , ),
    ( "agilite"       , 'a'     ,      5 ,   100 , ""               , ),
    ( "robustesse"    , 'r'     ,      5 ,   100 , ""               , ),
    ( "intelligence"  , 'i'     ,      5 ,   100 , ""               , ),
    ( "charisme"      , 'c'     ,      5 ,   100 , ""               , ),
    ( "sensibilite"   , 's'     ,      5 ,   100 , ""               , ),
)

## Stats pouvant être entraînées
# Ce dictionnaire définit, en clé, le nom des stats pouvant être entraînées
# et en valeur le message de progression.
entrainables = {
    "force": "Votre force musculaire est maintenant plus importante.",
    "agilite": "Votre agilité est plus importante.",
    "robustesse": "Votre robustesse est plus importante.",
    "intelligence": "Vous vous sentez plus intelligent",
    "charisme": "Vous sentez votre charisme augmenter.",
    "sensibilite": "Vous sentez votre sensibilité augmenter",
}

## Stats liées
# Ce dictionnaire définit les stats dont la progression influence une
# autre stat. Indiquez en clé la stat à entraîner pour que la seconde
# progresse.
entrainement_liees = {
    "agilite": "endurance_max",
    "robustesse": "vitalite_max",
    "intelligence": "mana_max",
}

"""
