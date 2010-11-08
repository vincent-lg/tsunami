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


"""Ce fichier est à la racine du package 'contexte', définissant plusieurs
types de contexte, chacun avec son paquet propre.

Ce fichier définit aussi la classe Contexte, classe-mère de tous les contextes
développés dans ce package.

"""

class Contexte:
    """Classe abstraite définissant un contexte.
    Si vous voulez utiliser un contexte :
    *   Choisissez-le dans les classes-filles de Contexte
    *   Créez une nouvelle sous-classe de Contexte correspondant mieux à vos
        attentes
    
    Cette classe est abstraite. Aucun objet ne doit être créé directement
    depuis cette classe. L'architecture de chaque contexte est à la charge du
    paquet concerné. Consultez la documentation de la classe avant de l'utiliser
    comme contexte.
    
    Les contextes sont des formes d'interpréteur destinés à remplir
    une mission bien précise. Ces contextes sont souvent chaînés.
    
    Par exemple, le contexte chargé de demander son nom à l'utilisateur
    va avoir plusieurs sorties possibles :
    *   Si le joueur entre un nom valide :
        *   Si le nom existe, on charge le personnage lié à ce nom
            et on redirige le joueur sur le contexte 'entrer le mot de passe'
        *   Si le nom n'existe pas, on redirige vers le contexte chargé
            de la création de personnage
    *   Si le nom est invalide, on demande au joueur de l'entrer à nouveau
        Autrement dit, on lui affiche un message d'erreur et on le redirige sur
        le même contexte.
    
    Il s'agit d'un exemple simple, mais des contextes peuvent être plus
    complexes, notamment les éditeurs. En fonction de la récurrence d'un
    contexte, des objets hérités devront être créés avec un certain nombre de
    comportements par défaut déjà programmés.
    
    Pour plus d'informations, visiter les sous-paquets.

    """

    importeur = None
    
    def __init__(self, nom):
        """Constructeur d'un contexte."""
        pass
    
    def accueil(self, emt):
        """Retourne un message d'accueil à l'émetteur.
        Ce message est envoyé à chaque fois que le joueur arrive dans ce
        contexte.
        
        """
        return ""
    
    def interpreter(self, emt, msg):
        """Méthode appelée quand le contexte reçoit un message à interpréter.
            emt - l'émetteur du message
            msg - le message sous la forme d'une chaîne
        
        """
        pass
