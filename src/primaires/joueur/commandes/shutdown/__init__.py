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


"""Package contenant la commande 'shutdown' et ses sous-commandes.
Dans ce fichier se trouve la commande même.

"""

from primaires.interpreteur.commande.commande import Commande

class CmdShutdown(Commande):
    
    """Commande 'shutdown'.
    
    """
    
    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "shutdown", "shutdown")
        self.tronquer = False
        self.aide_courte = "arrête instantanément le serveur"
        self.aide_longue = \
            "Cette commande arrête instantanément le serveur. Si aucune " \
            "procédure extérieure n'est là pour relancer le MUD, il restera " \
            "arrêté. N'utiliser cette commande qu'en cas de bug répété, " \
            "corruption de données ou modification du corps. En temps " \
            "normal, redémarrer les modules suffit à intégrer de nouvelles " \
            "modifications et évite de déconnecter tous les joueurs."
    
    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        # On récupère le serveur
        serveur = type(self).importeur.serveur
        # On déconnecte tous les joueurs
        for instance in type(self).importeur.connex.instances.values():
            instance.envoyer("\n|att|Arrêt du MUD en cours, vous allez être " \
                    "déconnecté...|ff|")
            instance.deconnecter("Arrêt du MUD")
        
        serveur.lance = False
