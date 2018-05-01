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


"""Fichier contenant les aides du scripting."""

syntaxe = r"""Tout script se compose d'instructions, chacune écrite sur une ligne, et
qui sont exécutées au fur et à mesure par le système de scripting. Pour
écrire une instruction, il suffit de l'entrer dans l'éditeur sans la
préfixer d'aucune option.

Il existe trois types d'instructions :
-   les affectations ;
-   les actions ;
-   les conditions.


L'affectation est l'instruction la plus simple : elle affecte une valeur
à une variable. Dans la suite du script, on pourra utiliser cette variable
ou la redéfinir. A noter que certaines variables sont définies par défaut
par les événements édités.

Un exemple d'affectation :
|bc|>>> age = 5|ff|
Par la suite, la variable age gardera la valeur 5 jusqu'à ce que vous la
modifiiez.


Les actions sont des instructions qui font agir un élément de l'univers ;
par exemple, dire quelque chose à quelqu'un, donner de l'xp à un joueur,
changer le titre d'une salle, fermer une porte, alerter les modérateus...
Toutes ces instructions pourraient être des actions car elles opèrent
un changement sur l'univers.

Un exemple d'action :
|bc|>>> dire personnage "Bouh !"|ff|
Cette action se contente de dire 'Bouh !' au personnage.


Les conditions sont des instructions permettant d'exécuter une ou plusieurs
actions dans certains cas précis.
Une condition est formée d'un mot-clé (|cmd|si|ff|, |cmd|sinon si|ff| ou |cmd|sinon|ff|) suivi
d'un ou plusieurs tests (généralement une valeur, un opérateur conditionnel
puis une seconde valeur) ; la condition est clôturée par un signe |cmd|:|ff|. Le
bloc d'instructions placé entre une condition et la suivante (ou le |cmd|finsi|ff|
qui vient fermer le dernier bloc) s'exécute si la condition est vérifiée.
Notez que le |cmd|sinon|ff| n'est pas suivi de test, pour la simple raison qu'il
s'exécute si aucune autre condition n'a été vérifiée.

Un exemple de condition, plus parlant :
|bc|>>> si stat(joueur, "force") > 10:
...     dire personnage "Quelle force !"
... sinon:
...     dire personnage "Encore trop faible..."
... finsi|ff|
Ce script affiche au joueur un message calibré en fonction de sa force, de
manière assez intuitive.


Des fonctions peuvent être utilisées dans les trois instructions ci-dessus.
Ce sont des outils d'interrogation qui récupèrent une certaine valeur. Elles
peuvent prendre de 0 à N paramètres (ceci est indiqué dans leurs aides
respectives) ; la valeur qu'elles retournent peut être utilisée telle
quelle ou bien enregistrée dans une variable.
Par exemple, la fonction |cmd|titre|ff| retourne le titre de la salle. Elle a
besoin en premier et unique paramètre la salle dont le titre doit
être récupéré.

Un exemple utilisant cette fonction (la variable |cmd|salle|ff| contient une
salle de l'univers) :
|bc|>>> titre_salle = titre(salle)
... si titre_salle = "Une place de village"
...     dire personnage titre(salle)|ff|


Enfin, un dernier type d'instruction s'ajoute à ceux vus plus haut : les
commentaires. Il s'agit d'instructions non prises en compte par le système
de scripting, et que vous pouvez placer n'importe où dans votre script.
Pour écrire un commentaire, vous devez commencer par un signe dièse : #.
Par exemple :
|bc|>>> degats = estimer(force_joueur, robustesse_cible)
... # Le code ci-dessus estime les dégâts reçus selon les caractéristiques.|ff|

Cette dernière ligne n'aura aucun effet ; son utilité est simplement de vous
rappelez la signification de votre code, par exemple s'il est compliqué
et que vous y revenez après ne pas y avoir touché pendant longtemps.
Commenter un script peut s'avérer très utile, même si vous n'en ressentez
pas le besoin au premier abord.


Ceci n'est qu'une introduction à la syntaxe du scripting. Vous pouvez en
apprendre plus grâce aux commandes suivantes :
  |cmd|/?s action|ff| : affiche plus d'information sur la syntaxe des actions
  |cmd|/?s condition|ff| : affiche plus d'aide sur la syntaxe des conditions
  |cmd|/?s fonction|ff| : affiche plus d'aide sur la syntaxe des fonctions
  |cmd|/?s variable|ff| : affiche plus d'aide sur les variables
  |cmd|/?s types|ff| : affiche plus d'informations sur les types de données
  manipulés

Il vous est conseillé de lire l'aide de chacun de ces sujets avant de
commencer à scripter."""

