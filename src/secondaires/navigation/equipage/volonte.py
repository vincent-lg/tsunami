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


"""Fichier contenant la méta-classe et la classe abstraite de volonté."""

from abstraits.obase import BaseObj, MetaBaseObj
from secondaires.navigation.equipage.ordres.revenir import Revenir
from secondaires.navigation.equipage.ordres.terminer_volonte import \
        TerminerVolonte

volontes = {}

class MetaVolonte(MetaBaseObj):

    """Métaclasse des volontés.

    Elle ajoute la volonté dans le dictionnaire 'volontes' si elle possède
    une clé.

    """

    def __init__(cls, nom, bases, contenu):
        """Constructeur de la métaclasse"""
        MetaBaseObj.__init__(cls, nom, bases, contenu)
        if cls.cle:
            volontes[cls.cle] = cls

class Volonte(BaseObj, metaclass=MetaVolonte):

    """Classe représentant une volonté.

    Une volonté n'est pas un ordre, mais elle doit finalement
    créer un ou plusieurs ordres correspondants. Par exemple, une
    volonté pourrait être de hisser une voile, l'ordre généré par cette
    volonté pourrait être de se déplacer dans la salle la plus proche
    possédant une voile, puis hisser la voile, puis revenir.

    """

    cle = ""
    logger = type(importeur).man_logs.get_logger("ordres")
    ordre_court = None
    ordre_long = None

    def __init__(self, navire):
        """Construit une volonté."""
        BaseObj.__init__(self)
        self.navire = navire
        self.initiateur = None
        self._construire()

    def __getnewargs__(self):
        return (None, )

    def __repr__(self):
        return "<volonté '{}.{}{}'".format(self.navire.cle, self.cle,
                self.arguments)

    @property
    def arguments(self):
        """Propriété à redéfinir si la volonté comprend des arguments."""
        return ()

    @property
    def equipage(self):
        return self.navire and self.navire.equipage or None

    def choisir_matelots(self, exception=None):
        """Retourne une liste de matelots les plus aptes.

        Cette méthode doit être redéfinie par les classes héritées.

        """
        raise NotImplementedError

    def executer(self, matelots):
        """Exécute la volonté.

        Cette méthode doit d'abord déduire les ordres nécessaires
        pour accomplir la volonté et ensuite demander au matelot
        de les exécuter.

        """
        raise NotImplementedError

    def terminer(self):
        """Cette méthode est appelée quand une volonté est terminée.

        Elle doit être appelée si la volonté est terminée (peu importe
        qu'elle se soit correctement exécutée ou qu'elle soit
        impossible).

        """
        equipage = self.equipage
        if self in equipage.volontes:
            equipage.volontes.remove(self)
        self.detruire()

    def ajouter_ordres(self, matelot, ordres):
        """Ajoute les ordres au matelot précisé."""
        terminer = TerminerVolonte(matelot, None)
        ordres.append(terminer)
        for ordre in ordres:
            if ordre:
                ordre.volonte = self
                matelot.ordonner(ordre)

        matelot.executer_ordres()

    def revenir_affectation(self, matelot):
        """Demande (si nécessaire) au matelot de revenir à sa sa salle."""
        navire = self.navire
        personnage = matelot.personnage
        salle = personnage.salle
        affectation = matelot.affectation
        revenir = Revenir(matelot, navire)
        revenir.volonte = self
        return revenir


    @classmethod
    def tester(cls, msg):
        """Test si le message correspond à l'ordre court ou long."""
        reg = cls.ordre_court.search(msg) or cls.ordre_long.search(msg)
        if reg:
            return reg.groups()

        return None

    @classmethod
    def extraire_arguments(cls, navire):
        """Extrait les arguments de la volonté."""
        return ()
