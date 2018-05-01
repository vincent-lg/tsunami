# -*-coding:Utf-8 -*

# Copyright (c) 2010-2017 LE GOFF Vincent
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


"""Package contenant le paramètre 'détruire' de la commande 'neige'."""

from primaires.interpreteur.masque.parametre import Parametre
from primaires.perso.exceptions.stat import DepassementStat
from primaires.salle.bonhomme_neige import BonhommeNeige

class PrmDetruire(Parametre):
    
    """Commande 'neige détruire'"""
    
    def __init__(self):
        """Constructeur du paramètre."""
        Parametre.__init__(self, "détruire", "destroy")
        self.schema = "<element_observable>"
        self.aide_courte = "détruit votre bonhomme de neige"
        self.aide_longue = \
            "Cette commande permet de détruire un bonhomme de neige dont " \
            "vous êtes le créateur. Vous ne pouvez utiliser cette commande " \
            "pour détruire les bonhommes des autres."
    
    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        elt = dic_masques["element_observable"].element
        salle = personnage.salle
        personnage.agir("neige")
        
        # Vérifie qu'il s'agit bien d'un bonhomme de neige
        if not isinstance(elt, BonhommeNeige):
            personnage << "|err|Ceci n'est pas un bonhomme de neige.|ff|"
            return
        
        bonhomme = elt
        if bonhomme.createur is not personnage:
            personnage << "|err|Ce bonhomme de neige n'est pas à vous.|ff|"
            return
        
        if personnage.nb_mains_libres < 2:
            personnage << "|err|Il vous faut au moins deux mains " \
                    "de libre.|ff|"
            return
        
        try:
            personnage.stats.endurance -= 15
        except DepassementStat:
            personnage << "|err|Vous êtes trop fatigué.|ff|"
        else:
            for objet in bonhomme.elements.values():
                salle.objets_sol.ajouter(objet)
            
            personnage << "Vous démentelez {}.".format(bonhomme.get_nom())
            salle.envoyer("{{}} démentèle {}.".format(bonhomme.get_nom()), personnage)
            salle.decors.remove(bonhomme)
            bonhomme.detruire()
