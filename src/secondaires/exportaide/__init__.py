# -*-coding:Utf-8 -*

# Copyright (c) 2013 LE GOFF Vincent
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


"""Fichier contenant le module secondaire exportaide.

Ce module est utilisé pour exporter l'aide IG (aide des commandes et des
sujets d'aide) dans différents formats.

"""

from abstraits.module import *

from secondaires.exportaide.config import CFG_FORMAT
from secondaires.exportaide.formats.pgsql.format import PGFormat

formats = {
    "pgsql": PGFormat,
}

class Module(BaseModule):

    """Module utilisé pour exporter l'aide IG dans différents formats.

    Les formats sont décrit dans le sous-package 'formats'. Ils ont
    chacun leur configuration.

    """
    def __init__(self, importeur):
        """Constructeur du module"""
        BaseModule.__init__(self, importeur, "exportaide", "secondaire")
        self.format = None
        self.exp_logger = type(importeur).man_logs.creer_logger(
                "exportaide", "exportaide", "exportaide.log")

    def config(self):
        """Méthode de configuration.

        On récupère le fichier de configuration correspondant au module.

        """
        self.cfg = type(self.importeur).anaconf.get_config("exportaide",
                "exportaide/format.cfg", "modele format", CFG_FORMAT)

        BaseModule.config(self)

    def preparer(self):
        """Préparation du module."""
        nom_format = self.cfg.nom_format
        if nom_format:
            self.exporter_aide()

    def exporter_aide(self):
        """Exporte l'aide.

        Cette méthode est appelée lros de la préparation du module mais
        peut aussi être appelée à n'importe quel moment pour mettre à jour
        l'aide exportée.

        """
        nom_format = self.cfg.nom_format
        if nom_format is None:
            self.exp_logger.fatal(
                    "le format spécifié dans la configuration est indéfini")
            return

        if nom_format not in formats:
            self.exp_logger.fatal("Format d'export {} inconnu".format(
                    repr(nom_format)))
            return

        format = formats[nom_format]()
        if not format.peut_tourner:
            self.format.exp_logger.fatal("Le format {} sélectionné ne peut " \
                    "pas s'exécuter, probablement à cause de modules " \
                    "tierses manquants".format(repr(nom_format)))
            return

        format.config()
        if not format.init():
            self.exp_logger.fatal("Initialisation du format {} échouée. " \
                    "Export annulé.".format(repr(nom_format)))
            return

        format.exporter_commandes()
