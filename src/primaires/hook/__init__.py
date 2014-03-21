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


"""Fichier contenant le module primaire hook."""

from abstraits.module import *
from .hook import Hook

class Module(BaseModule):

    """Cette classe contient les informations du module primaire hook.

    Ce module permet de gérer des hooks, c'est-à-dire des évènements
    qui sont appelés dans certains cas précis. Chaque module peut
    définir des hooks qui lui sont propres et chaque module peut
    utiliser ses hooks pour définir certains callback à appeler.

    Note : ne confondez pas actions différées et hooks. Les hooks sont
    des évènements appelés dans certaines circonstances (quand un joueur
    se connecte, par exemple). Les actions différées permettent
    d'appeler des fonctions après un certain temps.

    Un exemple pratique d'hook serait d'avertir le joueur si des messages
    (mudmails) non lus se trouvent dans sa boîte de réception.

    Pour ajouter un nouvel hook, utilisez la méthode ajouter_hook du module.
    Pour lier un hook existant avec un certain évènement, récupérez le
    hook (importeur.hooks[nom_du_hook) et utilisez sa méthode
    ajouter_evenement.

    Pour plus d'informations, regardez l'aide de ces deux méthodes.

    """

    def __init__(self, importeur):
        """Constructeur du module"""
        BaseModule.__init__(self, importeur, "hook", "primaire")
        self.__hooks = {}
        self.logger = type(self.importeur).man_logs.creer_logger("hook",
                "appels")

    def __getitem__(self, nom_hook):
        return self.__hooks[nom_hook]

    @property
    def hooks(self):
        """Retourne un dictionnaire déréférencé des hooks."""
        return dict(self.__hooks)

    def ajouter_hook(self, nom, aide):
        """Ajoute l'hook au dictionnaire des hooks.

        Par défaut, l'hook ajouté ne possède aucun évènement.
        Pour ajouter un évènement à cet hook, il faut appeler
        (sur l'objet hook) la méthode ajouter_evenement.

        Par exemple, le module joueur veut ajouter un hook appelé quand
        un joueur se connecte. Dans la méthode config du module joueur,
        on trouvera :
        |   self.importeur.hook.ajouter_hook("joueur:connecte",
        |           "Hook appelé quand un joueur se connecte")

        Le paramètre aide est utile surtout pour l'introspection.

        Dans le module communication qui veut avertir un joueur qui
        se connecte si il a un message, on trouvera :
        |   hook = self.importeur.hook["joueur:connecte"]
        |   hook.ajouter_evenement(methode)

        Notez que les hook doivent être appelés au moment opportun, ce
        module ne le gère pas. Regardez du côté de la méthode executer
        de l'objet Hook.

        NOTE : on ne peut supprimer d'hook dynamiquement.

        """
        if nom in self.__hooks:
            raise ValueError("le nom d'hook {} est déjà utilisé".format(nom))

        hook = Hook(nom, aide)
        self.__hooks[nom] = hook
