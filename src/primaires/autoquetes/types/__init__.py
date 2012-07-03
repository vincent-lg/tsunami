# -*-coding:Utf-8 -*

# Copyright (c) 2012 LE GOFF Vincent
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

"""Package définissant les types d'autoquêtes.

Il ne contient que de la documentation des types de quêtes.

Chaque type de quête est définie dans un sous-package du nom du type.
Ce sous-package contient au minimum :
    Un fichier __init__.py contenant la classe définissant le type de quête
    Un fichier editeur.yml définissant des informations propres à l'édition.

Ces deux fichiers sont étudiés par la suite. Suivez cette documentation
pour ajouter un nouveau type de quête.

1. Création du répertoire contenant le type d'autoquêtes

C'est le plus simple. Créer, à la racine de ce package, un répertoire
qui définira un type de sous-quête. Donenz-lui un nom Python valide assez
proche du nom qui sera affiché en définitive. Si possible, faites tenir
ce nom en un seul mot, tout en minuscule, les espaces éventuels sont
remplacés par des signes soulignés (_). Pour des raisons d'encodage,
évitez également les accents au sein du nom de package.

2. Créer la classe AutoQuete

Il faut ensuite créer le fichier __init__.py qui doit contenir la classe
AutoQuete. Elle n'a pas à hériter d'une autre classe (le système se chargera
de l'héritage dynamiquement avec intelligence).

A. Les attributs de la classe AutoQuete

Les attributs de classe disponibles (devant être définies dans le corps de la classe) sont :
    nom_type -- le nom du type d'autoquête (str). C'est le nom qui sera
                affiché côté bâtisseur au moment de choisir ou consulter
                le type d'une autoquête. Ce nom peut être celui du
                sous-package créé précédemment ou être différent (inclure
                des accents ou des espaces si vous le souhaitez).
    parent   -- le nom de la classe parente du type créé. Utilisez le
                nom_type de la classe parente.
    concrete -- défini si la classe est concrète (True) ou abstraite (False)
                Une classe abstraite intermédiaire doit avoir cet attribut
                à False. Pour simplifier, si une classe a cet attribut
                à True, elle peut être instanciée et donc servira de type
                d'autoquête. Sinon, elle ne pourra pas être instanciée
                et ne sert dans votre hiérarchie qu'à définir des classes
                de laquelle hériteront plusieurs types d'autoquêtes distincts.
                Un exemple de classe abstraite (concrete = False) pourrait
                être une classe QueteSurPNJ qui sera utilisé comme classe
                parente des autoquêtes Coursier, Courrier, Executeur,
                toutes trois concrètes (concrete = True).

Quant aux attributs d'instance (définis dans le constructeur), vous
pouvez en définir certains propres à votre type de quête. Sachez
également que ceux définis dans les classes parentes seront également
accessibles.

C. Méthode pouvant être redéfinies

Les méthodes pouvant être redéfinies sont :
    __init__(self)
        Constructeur de la classe. Vous pouvez y définir de nouveaux
        attributs d'instance.
    est_complete(self, personnage)
        Méthode retournant True si l'autoquete a été complétée par
        le personnage passé en paramètre.

D. Voir aussi

Vérifiez la documentation et la structure des classes que vous définissez
comme parent. Ceratines subtilités y sont indiqués, notamment la liste
des attributs que vous pouvez utiliser rien qu'en se basant sur ces
types. N'oubliez pas que les classes sont virtuellement liées par l'héritage,
donc de nouveaux attributs peuvent être définis à différents niveaux
de la hiérarchie. Assurez-vous de ne pas simplement regarder la classe
indiquée comme parent mais aussi son parent, ainsi de suite jusqu'en haut
de la hiérarchie.

3. Définir l'éditeur

Pour CHAQUE classe de la hiérarchie des types de quêtes, on trouve
généralement un fichier editeur.yml (dans le sous-package du type) définissant
les informations éditables dans l'éditeur d'autoquêtes.

Souvenez-vous qu'un type de Quete offre généralement des spécificités importantes. Par exemple, l'autoquête Coursier peut avoir besoin :
    De savoir quel PNJ donne la quête
    De connaître la "liste de courses" (la liste des objets demandés au joueur)
    De savoir combien de temps attendre avant de reproposer la même autoquête au même joueur.

Ces informations doivent être entrées par le bâtisseur créant la quête
et doivent donc être éditables dans un éditeur. Le fichier editeur.yml
spécifie quels sont les informations configurables pour ce type de quête.
Là encore, une quête héritant implicitement d'une autre possède également
les informations édfitables pour le type parent.

La structure du fichier editeur.yml est simple :
Chaque information éditable se trouve dans un bloc à part. Les informations spécifiques à la donnée devant être modifiée se trouvent au-dessous. L'indentation permet de repérer la structure des blocs. Voici un exemple clair :

# Début du bloc YAML
- temps d'attente avant de reproposer la quête:
    attribut: tps_attente
    type: entier
    minimum: 1
    aide: >
      Entrez le |ent|nombre de jours IRL|ff| à attendre avant de proposer
      de nouveau la même auto-quête au même personnage.
# Fin du bloc YAML

Dans l'ordre :

* La première ligne donne le nom affiché de la donnée à configurer.
  Elle commence par un tiret suivi d'un espace et du nom de l'information.
  Elle se termine par le signe ':' (car le détail de la configuration se
  trouve au-dessous, légèrement indenté).
* On définit ensuite le nom de l'attribut qui sera modifié (ici, tps_attente)
* On définit ensuite le type d'information à modifier. Cela influence bien
  entendu l'éditeur qui sera sélectionné pour éditer l'information. Ici,
  le type choisi est entier (c'est un nombre entier que l'on attend) et
  l'éditeur entier sera sélectionné (la liste des éditeurs possibles
  est listée plus bas, ainsi que les paramètres qu'ils attendent).
* On définit ensuite la configuration de nom 'minimum'. Cette donnée
  de configuration fait parti de celels qui sont attendues par le type
  entier (là encore, voire plus bas).
* Les dernières lignes définies l'aide spécifiée pour éditer cette
  information. C'est un message plus explicite pour le bâtisseur qui paramètre
  l'information. Notez que la première ligne, 'aide: >', se termine par
  le signe supérieur (>). Cela signifie que le texte qui suit (légèrement
  indenté là encore) sera entièrement sélectionné, même si il se trouve sur
  plusieurs lignes. Les sauts de lignes et l'indentation seront ignorés
  donc le texte sera de nouveau formatté avant d'être affiché au bâtisseur.

A. Informations à préciser invariablement

Quelque soit le type d'information, il existe des informations qu'il faut
toujours préciser et certaines, optionnelles, qui ont cours pour tous les
types.

Informations obligatoires :
    type -- le type d'information (voire les types disponibles plus bas)
    aide -- le message d'aide à afficher pour le bâtisseur.

Informations optionnelles :
    attribut -- le nom de l'attribut
                Si il n'est pas précisé, la quête-même est prise comme
                type édité. Ceci est par définition rare.

B. entier

Le type d'information entier doit être précisé quand on souhaite modifier un nombre entier.

Informations obligatoires : aucune

Informations facultatives :
    minimum -- le nombre minimum pouvant être précisé (aucune limite si absent)
    maximum -- le nombre maximum pouvant être précisé (idem)
    unite -- l'unité spécifiée (comme kg, $, €, ...)

C. flottant

Ce type permet d'éditer un nombre flottant.

Informations obligatoires : aucune

Informations facultatives :
    minimum -- le nombre minimum pouvant être précisé (aucune limite si absent)
    maximum -- le nombre maximum pouvant être précisé (idem)
    unite -- l'unité spécifiée (comme kg, $, €, ...)

D. ligne

Ce type permet d'éditer une ligne de texte. Il s'agit d'une seule ligne,
pas une description (plutôt comme un titre ou un unique message). L'information
modifiée est de type str.

Informations obligatoires : aucune

Informations facultatives : aucune

E. description

Le type description permet, comme son nom l'indique, d'éditer une description
(c'est un type particulier, pas str mais Description qui est défini dans
primaires.format.description).

Informations obligatoires : aucune

Informations facultatives : aucune

"""
