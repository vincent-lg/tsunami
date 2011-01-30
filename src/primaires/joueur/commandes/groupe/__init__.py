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


"""Package contenant la commande 'groupe' et ses sous-commandes.
Dans ce fichier se trouve la commande même.

"""

from primaires.interpreteur.commande.commande import Commande
from primaires.joueur.commandes.groupe.ajouter import PrmAjouter
from primaires.joueur.commandes.groupe.inclus import PrmInclus
from primaires.joueur.commandes.groupe.info import PrmInfo
from primaires.joueur.commandes.groupe.liste import PrmListe
from primaires.joueur.commandes.groupe.supprimer import PrmSupprimer

class CmdGroupe(Commande):
    
    """Commande 'groupe'.
    
    """
    
    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "groupe", "group")
        self.groupe = "administrateur"
        self.aide_courte = "manipulation des groupes d'utilisateur"
        self.aide_longue = \
            "Cette commande permet de manipuler les groupes " \
            "d'utilisateur. Ces groupes caractérisent un certain nombre " \
            "de flags communs à des catégories de joueurs mais surtout " \
            "définit les commandes utilisables par chacun. En plus des " \
            "groupes |tit|npc|ff|, |tit|joueur|ff| (par défaut) et " \
            "|tit|administrateur|ff|, vous pouvez créer l'architecture " \
            "des groupes que vous voulez grâce à cette commande. Cela " \
            "vous permet de créer simplement la hiérarchie des " \
            "administrateurs / joueurs que vous désirez. Regardez le détail " \
            "des sous-commandes pour plus d'informations."
    
    def ajouter_parametres(self):
        """Ajout des paramètres"""
        prm_ajouter = PrmAjouter()
        prm_inclus = PrmInclus()
        prm_info = PrmInfo()
        prm_liste = PrmListe()
        prm_supprimer = PrmSupprimer()
        
        self.ajouter_parametre(prm_ajouter)
        self.ajouter_parametre(prm_inclus)
        self.ajouter_parametre(prm_info)
        self.ajouter_parametre(prm_liste)
        self.ajouter_parametre(prm_supprimer)
