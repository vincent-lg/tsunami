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
from primaires.format.date import get_date

# Etats possible d'un mail
EN_COURS = 0
ENVOYE = 1
BROUILLON = 2
ARCHIVE = 3
RECU = 4

class MUDmail(BaseObj):

    """Cette classe contient un mudmail.
    
    """
    
    def __init__(self, parent=None, expediteur=None, source=None):
        """Constructeur de la classe"""
        BaseObj.__init__(self)
        self.parent = parent
        mails = type(self).importeur.communication.mails or {}
        self.id = len(mails) + 1
        if source is not None: # édition d'un brouillon
            self._etat = BROUILLON
            self.sujet = str(source.sujet)
            self.expediteur = expediteur
            self.liste_dest = list(source.liste_dest)
            self.contenu = Description()
            self.contenu.ajouter_paragraphe(str(source.contenu))
            self.id_source = int(source.id)
        else:
            self._etat = EN_COURS
            self.sujet = "aucun sujet"
            self.expediteur = expediteur
            self.liste_dest = []
            self.contenu = Description()
            self.id_source = 0
        self.destinataire = None
        self.date = None
        self.lu = False
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
    def aff_dest(self):
        """Renvoie le(s) destinataire(s) si existant(s)"""
        res = ""
        if self.destinataire:
            res += self.destinataire.nom
        else:
            res += ", ".join([dest.nom for dest in self.liste_dest])
            if not res:
                res += "aucun"
        return res
    
    @property
    def apercu_contenu(self):
        """Renvoie un aperçu du corps du message"""
        apercu = self.contenu.paragraphes_indentes
        if apercu == "\n   Aucune description.":
            apercu = "\n   Aucun contenu."
        return apercu
    
    def afficher(self):
        """Affiche le mail"""
        ret = "Expéditeur      : " + self.expediteur.nom + "\n"
        ret += "Destinataire(s) : " + self.aff_dest + "\n"
        ret += "Sujet           : " + self.sujet + "\n"
        ret += str(self.contenu)
        ret += "\n" + get_date(self.date.timetuple()).capitalize() + "."
        return ret
    
    def enregistrer(self):
        """Enregistre le mail dans son parent"""
        construit = self.construit
        if construit and self.parent:
            self.parent.enregistrer()
    
    def envoyer(self):
        """Envoie le mail"""
        for dest in self.liste_dest:
            mail = type(self).importeur.communication.mails.creer_mail(
                    self.expediteur)
            mail.date = datetime.datetime.now()
            mail.sujet = self.sujet
            mail.destinataire = dest
            mail.contenu = self.contenu
            mail._etat = RECU
            mail.enregistrer()
            if dest in type(self).importeur.connex.joueurs_connectes:
                dest << "\n|jn|Vous avez reçu un nouveau message.|ff|"
        self.date = datetime.datetime.now()
        self._etat = ENVOYE
        self.enregistrer()
    
    def enregistrer_brouillon(self):
        """Enregistre le mail comme brouillon"""
        self.date = datetime.datetime.now()
        self._etat = BROUILLON
        self.enregistrer()
    
    def archiver(self):
        """Archive le mail"""
        self._etat = ARCHIVE
        self.enregistrer()
    
    def restaurer(self):
        """Restaure le mail"""
        self._etat = RECU
        self.enregistrer()
