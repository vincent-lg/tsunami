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


"""Package contenant la commande 'dépecer'.

"""

from datetime import datetime

from corps.aleatoire import varier
from primaires.interpreteur.commande.commande import Commande
from primaires.perso.exceptions.stat import DepassementStat

class CmdDepecer(Commande):
    
    """Commande 'dépecer'.
    
    """
    
    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "dépecer", "skin")
        self.schema = "<nom_objet>"
        self.aide_courte = "dépece le cadavre d'un PNJ"
        self.aide_longue = \
            "Cette commande permet de dépecer le cadavre d'un PNJ " \
            "présent sur le sol de la salle où vous vous " \
            "trouvez. Vous pourrez peut-être ainsi récupérer, si " \
            "c'est un animal, de la viande ou de la fourrure, parfois " \
            "les deux."
    
    def ajouter(self):
        """Méthode appelée lors de l'ajout de la commande à l'interpréteur"""
        nom_objet = self.noeud.get_masque("nom_objet")
        nom_objet.proprietes["conteneurs"] = \
                "(personnage.salle.objets_sol.get_objets_par_nom(), )"
        nom_objet.proprietes["quantite"] = "True"
    
    def interpreter(self, personnage, dic_masques):
        """Interprétation de la commande"""
        objet = dic_masques["nom_objet"].objet
        if not objet.est_de_type("cadavre"):
            personnage << "|err|Vous ne pouvez dépecer " + objet.get_nom() + \
                    ".|ff|"
            return
        
        end = 5
        try:
            personnage.stats.endurance -= end
        except DepassementStat:
            personnage << "|err|Vous êtes trop fatigué pour cela.|ff|"
            return
        
        if (datetime.now() - objet.apparition).seconds >= 750:
            personnage << "|err|Ce cadavre est trop abîmé pour être " \
                    "dépecé.|ff|"
            return
        
        armes = personnage.get_armes()
        lame = None
        for arme in armes:
            if arme.peut_depecer:
                lame = arme
                break
        
        if lame is None:
            personnage << "|err|Vous n'équipez rien pouvant dépecer.|ff|"
            return
        
        personnage << "Vous commencez à dépecer " + objet.get_nom() + "."
        personnage.cle_etat = "depece"
        yield 5
        personnage.cle_etat = ""
        connaissance = varier(personnage.pratiquer_talent("depecage") + 1, 5)
        if connaissance < objet.pnj.niveau:
            personnage << "|err|Vous faites un beau gâchi en essayant de " \
                    "dépecer ce cadavre.|ff|"
            personnage.salle.envoyer("{} fait un beau gâchi en tentant de " \
                    "dépecer " + objet.get_nom() + ".", personnage)
            importeur.objet.supprimer_objet(objet.identifiant)
        else:
            importeur.objet.supprimer_objet(objet.identifiant)
            for elt, nb in objet.pnj.a_depecer.items():
                for i in range(nb):
                    o = importeur.objet.creer_objet(elt)
                    personnage.salle.objets_sol.ajouter(o)
            
            personnage << "Vous dépecez " + objet.get_nom() + " avec " + \
                    lame.get_nom() + "."
            personnage.salle.envoyer("{} dépece " + objet.get_nom() + \
                    " avec " + lame.get_nom() + ".", personnage)
            personnage.gagner_xp_rel(objet.pnj.niveau, objet.pnj.gain_xp // 3,
                    "survie")
