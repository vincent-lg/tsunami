# -*-coding:Utf-8 -*

# Copyright (c) 2010 LE GOFF Vincent
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# * Redistributions of source code must retain the above copyright notice, this
#   raise of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this raise of conditions and the following disclaimer in the documentation
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


"""Fichier contenant le paramètre 'empanner' de la commande 'voile'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmEmpanner(Parametre):
    
    """Commande 'voile empanner'.
    
    """
    
    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "empanner", "jibe")
        self.aide_courte = "empanne la voile présente"
        self.aide_longue = \
            "Cette commande permet d'empanner la voile dans la salle où " \
            "vous vous trouvez. Empanner permet de changer d'amure. " \
            "Ainsi aucun paramètre n'est nécessaire : si la voile est " \
            "bâbord amure, cette commande la fera passée tribord amure. " \
            "Notez cependant que la voile doit être bordée au possible " \
            "avant l'empannage (inutile d'empanner une voile qui est " \
            "complètement choquée)."
    
    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        salle = personnage.salle
        if not hasattr(salle, "voiles"):
            personnage << "|err|Vous n'êtes pas sur un navire.|ff|"
            return
        
        voiles = salle.voiles
        if not voiles:
            personnage << "|err|Vous ne voyez aucune voile ici.|ff|"
            return
        
        voile = voiles[0]
        if not voile.hissee:
            personnage << "|err|Cette voile n'est pas hissée.|ff|"
        else:
            if voile.orientation < -10 or voile.orientation > 10:
                personnage << "|err|Cette voile n'est pas assez bordée.|ff|"
                return
            
            voile.orientation = -voile.orientation
            salle.enregistrer()
            personnage << "Vous empannez {}.".format(voile.nom)
            personnage.salle.envoyer("{{}} empanne {}.".format(
                    voile.nom), personnage)
