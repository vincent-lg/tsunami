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

    enregistrer = True
    def __init__(self, equipage, personnage):
        """Constructeur du matelot."""
        BaseObj.__init__(self)
        self.equipage = equipage
        self.personnage = personnage
        self.nom_poste = "matelot"
        self.confiance = 0
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

    def executer_ordre(self, priorite=1):
        """Exécute le premier ordre de la liste.

        Traite les cas :
            Impossibilité anticipée -> annulation
            Difficulté anticipée -> information
            Empêchement temporaire -> information
            Impossibilité constatée -> annulation

        En fonction du statut de l'ordre, la liste entière peut être affectée.

        NOTE : le paramètre propriete (entre 1 et 100) permet de rendre
        un ordre plus impératif :
            Un ordre à 1 sera refusé si le moindre problème est anticipé
            Un ordre à 100 sera toujours tenté (urgence !)

        """
        if self.ordres:
            ordre = self.ordres[0]
            if ordre.calculer_empechement() > priorite:
                raise PrioriteTropFaible

            ordre.lancer()

    def execution_progressive(self, generateur):
        """Execution progressive de l'ordre."""
        for alerte in generateur:
            if isinstance(alerte, (int, float)):
                # L'alerte est un temps, on met en pause l'ordre
                tps = alerte
                # On ajoute l'action différée
                nom = "ordres_{}".format(id(generateur))
                importeur.diffact.ajouter_action(nom, tps,
                        self.execution_progressive, generateur)
            else:
                raise ValueError("Type d'alerte inconnu {}".format(
                        repr(alerte)))

    def ordonner(self, ordre):
        """Ajoute l'ordre."""
        self.ordres.append(ordre)

    def detruire(self):
        """Destruction du matelot."""
        self.personnage.detruire()
