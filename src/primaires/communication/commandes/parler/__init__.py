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


"""Package contenant la commande 'parler'.

"""

from primaires.interpreteur.commande.commande import Commande

class CmdParler(Commande):
    
    """Commande 'parler'.
    
    """
    
    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "parler", "tell")
        self.nom_categorie = "parler"
        self.schema = "<nom_joueur> <message>"
        self.aide_courte = "dit une phrase à un autre joueur"
        self.aide_longue = \
            "Cette commande permet de parler à un autre joueur connecté dans " \
            "l'univers. Ce que vous dites par ce moyen n'est pas soumis aux " \
            "règles du RP. La commande prend en paramètres le nom du joueur, " \
            "et ce que vous souhaitez dire."
    
    def interpreter(self, personnage, dic_masques):
        """Interprétation de la commande"""
        cible = dic_masques["nom_joueur"].joueur
        message = dic_masques["message"].message
        if cible is personnage:
            personnage << "Vous parlez tout seul... Hum."
        else:
            clr = type(self).importeur.anaconf. \
                    get_config("config_com").couleur_tell
            personnage << clr + "Vous dites à {} : {}|ff|".format(cible.nom,
                    message)
            cible << clr + "{} vous dit : {}|ff|".format(personnage.nom,
                    message)
            type(self).importeur.communication.conversations. \
                    ajouter_ou_remplacer(cible, personnage, message)
