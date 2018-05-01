# -*-coding:Utf-8 -*

# Copyright (c) 2010-2017 LE GOFF Vincent
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


"""Fichier contenant le paramètre 'message' de la commande 'rapport'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmMessage(Parametre):

    """Commande 'rapport message'.

    """

    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "message", "mail")
        self.schema = "<nombre>"
        self.groupe = "administrateur"
        self.aide_courte = "envoie un message à l'auteur"
        self.aide_longue = \
            "Cette commande permet d'envoyer un message à l'auteur du " \
            "rapport précisé."

    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        id = dic_masques["nombre"].nombre
        try:
            rapport = importeur.rapport.rapports[id]
        except KeyError:
            personnage << "|err|Ce rapport n'existe pas.|ff|"
        else:
            mail = type(self).importeur.communication.mails.creer_mail(
                    personnage)
            mail.liste_dest.append(rapport.createur)
            mail.sujet = "Rapport #" + str(rapport.id) + " : " + rapport.titre
            editeur = type(self).importeur.interpreteur.construire_editeur(
                    "medit", personnage, mail)
            personnage.contextes.ajouter(editeur)
            editeur.actualiser()
