# -*-coding:Utf-8 -*

# Copyright (c) 2012 LE GOFF Vincent
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


"""Package contenant la commande 'alias' et ses sous-commandes.

Dans ce fichier se trouve la commande même.

"""

from primaires.interpreteur.commande.commande import Commande
from .ajouter import PrmAjouter
from .liste import PrmListe
from .supprimer import PrmSupprimer

class CmdAlias(Commande):
    
    """Commande 'alias'.
    
    """
    
    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "alias", "alias")
        self.groupe = "joueur"
        self.aide_courte = "manipulation des aliass"
        self.aide_longue = \
            "Cette commande vous permet de manipuler vos alias. " \
            "Les alias sont des raccourcis pour des commandes. Si " \
            "vous définissez par exemple un alias |cmd|l|ff| qui a pour " \
            "valeur |cmd|look|ff|, quand vous entrerez |cmd|l|ff| " \
            "le système traduira cette commande en |cmd|look|ff|. " \
            "Et si vous entrez |cmd|l quelque chose|ff|, le système " \
            "traduira ça en |cmd|look quelque chose|ff|. Des alias " \
            "prédéfinis ont été paramétrés pour votre joueur. Vous " \
            "pouvez les éditer, en ajouter d'autre, les supprimer. Notez " \
            "qu'ils sont différents en fonction de la langue des " \
            "commandes que vous choisissez."
    
    def ajouter_parametres(self):
        """Ajout des paramètres"""
        prm_ajouter = PrmAjouter()
        prm_liste = PrmListe()
        prm_supprimer = PrmSupprimer()
        
        self.ajouter_parametre(prm_ajouter)
        self.ajouter_parametre(prm_liste)
        self.ajouter_parametre(prm_supprimer)
