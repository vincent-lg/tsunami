# -*-coding:Utf-8 -*

# Copyright (c) 2015 LE GOFF Vincent
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


"""Ce fichier contient la classe Commentaire, détaillée plus bas."""

from datetime import datetime

from abstraits.obase import BaseObj

class Commentaire(BaseObj):

    """Classe définissant un commentaire de rapport.

    Un commentaire conserve le rapport d'origine, l'auteur, la
    date du commentaire et le texte du commentaire.

    """

    def __init__(self, rapport, auteur, texte):
        """Constructeur d'un commentaire."""
        BaseObj.__init__(self)
        self.rapport = rapport
        self.auteur = auteur
        self.texte = texte
        self.date = datetime.now()
        self._construire()

    def __getnewargs__(self):
        return (None, None, None)

    def __repr__(self):
        rid = self.rapport and self.rapport.id or "inconnue"
        return "<Commentaire de rapport #{} par {}>".format(rid, self.auteur)

    def notifier(self):
        """On notifie l'auteur du rapport du commentaire."""
        if self.rapport is None:
            raise ValueError("On essaye de commenter un rapport inexistant")

        createur = self.rapport.createur
        participants = [createur]
        for commentaire in self.rapport.commentaires:
            if commentaire.auteur and commentaire.auteur not in participants:
                participants.append(commentaire.auteur)

        for participant in participants:
            if self.auteur is participant:
                continue

            pronom = participant is createur and "Votre" or "Le"
            rid = self.rapport.id
            titre = self.rapport.titre
            participant.envoyer("{pronom} rapport #{} ({}) a été commenté " \
                    "par {}.".format(rid, titre, self.auteur.nom,
                    pronom=pronom))

            systeme = importeur.joueur.joueur_systeme
            mail = importeur.communication.mails.creer_mail(systeme)
            mail.liste_dest.append(participant)
            article = self.auteur is participant and "de votre" or "du"
            mail.sujet = "Comentaire {article} rapport #{} par {}".format(
                    rid, self.auteur.nom, article=article)
            mail.contenu.paragraphes.extend([
                    "|tab|Un nouveau commentaire a été ajouté par " \
                    "{} au rapport #{} ({}) :".format(self.auteur.nom,
                    rid, titre),
                    "|tab|" + self.texte,
                    "",
                    "-" * 70,
            ])
            mail.contenu.paragraphes.extend(
                    self.rapport.get_description_pour(createur).split("\n"))

            mail.envoyer()
