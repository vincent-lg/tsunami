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


"""Package contenant la commande 'dire'.

"""

from primaires.interpreteur.commande.commande import Commande
from primaires.format.fonctions import echapper_accolades

class CmdDire(Commande):
    
    """Commande 'dire'.
    
    """
    
    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "dire", "say")
        self.nom_categorie = "parler"
        self.schema = "<message>"
        self.aide_courte = "dit une phrase dans la votre salle"
        self.aide_longue = \
            "Cette commande permet de dire une phrase dans la salle " \
            "où vous vous trouvez. Tous les personnages présents dans " \
            "la salle l'entendront. C'est la commande standard pour " \
            "discuter RP dans l'univers. Elle prend simplement en " \
            "paramètre le message que vous souhaitez dire."
    
    def interpreter(self, personnage, dic_masques):
        """Interprétation de la commande"""
        message = dic_masques["message"].message
        message = echapper_accolades(message)
        salle = personnage.salle
        moi = "Vous dites : " + message
        autre = "{} dit : " + message
        personnage.envoyer(moi)
        salle.envoyer(autre, personnage)
        
        # Appel de l'évènement 'dire' de la salle
        salle.script["dire"].executer(personnage=personnage,
                salle=salle, message=message)
