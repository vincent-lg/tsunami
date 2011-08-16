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


"""Ce fichier contient la classe Attitude détaillée plus bas."""

import datetime

from abstraits.obase import *
from primaires.format.description import Description

# Etats possible d'un mail
EN_COURS = 0
ENVOYE = 1
BROUILLON = 2
ARCHIVE = 3

SUPPR_AUCUN = 0
SUPPR_DEST = 1
SUPPR_EXP = 2
SUPPR_TOUS = 3

class MUDmail(BaseObj):

    """Cette classe contient un mudmail
    
    """
    
    def __init__(self, parent=None, expediteur=None):
        """Constructeur de la classe"""
        BaseObj.__init__(self)
        self.parent = parent
        mails = type(self).importeur.communication.mails or ""
        self.id = len(mails) + 1
        self._etat = EN_COURS
        self.date = None
        self.sujet = "aucun sujet"
        self.expediteur = expediteur
        self.destinataire = None
        self.contenu = Description()
        self.lu = False
        self.suppr_pour = SUPPR_AUCUN
        # On passe le statut en CONSTRUIT
        self._statut = CONSTRUIT
    
    def __getnewargs__(self):
        return ()
    
    def __setattr__(self, nom_attr, valeur):
        """Enregisre le parent si il est précisé"""
        construit = self.construit
        BaseObj.__setattr__(self, nom_attr, valeur)
        if construit and self.parent:
            self.parent.enregistrer()
    
    @property
    def etat(self):
        """Renvoie l'état du mail"""
        return self._etat
    
    @property
    def nom_dest(self):
        """Renvoie le nom du destinataire si existant"""
        return (self.destinataire is not None and self.destinataire.nom) or \
                "aucun"
    
    @property
    def apercu_contenu(self):
        """Renvoie un aperçu du corps du message"""
        apercu = self.contenu.paragraphes_indentes
        if apercu == "\n   Aucune description.":
            apercu = "\n   Aucun contenu."
        return apercu
    
    def afficher(self):
        """Affiche le mail"""
        ret = "2012-12-21 00:00\n"
        ret += "Sujet : " + self.sujet + "\n"
        ret += str(self.contenu)
        return ret
    
    def enregistrer(self):
        """Enregistrer le mail dans son parent"""
        construit = self.construit
        if construit and self.parent:
            self.parent.enregistrer()
    
    def envoyer(self):
        """Envoie le mail"""
        self._etat = ENVOYE
        self.date = datetime.datetime.now()
        self.enregistrer()
        self.destinataire << "\n|jn|Vous avez reçu un nouveau message.|ff|"
    
    def enregistrer_brouillon(self):
        """Enregistre le mail comme brouillon"""
        self._etat = BROUILLON
        self.date = datetime.datetime.now()
        self.enregistrer()
    
    def archiver(self):
        """Archive le mail"""
        self._etat = ARCHIVE
        self.enregistrer()
    
    def restaurer(self):
        """Restaure le mail"""
        self._etat = ENVOYE
        self.enregistrer()
    
    def suppr_pour_exp():
        """Supprime le mail pour son expéditeur"""
        self.suppr_pour = (SUPPR_DEST and SUPPR_TOUS) or SUPPR_EXP
    
    def suppr_pour_dest():
        """Supprime le mail pour son destinataire"""
        self.suppr_pour = (SUPPR_EXP and SUPPR_TOUS) or SUPPR_DEST
