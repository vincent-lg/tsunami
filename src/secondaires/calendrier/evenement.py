# -*-coding:Utf-8 -*

# Copyright (c) 2010-2016 AYDIN Ali-Kémal
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

"""Ce fichier contient la classe Evenement, détaillée plus bas."""

import datetime

from abstraits.obase import BaseObj
from primaires.format.description import Description
from primaires.format.date import get_date

from .commentaire import Commentaire

class Evenement(BaseObj):

    """Classe définissant un évènement pour le calendrier.

    Un évènement est défini par un ID, qui est unique, un titre,
    une description courte, ainsi qu'une description longue, son
    créateur et ses responsables et enfin les commentaires lui
    correspondant.

    """

    enregistrer = True
    id_actuel = 1

    def __init__(self, createur):
        """Constructeur d'un évènement"""
        BaseObj.__init__(self)
        self.id = type(self).id_actuel
        type(self).id_actuel += 1
        self.date = datetime.date.today()
        self.responsables = [createur]
        self.titre = "Sans Titre"
        self.description = Description(parent = self)
        self.commentaires = []
        self._construire()

    def __getnewargs__(self):
        return (None, )

    def __repr__(self):
        return "<évènement {}>".format(self.id)

    def __str__(self):
        return str(self.id)

    @property
    def str_detail(self):
        """Renvoie une présentation détaillée de l'évènement."""
        info_generale = \
                "Id : {id}\n" \
                "Titre : {titre}\n" \
                "Date : Pour {date}\n" \
                "Description :\n    {desc}\n" \
                "Responsables : {resp}\n" \

        nom_responsables = ", ".join([resp.nom for resp in self.responsables])

        info_generale = info_generale.format(id=self.id,
            titre=self.titre, date=self.str_date, desc=self.description,
            resp=nom_responsables)

        commentaires = ""
        if self.commentaires:
            commentaires = "Commentaires :\n"
            for comm in self.commentaires:
                commentaires += "\n{}".format(comm)
            info_generale += "\n\n" + commentaires

        return info_generale

    @property
    def str_date(self):
        """Retourne la date en format français."""
        return get_date(self.date.timetuple())

    def ajouter_commentaire(self, personnage, commentaire):
        """Ajoute un commentaire"""
        self.commentaires.append(Commentaire(self, personnage, commentaire))
        self._enregistrer()

    def detruire(self):
        """Destruction de l'évènement."""
        BaseObj.detruire(self)
        self.description.detruire()
        for commentaire in self.commentaires:
            commentaire.detruire()
