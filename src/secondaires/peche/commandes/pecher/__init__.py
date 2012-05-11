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


"""Package contenant la commande 'pêcher'."""

from primaires.interpreteur.commande.commande import Commande

class CmdPecher(Commande):
    
    """Commande 'pêcher'"""
    
    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "pêcher", "fish")
        self.aide_courte = "jète une ligne à l'eau"
        self.aide_longue = \
            "Cette commande permet de commencer à pêcher en jetant une " \
            "ligne à l'eau. Elle permet également d'arrêter de pêcher à " \
            "tout moment (entrer %pêcher% pour commencer à pêcher, puis " \
            "%pêcher% pour arrêter). En fonction de l'étendue d'eau " \
            "ou de la salle où vous vous trouvez, vous pêcherez dans " \
            "un banc différent. Avant de commencer à pêcher, vous devez " \
            "disposer d'une canne à pêche et l'appâter (voir ...)."
    
    def interpreter(self, personnage, dic_masques):
        """Interprétation de la commande."""
        salle = personnage.salle
        banc = importeur.peche.get_banc_pour(salle)
        if banc is None:
            personnage << "|err|Vous ne pouvez pêcher ici.|ff|"
            return
        
        if personnage.cle_etat == "pecher":
            personnage.cle_etat = ""
            personnage << "Vous retirez votre ligne de l'eau."
            personnage.salle.envoyer("{} retire sa ligne de l'eau.",
                    personnage)
            return
        
        canne = None
        for membre in personnage.equipement.membres:
            for objet in membre.equipe:
                if objet.est_de_type("canne à pêche"):
                    canne = objet
                    break
        
        if canne is None:
            personnage << "|err|Vous n'équipez pas de canne à pêche.|ff|"
            return
        
        if canne.appat is None:
            personnage << "|err|{} n'est pas appâtée.".format(
                    canne.get_nom().capitalize())
            return
        
        personnage.agir("pecher")
        personnage << "Vous jetez votre ligne à l'eau."
        personnage.salle.envoyer("{} jète sa lègne à l'eau.", personnage)
        personnage.cle_etat = "pecher"
        importeur.diffact.ajouter_action("peche:" + personnage.nom, 15,
                importeur.peche.attendre_pecher, personnage, canne)
