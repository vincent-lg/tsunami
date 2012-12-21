# -*-coding:Utf-8 -*

# Copyright (c) 2011 LE GOFF Vincent
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


"""Fichier contenant la classe Attaque, détaillée plus bas.

Il contient également les autres classes héritées d'Attaque :
    Attaque
    Coup

"""

from random import randint

from abstraits.obase import BaseObj
from corps.aleatoire import *

class Attaque(BaseObj):
    
    """Classe représentant une attaque."""
    
    def __init__(self, personnage, cle):
        """Constructeur de l'attaque."""
        BaseObj.__init__(self)
        self.personnage = personnage
        self.cle = cle
        self.probabilite = 100
        self.degats_min = 10
        self.degats_max = 20
        self.msg_tentative = {
            "moi": "",
            "contre": "",
            "autres": "",
        }
        self.msg_reussite = {
            "moi": "",
            "contre": "",
            "autres": "",
        }
        self.viser_membre = False
        self._construire()
    
    def __getnewargs__(self):
        return (None, "")
    
    def essayer(self, moi, contre, arme=None):
        """Retourne True si l'attaque a réussit, False sinon."""
        return True
    
    def get_membre(self, moi, contre, arme=None):
        """Retourne un membre visé ou None."""
        if self.viser_membre:
            membres = contre.equipement.membres
            membre = choix_probable(membres, attribut="probabilite_atteint")
        else:
            membre = None
        
        return membre
    
    def calculer_degats(self, moi, contre, membre, arme=None):
        """Retourne les dégâts infligés."""
        return randint(self.degats_min, self.degats_max)
    
    def envoyer_msg_tentative(self, moi, contre, membre, arme=None):
        """Envoie les messages en cas de tentative."""
        salle = moi.salle
        moi.envoyer_lisser(self.msg_tentative["moi"].format(moi="{moi}",
                contre="{contre}", membre=membre.nom_complet, arme=arme),
                moi=moi, contre=contre)
        contre.envoyer_lisser(self.msg_tentative["contre"].format(moi="{moi}",
                contre="{contre}", membre=membre.nom_complet, arme=arme),
                moi=moi, contre=contre)
        salle.envoyer_lisser(self.msg_tentative["autres"].format(moi="{moi}",
                contre="{contre}", membre=membre.nom_complet, arme=arme),
                moi=moi, contre=contre)
    
    def envoyer_msg_reussite(self, moi, contre, membre, degats, arme=None):
        """Envoie les messages en cas de réussite."""
        salle = moi.salle
        s = "s" if degats > 1 else ""
        moi.envoyer_lisser(self.msg_reussite["moi"].format(moi="{moi}",
                contre="{contre}", membre=membre.nom_complet, arme=arme,
                degats=degats, s=s), moi=moi, contre=contre)
        contre.envoyer_lisser(self.msg_reussite["contre"].format(moi="{moi}",
                contre="{contre}", membre=membre.nom_complet, arme=arme,
                degats=degats, s=s), moi=moi, contre=contre)
        salle.envoyer_lisser(self.msg_reussite["autres"].format(moi="{moi}",
                contre="{contre}", membre=membre.nom_complet, arme=arme,
                degats=degats, s=s), moi=moi, contre=contre)

class Coup(Attaque):
    
    """Classe représentant un coup."""
    
    def __init__(self, personnage):
        """Constructeur du coup."""
        Attaque.__init__(self, personnage, "coup")
        self.msg_tentative["moi"] = \
                "Vous tentez d'atteindre {contre}."
        self.msg_tentative["contre"] = \
                "{moi} tente de vous atteindre."
        self.msg_tentative["autres"] = \
                "{moi} tente d'atteindre {contre}."
        # Code temporaire
        self.msg_reussite["moi"] = \
                "Vous atteignez {contre} à {membre} ({degats} point{s})."
        self.msg_reussite["contre"] = \
                "{moi} vous atteint à {membre} ({degats} point{s})."
        self.msg_reussite["autres"] = \
                "{moi} atteint {contre} à {membre}."
        self.viser_membre = True
    
    def __getnewargs__(self):
        return (None, )
    
    def essayer(self, moi, contre, arme=None):
        """Retourne True si l'attaque réussit, False sinon."""
        if arme:
            talent = arme.cle_talent
            connaissance = moi.pratiquer_talent(talent)
        else:
            connaissance = moi.pratiquer_talent("combat_mains_nues")
        
        connaissance = varier(connaissance, 20)
        return randint(1, 20) + connaissance >= randint(1, 90)
    
    def calculer_degats(self, moi, contre, membre, arme=None):
        """Retourne les dégâts infligés par l'arme."""
        if arme:
            talent = arme.cle_talent
            connaissance = moi.get_talent(talent)
        else:
            connaissance = moi.get_talent("combat_mains_nues")
        
        facteur = 0.8 + moi.force / 300 + connaissance / 300
        
        if arme:
            degats_min = facteur * arme.degats_fixes
            degats_max = facteur * (arme.degats_fixes + arme.degats_variables)
        else:
            degats_min = facteur * moi.force * 0.9
            degats_max = facteur * moi.force * 1.3
        
        degats = randint(int(degats_min), int(degats_max))
        return degats if degats > 0 else 1
