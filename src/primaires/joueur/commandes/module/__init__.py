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


"""Package contenant la commande 'module' et ses sous-commandes.
Dans ce fichier se trouve la commande même.

"""

from primaires.interpreteur.commande.commande import Commande
from primaires.joueur.commandes.module.liste import PrmListe
from primaires.joueur.commandes.module.hotboot import PrmHotboot

class CmdModule(Commande):
    
    """Commande 'module'.
    
    """
    
    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "module", "module")
        self.groupe = "administrateur"
        self.aide_courte = "manipulation des modules"
        self.aide_longue = \
            "Cette commande permet de manipuler les modules, connaître la " \
            "liste des modules chargés, en redémarrer certains ou les " \
            "reconfigurer pendant l'exécution. Cette commande doit être " \
            "réservée aux administrateurs, ceux ayant un accès aux fichiers " \
            "de configuration ou au code."
        
        # On prépare les différents paramètres de la commande
        prm_liste = PrmListe()
        prm_hotboot = PrmHotboot()
        
        self.ajouter_parametre(prm_liste)
        self.ajouter_parametre(prm_hotboot)
