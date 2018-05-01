# -*-coding:Utf-8 -*

# Copyright (c) 2010-2017 NOEL-BARON Léo
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


"""Package contenant la commande 'quete'"""

from primaires.interpreteur.commande.commande import Commande

class CmdQuete(Commande):
    
    """Commande 'quete'.
    
    """
    
    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "quete", "quest")
        self.groupe = "joueur"
        self.schema = ""
        self.aide_courte = "récapitule vos quêtes"
        self.aide_longue = \
            "Cette commande récapitule l'état actuel de vos quêtes, en " \
            "cours ou terminées."
    
    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        a_faire = personnage.quetes.etapes_a_faire
        faites = personnage.quetes.etapes_accomplies
        ret = ""
        if not faites and not a_faire:
            personnage << "Vous n'avez encore aucune quête en cours ou accomplie."
            return
        
        if a_faire:
            ret += "|tit|Vos quêtes en cours :|ff|"
            # On parcourt les quêtes en cours / terminees
            for quete, etapes in a_faire.items():
                ret += "\n|cy|" + quete.titre[0].upper() + quete.titre[1:] + "|ff|"
                for etape in etapes:
                    ret += "\n - " + etape.titre
        
        if faites:
            if a_faire:
                ret += "\n\n"
            
            ret += "|tit|Vos quêtes accomplies :|ff|"
            for quete, etapes in faites.items():
                ret += "\n" + quete.titre[0].upper() + quete.titre[1:]
                if len(etapes) == 1 and (quete.ordonnee or quete is etapes[0]):
                    continue
                
                for etape in etapes:
                    ret += "\n - " + etape.titre
            
        personnage << ret
