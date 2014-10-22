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


"""Fichier contenant le contexte éditeur EdtBrouillons"""

from primaires.interpreteur.editeur import Editeur
from primaires.interpreteur.editeur.env_objet import EnveloppeObjet
from primaires.communication.editeurs.medit import EdtMedit
from primaires.communication.mudmail import BROUILLON
from primaires.format.fonctions import couper_phrase

class EdtBrouillons(Editeur):
    
    """Classe définissant le contexte-éditeur 'brouillons'.
    Ce contexte liste les brouillons et propose des options d'édition.
    
    """
    
    def __init__(self, pere, objet=None, attribut=None):
        """Constructeur de l'éditeur"""
        Editeur.__init__(self, pere, objet, attribut)
        self.ajouter_option("e", self.opt_editer)
        self.ajouter_option("s", self.opt_supprimer)
    
    def accueil(self):
        """Méthode d'accueil"""
        joueur = self.pere.joueur
        mails = type(self).importeur.communication.mails.get_mails_pour(
                joueur, BROUILLON)
        msg = "||tit| " + "Brouillons".ljust(76) + "|ff||\n"
        msg += self.opts.separateur + "\n"
        msg += self.aide_courte + "\n\n"
        
        if not mails:
            msg += "|att|Aucun message enregistré dans ce dossier.|ff|"
        else:
            taille = 0
            for mail in mails:
                t_sujet = len(couper_phrase(mail.sujet, 33))
                if t_sujet > taille:
                    taille = t_sujet
            taille = (taille < 5 and 5) or taille
            msg += "+" + "-".ljust(taille + 41, "-") + "+\n"
            msg += "| |tit|N°|ff| | |tit|" + "Sujet".ljust(taille)
            msg += "|ff| | |tit|Destinataire|ff| | |tit|" + "Date".ljust(16)
            msg += "|ff| |\n"
            i = 1
            for mail in mails:
                msg += "| |rg|" + str(i).rjust(2) + "|ff| | "
                msg += "|vr|" + couper_phrase(mail.sujet, 33).ljust( \
                        taille) + "|ff| | |blc|"
                msg += couper_phrase(mail.aff_dest,12).ljust(12) + "|ff| | "
                msg += "|jn|" + mail.date.isoformat(" ")[:16] + "|ff| |\n"
                i += 1
            msg += "+" + "-".ljust(taille + 41, "-") + "+"
        
        return msg
    
    def opt_editer(self, arguments):
        """Option éditer"""
        if not arguments or arguments.isspace():
            self.pere.joueur << "|err|Vous devez préciser le numéro d'un " \
                    "message.|ff|"
            return
        mails = type(self).importeur.communication.mails.get_mails_pour(
                self.pere.joueur, BROUILLON)
        try:
            num = int(arguments.split(" ")[0])
        except ValueError:
            self.pere.joueur << "|err|Vous devez spécifier un nombre entier " \
                    "valide.|ff|"
        else:
            i = 1
            e_mail = None
            for mail in mails:
                if num == i:
                    e_mail = mail
                    break
                i += 1
            if e_mail is None:
                self.pere.joueur << "|err|Le numéro spécifié ne correspond " \
                        "à aucun message.|ff|"
                return
            brouillon = type(self).importeur.communication.mails.creer_mail( \
                e_mail.expediteur, source=e_mail)
            enveloppe = EnveloppeObjet(EdtMedit, brouillon, None)
            enveloppe.parent = self
            contexte = enveloppe.construire(self.pere.joueur)
            contexte.opts.rci_ctx_prec = ""
            self.pere.joueur.contextes.ajouter(contexte)
            contexte.actualiser()
    
    def opt_supprimer(self, arguments):
        """Option supprimer"""
        if not arguments or arguments.isspace():
            self.pere.joueur << "|err|Vous devez préciser le numéro d'un " \
                    "message.|ff|"
            return
        mails = type(self).importeur.communication.mails.get_mails_pour(
                self.pere.joueur, BROUILLON)
        try:
            num = int(arguments.split(" ")[0])
        except ValueError:
            self.pere.joueur << "|err|Vous devez spécifier un nombre entier " \
                    "valide.|ff|"
        else:
            i = 1
            s_mail = None
            for mail in mails:
                if num == i:
                    s_mail = mail
                    break
                i += 1
            if s_mail is None:
                self.pere.joueur << "|err|Le numéro spécifié ne correspond à " \
                        "aucun message.|ff|"
                return
            del type(self).importeur.communication.mails[s_mail.id]
            self.pere.joueur << "|att|Ce message a bien été supprimé.|ff|"
