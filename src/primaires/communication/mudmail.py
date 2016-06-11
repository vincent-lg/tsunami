# -*-coding:Utf-8 -*

# Copyright (c) 2010-2016 LE GOFF Vincent
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
from primaires.communication.constantes import bas_page
from primaires.format.date import get_date
from primaires.format.description import Description
from primaires.format.fonctions import echapper_accolades

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
        self.id = -1
        self.notifier = True
        if source is not None: # édition d'un brouillon
            self._etat = BROUILLON
            self.sujet = str(source.sujet)
            self.expediteur = expediteur
            self.liste_dest = []
            for d in list(source.liste_dest):
                self.liste_dest.append(d)
            self.aliases = source.aliases
            self.copies_a = source.copies_a
            self.contenu = Description(parent=self, scriptable=False)
            self.contenu.ajouter_paragraphe(str(source.contenu))
            self.id_source = int(source.id)
        else:
            self._etat = EN_COURS
            self.sujet = "aucun sujet"
            self.expediteur = expediteur
            self.liste_dest = []
            self.aliases = []
            self.copies_a = []
            self.contenu = Description(parent=self)
            self.id_source = 0
        self.destinataire = None
        self.date = None
        self.lu = False
        # On passe le statut en CONSTRUIT
        self._construire()

    def __getnewargs__(self):
        return ()

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
            if self.aliases:
                res += ", " if res else ""
                res += ", ".join(["|bc|@" + a.nom_alias + "|ff|" \
                        for a in self.aliases])
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

    @property
    def nom_expediteur(self):
        """Retourne, si trouvé, le nom de l'expéditeur."""
        return self.expediteur and self.expediteur.nom or "inconnu"

    def afficher(self):
        """Affiche le mail"""
        ret = "Expéditeur      : " + self.expediteur.nom + "\n"
        ret += "Destinataire(s) : " + self.aff_dest + "\n"
        ret += "Sujet           : " + echapper_accolades(self.sujet) + "\n"
        ret += echapper_accolades(str(self.contenu))
        ret += "\n" + get_date(self.date.timetuple()).capitalize() + "."
        return ret

    def envoyer(self):
        """Envoie le mail"""
        liste_dest = set(self.liste_dest)
        if self.aliases:
            for alias in self.aliases:
                [liste_dest.add(j) for j in alias.retourner_joueurs()]
        if self.expediteur in liste_dest:
            liste_dest.remove(self.expediteur)

        if not liste_dest:
            raise ValueError("la liste de destinataires est vide")

        self.date = datetime.datetime.now()
        for dest in liste_dest:
            mail = type(self).importeur.communication.mails.creer_mail(
                    self.expediteur)
            mail.date = datetime.datetime.now()
            mail.sujet = self.sujet
            mail.destinataire = dest
            mail.contenu = self.contenu
            mail.copies_a = list(self.liste_dest) + list(self.aliases)
            if dest in mail.copies_a:
                mail.copies_a.remove(dest)
            mail._etat = RECU
            if dest in type(self).importeur.connex.joueurs_connectes:
                dest << "\n|jn|Vous avez reçu un nouveau message.|ff|"
            if self.notifier:
                self.envoyer_email(dest)
        self._etat = ENVOYE

    def archiver(self):
        """Archive le mail"""
        self._etat = ARCHIVE

    def restaurer(self):
        """Restaure le mail"""
        self._etat = RECU

    def envoyer_email(self, dest):
        """Envoie l'e-mail au destinataire."""
        if not dest.compte.email:
            return

        destinateur = "equipe"
        destinataire = dest.compte.adresse_email
        expediteur = self.expediteur.nom
        sujet = "[VanciaMUD] : " + self.sujet
        nom_compte = dest.compte.nom
        contenu = self.afficher().replace("|tab|", "   ")
        corps = contenu + bas_page.format(nom_compte=nom_compte,
                expediteur=expediteur)
        if not importeur.email.serveur_mail:
            return

        if not destinataire:
            return

        importeur.email.envoyer(destinateur, destinataire, sujet, corps)
