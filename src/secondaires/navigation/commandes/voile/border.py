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


"""Fichier contenant le paramètre 'border' de la commande 'voile'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmBorder(Parametre):
    
    """Commande 'voile border'.
    
    """
    
    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "border", "haul")
        self.schema = "<nombre>"
        self.aide_courte = "borde la voile présente"
        self.aide_longue = \
            "Cette commande permet de border la voile dans la salle où " \
            "vous vous trouvez. Plus la voile est bordée, plus elle " \
            "est parallèle à l'âxe du navire. La voile doit être plus " \
            "ou moins bordée selon l'allure du navire. Si vous voulez " \
            "changer d'amure, utilisez la commande %voile% %voile:empanner%."
    
    def ajouter(self):
        """Méthode appelée lors de l'ajout de la commande à l'interpréteur"""
        nombre = self.noeud.get_masque("nombre")
        nombre.proprietes["limite_sup"] = "90"
    
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
            nombre = dic_masques["nombre"].nombre
            if voile.orientation < 0:
                voile.orientation += nombre
                if voile.orientation > -5:
                    voile.orientation = -5
                personnage << "Vous bordez {}.".format(voile.nom)
                personnage.salle.envoyer("{{}} borde {}.".format(
                        voile.nom), personnage)
            elif voile.orientation > 0:
                voile.orientation -= nombre
                if voile.orientation < 5:
                    voile.orientation = 5
                personnage << "Vous bordez {}.".format(voile.nom)
                personnage.salle.envoyer("{{}} borde {}.".format(
                        voile.nom), personnage)
            else:
                personnage << "|err|Cette voile ne peut être bordée " \
                        "davantage.|ff|"
