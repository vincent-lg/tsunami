# -*-coding:Utf-8 -*

# Copyright (c) 2011 LE GOFF Vincent
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


"""Ce fichier définit la classe Etat, détaillée plus bas."""

from corps.fonctions import valider_cle
from primaires.perso.exceptions.action import ExceptionAction

class Etat:

    """Classe représentant un état d'un personnage.

    L'état est une classe générique représentant un état d'un personnage.
    Un état est l'état actif du personnage (est en train de combattre,
    est en train de chercher du bois, est en train de pêcher...).

    L'état autorise ou interdit certaines actions identifiées simplement
    par leur clé.
    Par exemple, l'état "combat" (est en combat) interdit qu'on ramasse
    un objet.

    Si un personnage change d'état, on manipule son attribut 'cle_etat'.
    On ne crée pas un nouvel état pour lui. L'état reste, en somme,
    le même d'un personnage à l'autre.

    En terme d'objet, si un personnage entre en combat contre
    un autre personnage, ils partagent le même état.
    L'état ne peut donc pas contenir d'informations propres à un personnage.

    Pour notifier qu'un personnage effectue une action dans une commande,
    on appelle la méthode 'agir' du personnage en lui passant en paramètre
    la clé de l'action.
    >>> personnage.agir("ramasser")
    Si l'état dans lequel se trouve le personnage n'autorise pas à ramasser,
    une exception interceptée est levée, interrompant l'exécution
    de la commande et envoyant un message de refus au joueur
    (vous êtes en train de combattre).

    NOTE : Si seul le dictionnaire des actions interdites est renseigné,
    toutes les actions non interdites sont, par défaut, autorisées. Si seul
    le dictionnaire des actions autorisées est renseigné, toutes les actions
    non autorisées sont interdites. Si les deux sont vides, toutes les actions
    sont interdites.

    """

    cle = None
    msg_refus = "Non précisé."
    msg_visible = "fait quelque chose"
    act_autorisees = []
    act_interdites = []
    peut_etre_attaque = True
    sauvegarder_au_reboot = False

    def __init__(self, personnage):
        """Constructeur d'un état."""
        self.personnage = personnage

    @property
    def arguments(self):
        return (self.cle, )

    def peut_faire(self, cle_action):
        """Si ne peut pas faire l'action, lève une exception ExceptionEtat.

        Sinon, laisse passer.

        """
        if cle_action in self.act_interdites or (not self.act_interdites \
                and not cle_action in self.act_autorisees):
            raise ExceptionAction(self.msg_refus)

    def message_visible(self):
        """Retourne le message pour les autres."""
        return self.msg_visible

    def get_facteur(self):
        """Retourne le facteur de récupération."""
        return 1
