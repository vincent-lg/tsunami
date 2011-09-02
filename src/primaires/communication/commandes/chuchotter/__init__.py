# -*-coding:Utf-8 -*

# Copyright (c) 2011 EILERS Christoff
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


"""Package contenant la commande 'chuchotter'.

"""

from primaires.interpreteur.commande.commande import Commande
from random import randint
from math import ceil

class CmdChuchotter(Commande):
    
    """Commande 'chuchotter'.
    
    """
    
    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "chuchotter", "whisper")
        self.nom_categorie = "chuchotter"
        self.schema = "<nom_joueur> <message>"
        self.aide_courte = "chuchotte une phrase à un autre joueur"
        self.aide_longue = \
            "Cette commande permet de parler à un autre joueur ou à un bot présent dans " \
            "la même salle. Ce que vous dites par ce moyen est soumis aux " \
            "règles du RP. La commande prend en paramètres la cible de votre chuchottement (bot ou joueur), " \
                "et ce que vous souhaitez lui chuchotter."
    
    def interpreter(self, personnage, dic_masques):
        """Interprétation de la commande"""
        cible = dic_masques["nom_joueur"].joueur
        message = dic_masques["message"].message
        if not personnage.salle is cible.salle:
            personnage << "|err|Cette personne n'est pas avec vous.|ff|"
        else:
            # FIXME ajouter une couleur spécifique pour le whisper ?
            personnage << "Vous chuchottez à {} : {}".format(cible.nom, message)
            cible << "{} vous chuchotte : {}".format(personnage.nom, message)
            moyenne_sens = ceil((personnage.sensibilite + cible.sensibilite) / 2)
            for perso in personnage.salle.personnages:
                if perso != personnage and perso != cible:
                    # FIXME il faut faire quelque chose pour les pnj, pour l'instant on ne chuchotte qu'aux joueurs à cause du masque
                    # On vérifie si la personne a plus de sens que la moyenne des deux autres. Si c'est le cas, un random détermine pour chaque mot si elle l'entend. Sinon, un random beaucoup plus petit joue le même rôle. Ma phrase est mal construite, et je vous zute. =)
                    if perso.sensibilite > moyenne_sens:
                        random_entendre = 5 # une chance sur deux
                    else:
                        random_entendre = 2 # une sur cinq
                    phrase = ""
                    i = 0 # désolé j'ai encore du mal à trouver une autre syntaxe, Python est nouveau pour moi :S
                    message_split = message.split()
                    longueur_message = len(message_split)
                    for mot in message_split:
                        if not mot in "?!;:":
                            if randint(1, random_entendre) <= random_entendre:
                                phrase += mot
                            else:
                                phrase += "..."
                        else:
                            phrase += mot
                        if i > 0 and i < longueur_message:
                            phrase += " "
                        i += 1
                    perso << "{} chuchotte quelque chose à {}. Vous parvenez à entendre : {}".format(personnage.nom, cible.nom, phrase)