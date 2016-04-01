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


"""Ce fichier contient la classe Detail, détaillée plus bas."""

from abstraits.obase import *
from primaires.format.description import Description
from primaires.format.fonctions import oui_ou_non
from primaires.objet.conteneur import ConteneurObjet
from primaires.scripting.script import Script

# Constantes
FLAGS = {
    "fontaine": 1,
    "cheminée": 2,
}

class Detail(BaseObj):

    """Cette classe représente un détail observable dans une salle.

    Elle permet d'ajouter à la description d'une salle des détails invisibles
    au premier abord, mais discernable avec la commande look.

    """

    nom_scripting = "le détail"
    def __init__(self, nom, parent=None, modele=None):
        """Constructeur de la classe"""
        BaseObj.__init__(self)
        self.nom = nom
        self.synonymes = []
        self.titre = "un détail aux alentours"
        self.description = Description(parent=self)
        self.positions = {}
        self.est_visible = True
        self.script = ScriptDetail(self)
        self.peut_asseoir = False
        self.peut_allonger = False
        self.facteur_asseoir = 1.1
        self.facteur_allonger = 1.2
        self.connecteur = "sur"
        self.nb_places_assises = 1
        self.nb_places_allongees = 1
        self.parent = parent
        self.flags = 0
        self.supporte = None
        self._peut_supporter = 0.0
        self.message_supporte = "Dessus se trouve"
        self.message_installation = "Vous posez %objet sur %detail."
        self.message_desinstallation = "Vous retirez %objet% de %detail."
        if modele is not None:
            self.synonymes = modele.synonymes
            self.titre = modele.titre
            self.description = modele.description
        # On passe le statut en CONSTRUIT
        self._construire()

    def __getnewargs__(self):
        return ("", "")

    def __str__(self):
        return self.titre.lower()

    @property
    def repos(self):
        return oui_ou_non(self.peut_asseoir or self.peut_allonger)

    @property
    def support(self):
        """Retourne oui_ou_non."""
        return oui_ou_non(self._peut_supporter > 0)

    def _get_peut_supporter(self):
        return self._peut_supporter
    def _set_peut_supporter(self, poids):
        self._peut_supporter = poids
        if poids:
            if self.supporte is None:
                self.supporte = ConteneurObjet(self)
        else:
            if self.supporte:
                self.supporte.detruire()
                self.supporte = None
    peut_supporter = property(_get_peut_supporter, _set_peut_supporter)

    def get_nom_pour(self, personnage):
        """Retourne le nom pour le personnage précisé."""
        return self.titre

    def a_flag(self, nom_flag):
        """Retourne True si le détail a le flag, False sinon."""
        valeur = FLAGS[nom_flag]
        return self.flags & valeur != 0

    def regarder(self, personnage):
        """Le personnage regarde le détail"""
        if not self.est_visible:
            personnage << "Il n'y a rien qui ressemble à cela par ici..."
            return
        personnage << "Vous examinez {} :".format(self.titre)
        self.script["regarde"]["avant"].executer(personnage=personnage,
                salle=personnage.salle)
        description = self.description.regarder(personnage, self)
        if not description:
            description = "Il n'y a rien de bien intéressant à voir."

        personnage << description

        self.script["regarde"]["apres"].executer(personnage=personnage,
                salle=personnage.salle)

class ScriptDetail(Script):

    """Script s'appliquant à un détail."""

    def init(self):
        """Initialisation du script"""
        # Événement asseoit
        evt_asseoit = self.creer_evenement("asseoit")
        evt_asseoit.aide_courte = "un personnage s'asseoit sur un détail"
        evt_asseoit.aide_longue = \
            "Cet évènement est appelé quand un personnage s'asseoit " \
            "sur un détail dans la salle. Il se produit après le " \
            "message comme quoi le personnage s'est assis. L'état " \
            "a déjà été renseigné."

        # Configuration des variables de l'évènement asseoit
        var_perso = evt_asseoit.ajouter_variable("personnage", "Personnage")
        var_perso.aide = "le personnage s'asseyant"

        # Événement allonge
        evt_allonge = self.creer_evenement("allonge")
        evt_allonge.aide_courte = "un personnage s'allonge sur un détail"
        evt_allonge.aide_longue = \
            "Cet évènement est appelé quand un personnage s'allonge " \
            "sur un détail dans la salle. Il se produit après le " \
            "message comme quoi le personnage s'est allongé. L'état " \
            "a déjà été renseigné."

        # Configuration des variables de l'évènement allonge
        var_perso = evt_allonge.ajouter_variable("personnage", "Personnage")
        var_perso.aide = "le personnage s'allongeant"

        # Événement regarde
        evt_regarde = self.creer_evenement("regarde")
        evt_reg_avant = evt_regarde.creer_evenement("avant")
        evt_reg_apres = evt_regarde.creer_evenement("après")
        evt_regarde.aide_courte = "un personnage regarde le détail"
        evt_reg_avant.aide_courte = "avant la description du détail"
        evt_reg_apres.aide_courte = "après la description du détail"
        evt_regarde.aide_longue = \
            "Cet évènement est appelé quand un personnage regarde le détail."
        evt_reg_avant.aide_longue = \
            "Cet évènement est appelé avant que la description du détail " \
            "ne soit envoyée au personnage le regardant."
        evt_reg_apres.aide_longue = \
            "Cet évènement est appelé après que la description du détail " \
            "ait été envoyée au personnage le regardant."

        # Configuration des variables de l'évènement regarde
        var_perso = evt_regarde.ajouter_variable("personnage", "Personnage")
        var_perso.aide = "le personnage regardant le détail"
        var_salle = evt_regarde.ajouter_variable("salle", "Salle")
        var_salle.aide = "la salle dans laquelle se trouve le détail"
