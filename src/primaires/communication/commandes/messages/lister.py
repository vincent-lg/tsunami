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


"""Fichier contenant le paramètre 'lister' de la commande 'messages'."""

from primaires.format.fonctions import couper_phrase
from primaires.communication.mudmail import RECU, ENVOYE, BROUILLON, ARCHIVE
from primaires.interpreteur.masque.parametre import Parametre

class PrmLister(Parametre):
    
    """Commande 'messages lister'.
    
    """
    
    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "lister", "list")
        self.schema = "(<flag_mail>)"
        self.aide_courte = "liste les mudmails"
        self.aide_longue = \
            "Cette sous-commande permet de lister vos message selon un flag " \
            "de filtre. Les flags existants sont recus, brouillons, archives " \
            "et envoyes. Si vous ne précisez pas de filtre, la commande " \
            "renvoie vos messages non lus."
    
    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        flag = ""
        mails = type(self).importeur.communication.mails
        if dic_masques["flag_mail"] is not None:
            flag = dic_masques["flag_mail"].flag
            if flag == "recus":
                mails = mails.get_mails_pour(personnage, RECU)
            elif flag == "brouillons":
                mails = mails.get_mails_pour(personnage, BROUILLON)
            elif flag == "archives":
                mails = mails.get_mails_pour(personnage, ARCHIVE)
            elif flag == "envoyes":
                mails = mails.get_mails_pour(personnage, ENVOYE)
        else:
            mails = mails.get_mails_pour(personnage, RECU)
            mails = [mail for mail in mails if not mail.lu]
        
        if not mails:
            personnage << "|att|Vous n'avez aucun message dans cette " \
                    "catégorie.|ff|"
        else:
            if flag == "brouillons" or flag == "envoyes":
                taille = 0
                for mail in mails:
                    t_sujet = len(couper_phrase(mail.sujet, 33))
                    if t_sujet > taille:
                        taille = t_sujet
                taille = (taille < 5 and 5) or taille
                msg = "+" + "-".ljust(taille + 41, "-") + "+\n"
                msg += "| |tit|N°|ff| | |tit|" + "Sujet".ljust(taille)
                msg += "|ff| | |tit|Destinataire|ff| | |tit|" + "Date".ljust(16)
                msg += "|ff| |\n"
                i = 1
                for mail in mails:
                    msg += "| |rg|" + str(i).ljust(2) + "|ff| | "
                    msg += "|vr|" + couper_phrase(mail.sujet, 33).ljust( \
                            taille) + "|ff| | |blc|"
                    msg += couper_phrase(mail.aff_dest,12).ljust(12) + "|ff| | "
                    msg += "|jn|" + mail.date.isoformat(" ")[:16] + "|ff| |\n"
                    i += 1
                msg += "+" + "-".ljust(taille + 41, "-") + "+"
            else:
                taille = 0
                for mail in mails:
                    t_sujet = len(couper_phrase(mail.sujet, 29))
                    if t_sujet > taille:
                        taille = t_sujet
                taille = (taille < 5 and 5) or taille
                msg = "+" + "-".ljust(taille + 45, "-") + "+\n"
                msg += "| |tit|N°|ff| | |tit|Lu|ff|  | |tit|" + "Sujet".ljust(
                        taille)
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
            personnage << msg
