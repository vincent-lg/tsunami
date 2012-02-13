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


"""Fichier contenant le paramètre 'vitesse' de la commande 'rames'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmVitesse(Parametre):
    
    """Commande 'rames vitesse'.
    
    """
    
    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "vitesse", "speed")
        self.schema = "<vitesse_rames>"
        self.aide_courte = "change la vitesse des rames"
        self.aide_longue = \
            "Cette commande permet de modifier la vitesse des rames " \
            "que vous tenez en main. Les vitesses disponibles sont " \
            "|cmd|arrière|ff| (pour aller en marche arrière), " \
            "|cmd|immobile|ff| (vous n'avancez plus), |cmd|lente|ff|, " \
            "|cmd|moyenne|ff| ou |cmd|rapide|ff|. Chaque vitesse " \
            "consomme plus ou moins d'endurance, ainsi, la vitesse " \
            "rapide est plus fatigante que la vitesse lente."
    
    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        salle = personnage.salle
        if not hasattr(salle, "navire") or salle.navire is None or \
                salle.navire.etendue is None:
            personnage << "|err|Vous n'êtes pas sur un navire.|ff|"
            return
        
        navire = salle.navire
        rames = salle.rames
        if not rames:
            personnage << "|err|Il n'y a pas de rames ici.|ff|"
            return
        
        if rames.tenu is not personnage:
            personnage << "|err|Vous ne tenez pas ces rames.|ff|"
        else:
            vitesse = rames.vitesse
            n_vitesse = dic_masques["vitesse_rames"].vitesse
            if vitesse == n_vitesse:
                personnage << "|err|Vous ramez déjà à cette vitesse.|ff|"
                return
            
            rames.vitesse = n_vitesse
            msg = "Vous commencez de ramer {vitesse}."
            msg_autre = "{{personnage}} commence à ramer {vitesse}."
            msg_vit = ""
            if n_vitesse == "arrière":
                msg_vit = "en marche arrière"
            elif n_vitesse == "immobile":
                msg = "Vous arrêtez de ramer."
                msg_autre = "{{personnage}} arrête de ramer."
            elif n_vitesse == "lente":
                msg_vit = "à faible vitesse"
            elif n_vitesse == "moyenne":
                msg_vit = "à vitesse moyenne"
            elif n_vitesse == "rapide":
                msg_vit = "rapidement"
            else:
                raise RuntimeError("vitesse non traitée {}".format(n_vitesse))
            
            msg = msg.format(vitesse=msg_vit)
            msg_autre = msg_autre.format(vitesse=msg_vit)
            personnage << msg
            salle.envoyer(msg_autre, personnage)
