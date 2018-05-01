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

    @property
    def navire(self):
        """Retourne le navire de l'équipage."""
        if self.equipage:
            return self.equipage.navire
        else:
            return None

    def get_ordre(self, cle_ordre):
        """Retourne le premier ordre de clé spécifié ou None."""
        ordres = [o for o in self.ordres if o.cle == cle_ordre]
        if ordres:
            return ordres[0]

        return None

    def nettoyer_ordres(self):
        """Retire les ordres doubles."""
        volontes = self.equipage.volontes
        uniques = []
        args = []
        for ordre in self.ordres:
            if ordre.volonte and ordre.volonte not in volontes:
                continue

            arg = (ordre.cle, ) + ordre.arguments_suplementaires
            if arg not in args:
                args.append(arg)
                uniques.append(ordre)

        self.ordres[:] = uniques

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

        if ordre.peut_deleguer and (personnage is None or \
                personnage.est_mort()):
            self.logger.debug(indent + "{} est mort".format(personnage))
            matelot.relayer_ordres()
            matelot.ordres[:] = []
            return

        etats = [etat.cle for etat in personnage.etats]
        if ordre.etats_autorises != ("*", ) and \
                any(cle not in ordre.etats_autorises for cle in etats) and \
                ordre.peut_deleguer:
            self.logger.debug(indent + "{} est occupé ({} {})".format(
                    personnage, personnage.etats, ordre.etats_autorises))
            matelot.relayer_ordres()
            matelot.ordres[:] = []
            return

        try:
            signal = next(generateur)
        except StopIteration:
            matelot.ordres[:] = []
            return

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
            self.equipage.demander(volonte.cle, *volonte.arguments,
                    exception=self)

    def invalider_ordres(self, cle):
        """Invalide les ordres."""
        for ordre in list(self.ordres):
            if ordre.cle == cle:
                self.ordres.remove(ordre)
                ordre.invalide = True

    # Gestion de l'équipement
    def jeter_ou_entreposer(self, exception=""):
        """Jette les objets tenus ou les met en cale.

        Si l'objet tenu peut être mis en cale, il est entreposé. Sinon
        il est jeté.

        Cette méthode ne fait quelque chose que si le personnage n'a
        aucune main libre.

        """
        personnage = self.personnage
        navire = self.navire
        cale = navire.cale
        if personnage.nb_mains_libres > 0:
            return

        conteneurs = (
                personnage.equipement.tenus,
                personnage.equipement.equipes,
        )

        for conteneur in conteneurs:
            for objet in list(conteneur):
                if personnage.nb_mains_libres > 0:
                    return

                if objet.nom_type != exception:
                    detruire = False
                    conteneur.retirer(objet)
                    if objet.nom_type in cale.types:
                        try:
                            cale.ajouter_objets([objet])
                        except ValueError:
                            detruire = True
                    else:
                        detruire = True

                    if detruire:
                        importeur.objet.supprimer_objet(objet.identifiant)

    def armer(self):
        """Arme le personnage si nécessaire.

        Le personnage essaye de récupérer une arme depuis la cale.

        """
        personnage = self.personnage
        self.jeter_ou_entreposer()

        # Si le personnage a déjà une arme, laisse courir
        if any(o.est_de_type("arme") for o in personnage.equipement.equipes):
            return
        cale = self.navire.cale
        armes = cale.armes
        if not armes:
            return

        armes = [importeur.objet.prototypes[cle] for cle in \
                armes.keys()]
        armes = [a for a in armes if a.cle_talent]
        armes.sort(key=lambda prototype: \
                personnage.talents.get(prototype.cle_talent, 0), reverse=True)
        arme = armes[0]
        objet = cale.recuperer(personnage, arme.cle)
        if objet:
            # On essaye de l'équiper
            for membre in personnage.equipement.membres:
                if membre.peut_equiper(objet):
                    objet.contenu.retirer(objet)
                    membre.equiper(objet)

            personnage.salle.envoyer("{{}} ramasse {}.".format(
                    objet.get_nom(1)), personnage)
