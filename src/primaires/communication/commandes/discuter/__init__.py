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


"""Package contenant la commande 'discuter'.

"""

from primaires.interpreteur.commande.commande import Commande
from primaires.format.fonctions import echapper_accolades

class CmdDiscuter(Commande):
    
    """Commande 'discuter'.
    
    """
    
    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "discuter", "talk")
        self.nom_categorie = "parler"
        self.schema = "<nom_pnj> (de/about <message>)"
        self.aide_courte = "engage une discussion avec un PNJ"
        self.aide_longue = \
            "Cette commande engage une discussion avec un PNJ présent dans " \
            "la salle à propos d'un sujet quelconque. Il est tout à fait " \
            "possible qu'un PNJ ne réagisse pas à un sujet donné, et rien " \
            "ne peut vous l'indiquer a priori."
    
    def interpreter(self, personnage, dic_masques):
        """Interprétation de la commande"""
        if dic_masques["message"] is None:
            message = ""
            ret = "Vous engagez la discussion avec {}."
        else:
            message = dic_masques["message"].message
            ret = "Vous engagez la discussion avec {} à propos de \"{}\"."
        pnj = dic_masques["nom_pnj"].pnj
        personnage << ret.format(pnj.get_nom_pour(personnage), message)
        
        # Appel de l'évènement 'discute' du PNJ
        pnj.script["discute"].executer(sujet=message, personnage=personnage,
                pnj=pnj)
