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


"""Fichier contenant la classe Diffact définissant le module primaire
du même nom.

"""

from abstraits.module import *
from primaires.diffact.action_differee import ActionDifferee

class Diffact(Module):
    """Cette classe contient les informations du module primaire diffact.
    Ce module permet de gérer des actions différés.
    Typiquement, quand un module primaire ou secondaire doit se mettre en pause
    pendant un certain temps, il ne peut pas paralyser la boucle synchro
    du projet. La solution la plus simple est de créer une action différée
    qui s'exécutera dans un temps fixé à l'avance.
    
    Exemples :
    -   si une commande doit faire une pause pendant 3 secondes, au moment
        de la pause, la commande s'arrête et créée une action différée
        qui devra s'exécuter dans 3 secondes. Il sera nécessaire de dédier
        l'exécution de cette action à une fonction ou méthode, en lui précisant
        un certain nombre de paramètres
    -   si un module primaire doit contrôler toutes les 60 secondes une
        information quelconque, il peut créer dès son initialisation
        une action différée. La méthode qui sera exécutée par l'action en
        question devra recréer une action différée devant s'exécuter 60
        secondes plus tard.
    
    Concrètement, une action différée possède une référence vers
    une fonction ou méthode, et une liste de paramètres. Un temps d'échéance,
    précisé sous la forme d'un timestamp, permet de savoir quand appeler
    cette action. Dans la boucle synchro du projet, une méthode de
    module devra vérifier qu'aucune action différée n'a atteint le temps
    d'échéance. Si une action est arrivée à son terme, on exécute la fonction
    en lui passant ses paramètres. On la supprime bien entendu de la liste
    des actions en attente.
    
    Les actions différées étant contrôlées à chaque tour de boucle synchro,
    il faut prévoir un retard d'exécution maximum à peu près équivalent au
    temps moyen du Watch Dog.
    
    """
    def __init__(self, importeur, parser_cmd):
        """Constructeur du module"""
        Module.__init__(self, importeur, parser_cmd, "diffact", "primaire")
        self.actions = {} # {nom_action:action_differee}
        self.logger = None
    
    def config(self):
        """Redéfinition de la configuration du module.
        On créée un logger portant le nom du module.
        
        """
        self.logger = self.importeur.log.creer_logger("diffact", "diffact")
        Module.config(self)

    def boucle(self):
        """Redéfinition de la méthode boucle du Module.
        Cette méthode est appelée pour chaque module, à chaque tour de boucle
        temps réel.
        
        """
        self.mettre_a_jour_actions()
    
    def ajouter_action(self, nom_action, tps, ref_fonc, *args, **kwargs):
        """Cette méthode permet d'ajouter une action différée à la liste
        de celles en attente. On précise :
        -   le nom de l'action (nom unique, servant d'identifiant)
        -   le temps d'attente avant exécution en secondes
        -   la référence vers la fonction ou la méthode à exécuter
        -   les paramètres non nommés organisés en tuple
        -   les paramètres nommés organisés dans un dictionnaire
        
        """
        if nom_action in self.actions.keys():
            self.logger.warning("l'action différée {0} existe déjà. " \
                    "L'ancienne sera écrasée".format(nom_action))
        action = ActionDifferee(nom_action, tps, ref_fonc, *args, **kwargs)
        self.actions[nom_action] = action
        self.logger.debug("Ajout de l'action {0} exécutée dans {1}s".format( \
                nom_action, tps))
    
    def retirer_action(self, nom):
        """Méthode permettant de retirer une action différée de la liste de
       celles en attente.
        
        """
        if not nom in self.actions.keys():
            self.logger.warning("L'action différée {0} devant être " \
                    "supprimée n'existe pas".format(nom))
        else:
            del self.actions[nom]
            self.logger.debug("L'action {0} a bien été supprimée".format(nom))

    def mettre_a_jour_actions(self):
        """Cette méthode se charge de mettre à jour les actions différées en
        attente d'être exécutées. Elle parcourt la liste des actions en
        attente et exécute celle qui doivent l'être, tout en les supprimant
        de la liste.
        
        """
        for nom,action in tuple(self.actions.items()):
            if action.doit_exec():
                # On la supprime avant toute chose
                self.retirer_action(nom)
                # On l'exécute ensuite
                action.executer()
