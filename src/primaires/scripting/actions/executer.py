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


"""Fichier contenant l'action executer."""

from primaires.connex.instance_connexion import InstanceConnexion
from primaires.joueur.contextes.connexion.mode_connecte import ModeConnecte
from primaires.scripting.action import Action
from primaires.scripting.instruction import ErreurExecution

class ClasseAction(Action):

    """Force le personnage à exécuter une commande.

    Soyez prudent avec cette action : elle force un personnage à
    exécuter une commande, ce qui semble une bonne solution dans de
    nombreux cas. Les commandes ne sont cependant pas optimisées.
    L'interprétation des arguments rajoute du temps à l'exécution.
    Mieux vaut passer par d'autres actions ou fonctions tant que
    cela est possible.

    """

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.cmd_executer, "Personnage", "str")

    @staticmethod
    def cmd_executer(personnage, commande):
        """Force un personnage à executer une commande.

        Essayez de ne pas utiliser cette action régulièrement,
        surtout dans des scripts qui s'exécutent d'eux-mêmes (les
        ticks, les changements de temps). L'exécution d'une commande
        par scripting n'est pas un processus optimisé et peut être
        lente. Il faut trouver la commande et interpréter ses
        paramètres. Préférez utiliser d'autres actions et fonctions
        tant que cela est possible.

        Paramètres à préciser :

          * personnage : le personnage devant exécuter la commande
          * commande : la commande à exécuter (une chaîne).

        Exeples d'utilisation :

          # Force le personnage à exécuter la commande 'pêcher'
          executer personnage "pêcher"
          # Force le personnage à dire quelque chose
          executer personnage "dire Coucou !"

        """
        instance = InstanceConnexion(None, False)
        instance.joueur = personnage
        mode_connecte = ModeConnecte(instance)
        mode_connecte.interpreter(commande)
