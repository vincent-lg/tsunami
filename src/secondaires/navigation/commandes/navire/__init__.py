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


"""Package contenant la commande 'navire' et ses sous-commandes.

Dans ce fichier se trouve la commande même.

"""

from primaires.interpreteur.commande.commande import Commande
from .creer import PrmCreer
from .detruire import PrmDetruire
from .direction import PrmDirection
from .editer import PrmEditer
from .etendue import PrmEtendue
from .info import PrmInfo
from .liste import PrmListe
from .matelot import PrmMatelot
from .nom import PrmNom
from .proprietaire import PrmProprietaire
from .teleporter import PrmTeleporter
from .zero import PrmZero

class CmdNavire(Commande):

    """Commande 'navire'.

    """

    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "navire", "ship")
        self.groupe = "administrateur"
        self.aide_courte = "manipulation des navires"
        self.aide_longue = \
            "Cette commande permet de manipuler les navires, connaître " \
            "la liste des navires et modèles existants, créer des " \
            "navires, les téléporter, changer leur orientation, " \
            "leur vitesse, les forcer à avancer..."

    def ajouter_parametres(self):
        """Ajout des paramètres"""
        prm_creer = PrmCreer()
        prm_detruire = PrmDetruire()
        prm_direction = PrmDirection()
        prm_etendue = PrmEtendue()
        prm_info = PrmInfo()
        prm_liste = PrmListe()
        prm_teleporter = PrmTeleporter()

        self.ajouter_parametre(prm_creer)
        self.ajouter_parametre(prm_detruire)
        self.ajouter_parametre(prm_direction)
        self.ajouter_parametre(PrmEditer())
        self.ajouter_parametre(prm_etendue)
        self.ajouter_parametre(prm_info)
        self.ajouter_parametre(prm_liste)
        self.ajouter_parametre(PrmMatelot())
        self.ajouter_parametre(PrmNom())
        self.ajouter_parametre(PrmProprietaire())
        self.ajouter_parametre(prm_teleporter)
        self.ajouter_parametre(PrmZero())
