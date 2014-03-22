# -*-coding:Utf-8 -*

# Copyright (c) 2012 LE GOFF Vincent
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


"""Fichier contenant la classe Matelot, détaillée plus bas."""

from abstraits.obase import BaseObj
from primaires.objet.objet import MethodeObjet
from secondaires.navigation.equipage.signaux import *
from secondaires.navigation.equipage.postes import postes
from .ordre import *

class Matelot(BaseObj):

    """Un matelot est un PNJ particulier membre d'un équipage d'un navire.

    Si la classe représentant un Matelot n'est pas directement héritée de PNJ,
    c'est surtout pour permettre la transition à la volée d'un PNJ à un
    matelot et inversement. Si un Matelot est hérité de PNJ, alors un
    PNJ doit être déclaré dès le départ comme un Matelot et ne pourra
    plus être modifié par la suite.

    Le matelot possède plus spécifiquement :
        un poste de prédilection
        une confiance éprouvée envers le capitaine

    Les autres informations sont propres au PNJ et sont accessibles
    directement. La méthode __getattr__ a été construit sur le même
    modèle que celle des objets ou des éléments de navire : si
    l'information n'est pas trouvée dans l'objet, on cherche dans le PNJ.

    """

    logger = type(importeur).man_logs.get_logger("ordres")

    def __init__(self, equipage, personnage):
        """Constructeur du matelot."""
        BaseObj.__init__(self)
        self.equipage = equipage
        self.personnage = personnage
        self.nom_poste = "matelot"
        self.confiance = 0
        self.affectation = None
        self.ordres = []

    def __getnewargs__(self):
        return (None, None)

    def __getattr__(self, nom_attr):
        """On cherche l'attribut dans le personnage."""
        try:
            attribut = getattr(type(self.personnage), nom_attr)
            assert callable(attribut)
            return MethodeObjet(attribut, self)
        except (AttributeError, AssertionError):
            return getattr(self.personnage, nom_attr)

    def __repr__(self):
        return "<mâtelot {} ({})>".format(repr(self.nom), str(self.personnage))

    @property
    def poste(self):
        """Retourne l'objet Poste."""
        return postes[self.nom_poste]

    def get_ordre(self, cle_ordre):
        """Retourne le premier ordre de clé spécifié ou None."""
        ordres = [o for o in self.ordres if o.cle == cle_ordre]
        if ordres:
            return ordres[0]

        return None

    def executer_ordres(self, priorite=1):
        """Exécute les ordres du mâtelot, dans l'ordre.

        Cette méthode doit retourner assez rapidement mais l'exécution
        des ordres peut prendre plusieurs secondes (voire minutes). Le
        module 'diffact' est utilisé pour reprendre l'exécution
        d'ordres plus tard. Les ordres contenus dans cette liste sont
        considérés comme étant des ordres parents (ils n'ont que des
        ordres enfants, mais ceux-ci peuvent avoir des ordres enfants
        également).

        Les différents cas sont gérés par des signaux. Ceux-ci ne
        sont pas des exceptions, mais des formes d'étapes : le système
        peut considérer qu'un signal n'est pas suffisant pour interrompre
        l'ordre et le relance, si besoin avec une plus grande priorité.

        NOTE : le paramètre propriete (entre 1 et 100) permet de rendre
        un ordre plus impératif :
            Un ordre à 1 sera refusé si le moindre problème est anticipé
            Un ordre à 100 sera toujours tenté (urgence !)

        """
        if self.ordres:
            ordre = self.ordres[0]
            generateur = ordre.creer_generateur()
            self.executer_generateur(generateur)

    def executer_generateur(self, generateur, profondeur=0):
        """Exécute récursivement le générateur."""
        indent = "  " * profondeur
        msg = "Exécution du générateur : {}".format(generateur)
        self.logger.debug(indent + msg)
        ordre = generateur.ordre
        volonte = ordre.volonte
        matelot = ordre.matelot
        personnage = matelot.personnage
        if ordre.invalide:
            self.logger.debug(indent + "{} est invalidé".format(ordre))
            return

        if personnage is None or personnage.est_mort():
            self.logger.debug(indent + "{} est mort".format(personnage))
            matelot.relayer_ordres()
            matelot.ordres[:] = []
            return

        etats_autorises = [etat.cle for etat in personnage.etats]
        if any(cle not in ordre.etats_autorises for cle in etats_autorises):
            self.logger.debug(indent + "{} est occupé ({})".format(
                    personnage, personnage.etats))
            matelot.relayer_ordres()
            matelot.ordres[:] = []
            return

        signal = next(generateur)
        self.logger.debug(indent + "Signal {} reçu".format(signal))
        if signal is None:
            # On boucle
            self.executer_generateur(generateur, profondeur)
        elif isinstance(signal, (int, float)):
            tps = signal
            # On ajoute l'action différée
            nom = "ordres_{}".format(id(generateur))
            self.logger.debug(indent + "Pause pendant {} secondes".format(
                    tps))
            importeur.diffact.ajouter_action(nom, tps,
                    self.executer_generateur, generateur, profondeur)
        else:
            signal.traiter(generateur, profondeur)

    def ordonner(self, ordre):
        """Ajoute l'ordre."""
        self.ordres.append(ordre)

    def relayer_ordres(self):
        """Relaye les ordres (demande à être relevé).

        Cette méthode va demander l'ordre à un autre matelot, étant
        entendu que celui-ci (self) ne peut pas les accomplir (pour
        diverses raisons, trop fatigué par exemple). Il faut cependant
        que la raison de la demande de relais soit justifiée et en
        lien avec la volonté, car sinon le même matelot pourrait
        être sélectionné pour les mêmes ordres.

        """
        volontes = []
        for ordre in self.ordres:
            if ordre.volonte and ordre.volonte not in volontes:
                volontes.append(ordre.volonte)

        for volonte in volontes:
            self.equipage.demander(volonte.cle, *volonte.arguments)

    def invalider_ordres(self, cle):
        """Invalide les ordres."""
        for ordre in list(self.ordres):
            if ordre.cle == cle:
                self.ordres.remove(ordre)
                ordre.invalide = True
