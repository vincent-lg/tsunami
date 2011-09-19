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


"""Fichier contenant les aides su scripting."""

syntaxe = r""" 
Pour écrire une instruction, il suffit de l'entrer dans l'éditeur sans
la préfixer d'aucune option.

Il existe trois types d'instructions :
-   Les actions
-   Les conditions
-   Les affectations

L'action est une instruction qui FAIT AGIR un élément de l'univer.
Par exemple, dire quelque chose à quelqu'un, donner de l'xp à un joueur,
changer le titre d'une salle, fermer une porte, alerter les
modérateurs...
Routes ces instructions pourraient être des actions car elles effectuent
une action sur l'univers.

Les conditions sont des instructions permettant d'exécuter une ou plusieurs
actions dans un cas précis.
Par exemple :
    si stat(joueur, "force") > 10:
        dire personnage "Quelle force !"
    sinon:
        dire personnage "Encore trop faible..."
    finsi

Les conditions sont formées d'un mot-clé entre |cmd|si|ff|, |cmd|sinon si|ff|,
|cmd|sinon|ff| et |cmd|finsi|ff| qui marque la fin du bloc
conditionnel. Ce mot-clé est suivi d'un ou plusieurs tests, généralement
constitués d'une première valeur, d'un opérateur et d'une seconde valeur.
Notez que la condition |cmd|sinon|ff| et |finsi| ne sont pas suivis de test.
Enfin, un signe |cmd|:|ff| vient clôturer l'instruction, sauf si
c'est un |cmd|finsi|ff|.

L'affectation est l'instruction la plus simple. Elle affecte une valeur
à une certaine variable.
Par exemple :
nombre = 5

Des fonctions peuvent être utilisées dans les trois instructions ci-dessus.
Ce sont des outils d'interrogation qui récupèrent une certaine valeur.
Elles peuvent prendre de 0 à N paramètres (ceci est indiqué dans leur
aide respective). La valeur qu'elle retourne peut être utilisée tel quel
ou bien enregistrée dans une variable.
Par exemple, la fonction titre retourne le titre de la salle.
Elle a besoin en premier et unique paramètre la salle dont le titre
doit être récupéré.
Voici quelques exemples d'instructions utilisant cette fonction, sachant
que la variable |cmd|salle|ff| contient une salle de l'univers.

titre_salle = titre(salle)
si titre(salle) = "Une place de village:"
    dire personnage titre(salle)

Ceci n'est qu'une introduction à la syntaxe du scripting. Vous pouvez
en apprendre plus grâce aux commandes 
suivantes :
  |cmd|/?s action|ff| Affiche plus d'information sur la syntaxe des actions
  |cmd|/?s condition|ff| affiche plus d'aide sur la syntaxe des conditions
  |cmd|/?s fonction|ff| affiche plus d'aide sur la syntaxe des fonctions
  |cmd|/?s variable|ff| affiche plus d'aide sur les variables
  |cmd|/?s types|ff| affiche plus d'informations sur les types de données
  manipulés

Il vous est conseillé de lire l'aide de chacun de ces sujets avant de commencer
à scripter."""

