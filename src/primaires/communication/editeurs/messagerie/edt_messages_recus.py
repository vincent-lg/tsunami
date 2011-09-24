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


"""Fichier contenant le contexte éditeur EdtMessagesRecus"""

from primaires.interpreteur.editeur import Editeur
from primaires.interpreteur.editeur.env_objet import EnveloppeObjet
from primaires.communication.editeurs.medit import EdtMedit
from primaires.communication.mudmail import RECU
from primaires.format.fonctions import couper_phrase

class EdtMessagesRecus(Editeur):
    
    """Classe définissant le contexte-éditeur 'messages reçus'.
    Ce contexte liste les messages reçus et propose des options d'édition.
    
    """
    
    def __init__(self, pere, objet=None, attribut=None):
        """Constructeur de l'éditeur"""
        Editeur.__init__(self, pere, objet, attribut)
        self.ajouter_option("l", self.opt_lire)
        self.ajouter_option("a", self.opt_archiver)
        self.ajouter_option("r", self.opt_repondre)
        self.ajouter_option("b", self.opt_boite_refresh)
    
    def accueil(self):
        """Méthode d'accueil"""
        joueur = self.pere.joueur
        mails = type(self).importeur.communication.mails.get_mails_pour(
                joueur, RECU)
        nb_mails = len(mails)
        prf_mails = (nb_mails > 1 and "s") or ""
        nb_non_lus = len([mail for mail in mails if not mail.lu])
        prf_non_lus = (nb_non_lus > 1 and "s") or ""
        nb_non_lus = (nb_non_lus != 0 and "|rgc|" + str(nb_non_lus) + "|ff|") \
                or "aucun"
        msg = "||tit| " + "Messages reçus".ljust(76) + "|ff||\n"
        msg += self.opts.separateur + "\n"
        msg += self.aide_courte + "\n\n"
        if nb_mails != 0:
            msg += "|blc|" + str(nb_mails) + "|ff| message" + prf_mails
            msg += " dont " + nb_non_lus + " non lu" + prf_non_lus
            msg += "\n"
        
        if not mails:
            msg += "|att|Vous n'avez reçu aucun message.|ff|"
        else:
            taille = 0
            for mail in mails:
                t_sujet = len(couper_phrase(mail.sujet, 29))
                if t_sujet > taille:
                    taille = t_sujet
            taille = (taille < 5 and 5) or taille
            msg += "+" + "-".ljust(taille + 45, "-") + "+\n"
            msg += "| |tit|N°|ff| | |tit|Lu|ff|  | |tit|" + "Sujet".ljust(taille)
            msg += "|ff| | |tit|Expéditeur|ff| | |tit|" + "Date".ljust(16)
            msg += "|ff| |\n"
            i = 1
            for mail in mails:
                msg += "| |rg|" + str(i).ljust(2) + "|ff| | "
                msg += (mail.lu and "|vrc|oui|ff|" or "|rgc|non|ff|")
                msg += " | |vr|" + couper_phrase(mail.sujet, 29).ljust( \
                        taille) + "|ff| | |blc|"
                msg += mail.expediteur.nom.ljust(10) + "|ff| | |jn|"
                msg += mail.date.isoformat(" ")[:16] + "|ff| |\n"
                i += 1
            msg += "+" + "-".ljust(taille + 45, "-") + "+"
        
        return msg
    
    def opt_lire(self, arguments):
        """Option lire"""
        if not arguments or arguments.isspace():
            self.pere.joueur << "|err|Vous devez préciser le numéro d'un " \
                    "message.|ff|"
            return
        mails = type(self).importeur.communication.mails.get_mails_pour(
                self.pere.joueur, RECU)
        try:
            num = int(arguments.split(" ")[0])
        except ValueError:
            self.pere.joueur << "|err|Vous devez spécifier un nombre entier " \
                    "valide.|ff|"
        else:
            i = 1
            l_mail = None
            for mail in mails:
                if num == i:
                    l_mail = mail
                    break
                i += 1
            if l_mail is None:
                self.pere.joueur << "|err|Le numéro spécifié ne correspond à " \
                        "aucun message.|ff|"
                return
            self.pere.joueur << l_mail.afficher()
            l_mail.lu = True
    
    def opt_archiver(self, arguments):
        """Option archiver"""
        if not arguments or arguments.isspace():
            self.pere.joueur << "|err|Vous devez préciser le numéro d'un " \
                    "message.|ff|"
            return
        mails = type(self).importeur.communication.mails.get_mails_pour(
                self.pere.joueur, RECU)
        try:
            num = int(arguments.split(" ")[0])
        except ValueError:
            self.pere.joueur << "|err|Vous devez spécifier un nombre entier " \
                    "valide.|ff|"
        else:
            i = 1
            a_mail = None
            for mail in mails:
                if num == i:
                    a_mail = mail
                    break
                i += 1
            if a_mail is None:
                self.pere.joueur << "|err|Le numéro spécifié ne correspond à " \
                        "aucun message.|ff|"
                return
            a_mail.archiver()
            self.pere.joueur << "|att|Le message a bien été archivé.|ff|"
    
    def opt_repondre(self, arguments):
        """Option répondre"""
        if not arguments or arguments.isspace():
            self.pere.joueur << "|err|Vous devez préciser le numéro d'un " \
                    "message.|ff|"
            return
        mails = type(self).importeur.communication.mails.get_mails_pour(
                self.pere.joueur, RECU)
        try:
            num = int(arguments.split(" ")[0])
        except ValueError:
            self.pere.joueur << "|err|Vous devez spécifier un nombre entier " \
                    "valide.|ff|"
        else:
            i = 1
            r_mail = None
            for mail in mails:
                if num == i:
                    r_mail = mail
                    break
                i += 1
            if r_mail is None:
                self.pere.joueur << "|err|Le numéro spécifié ne correspond à " \
                        "aucun message.|ff|"
                return
            mail = type(self).importeur.communication.mails.creer_mail(
                    self.pere.joueur)
            mail.sujet = "RE:" + r_mail.sujet
            mail.liste_dest.append(r_mail.expediteur)
            mail.contenu.ajouter_paragraphe(
                    r_mail.expediteur.nom + " a écrit :\n")
            mail.contenu.ajouter_paragraphe(str(r_mail.contenu))
            mail.contenu.ajouter_paragrape("<------------->")
            enveloppe = EnveloppeObjet(EdtMedit, mail, None)
            enveloppe.parent = self
            contexte = enveloppe.construire(self.pere.joueur)
            self.pere.joueur.contextes.ajouter(contexte)
            contexte.actualiser()
    
    def opt_boite_refresh(self, arguments):
        """Option de réactualisation"""        
        self.pere.joueur << self.opts.separateur + "\n" + self.accueil()
