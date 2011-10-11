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


"""Ce package contient l'ensemble des modules primaires du projet.

Chaque module primaire possède son propre package.

Les modules primaires ayant des relations d'interdépendance entre eux, un
ordre d'instanciation est défini dans la configuration du corps
(voir src/corps/config.py). Tout ce qui n'est pas dans
l'ordre d'instanciation sera instancié par la suite, après les modules
définis.

Règles d'interdépendance :
- un module primaire peut faire appel aux autres modules primaires
- un module primaire ne peut faire appel à un module secondaire, sauf
  s'il utilise des méthodes génériques aux modules servant à modifier
  son état, ou à l'interprétation de commandes
- le corps du projet peut interagir avec les modules primaires

Pour obtenir une aide sur chaque module primaire, consulter le fichier
__init__.py du package concerné.

NOTE: les modules primaires et secondaires ne doivent pas porter de noms
identiques, susceptibles d'entrer en conflit.

Voici un résumé des modules primaires existants :
-   aide            Module gérant les sujets d'aide in-game
-   combat          Module gérant le combat rapproché
-   commerce        Module gérant les magasins et transactions    
-   communication   Module gérant la communication dans l'univers
-   connex          Module proche des clients, chargé des connexions,
                    créations de compte, interprétation des commandes
-   diffact         Module gérant les actions différées, c'est-à-dire des
                    fonctions programmées pour s'exécuter après un temps
                    d'attente défini
-   email           Module gérant l'envoie d'e-mails depuis le projet
-   format          Module gérant le formatage des messages reçus / à envoyer
-   hook            Module gérant les hooks et évènements
-   interpreteur    Module chargé tout particulièrement d'interpréter les
                    commandes envoyés par les clients
-   joueur          Module contenant les informations sur les joueurs
                    (personnages connectés)
-   objet           Module chargé des objets et des prototypes d'objets
-   meteo           Module gérant la météorologie
-   perso           Module gérant les personnages, connectés (joueurs) ou non
                    (PNJ)
-   pnj             Module gérant les personnages non joueurs
-   salle           Module gérant les salles du MUD
-   scripting       Module gérant le scripting
-   supenr          Superviseur de l'enregistrement des objets dans des
                    fichiers sérialisés
-   temps           Module gérant le temps, non pas la météo, mais le temporel
                    (
                    (années, saisons, mois, jours, heures...)

"""
