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


"""Fichier contenant la classe DiligenceMaudite, détaillée plus bas."""

from random import choice

from abstraits.obase import BaseObj

class DiligenceMaudite(BaseObj):

    """Classe représentant une diligence maudite.

    Une diligence maudite au niveau prototype est un modèle, définissant
    un ensemble de salles qui seront dupliquées par le système en
    ajoutant quelques aléatoires. Par exemple, une diligence maudite
    pourrait contenir vingt salles, en comptant des détails et scripts,
    peut-être certains PNJ. La configuration particulière de la
    diligence se fera dans un éditeur spécialisé. Quand le système
    devra créer une véritable diligence maudite, accessible aux
    joueurs, il créera une zone particulière en dupliquant les salles
    de la diligence et en intégrant les paramètres aléatoires configurés
    dans l'éditeur spécifique (comme la présence ou l'absence de
    PNJ aléatoires). La diligence maudite est ensuite rendue accessible
    grâce à une sortie menant dans l'univers accessible aux joueurs.

    """

    enregistrer = True

    def __init__(self, cle):
        """Constructeur de la fiche."""
        BaseObj.__init__(self)
        self.cle = cle
        self.ouverte = False
        self._construire()

    def __getnewargs__(self):
        return ("", )

    @property
    def salles(self):
        """Retourne toutes les salles modèle de la diligence."""
        zone = importeur.salle.zones.get(self.cle)
        if zone:
            return zone.salles

        return []

    def creer_premiere_salle(self):
        """Crée la première salle de la diligence."""
        return importeur.salle.creer_salle(self.cle, "1", valide=False)

    def apparaitre(self):
        """Fait apparaître la diligence dupliquée."""
        # Cherche la clé de la zone à créer
        nb = 1
        while (self.cle + "_" + str(nb)) in importeur.salle.zones:
            nb += 1

        cle = self.cle + "_" + str(nb)

        # Duplication des salles
        for salle in self.salles:
            n_salle = importeur.salle.creer_salle(cle, salle.mnemonic,
                        valide=False)
            n_salle.titre = salle.titre
            n_salle.description = salle.description
            n_salle.details = salle.details
            n_salle.interieur = salle.interieur
            n_salle.script = salle.script

        # On recopie les sorties
        for salle in self.salles:
            ident = "{}:{}".format(cle, salle.mnemonic)
            n_salle = importeur.salle.salles[ident]
            for dir, sortie in salle.sorties._sorties.items():
                if sortie and sortie.salle_dest:
                    n_ident = "{}:{}".format(cle, sortie.salle_dest.mnemonic)
                    c_salle = importeur.salle.salles[n_ident]
                    t_sortie = n_salle.sorties.ajouter_sortie(dir,
                            sortie.nom, sortie.article, c_salle,
                            sortie.correspondante)
                    if sortie.porte:
                        t_sortie.ajouter_porte()
                        t_sortie.porte._clef = sortie.porte._clef
                        t_sortie.porte.verrouillee = sortie.porte.verrouillee

        return cle


    @staticmethod
    def lier(origine, salle):
        """Lie l'origine de la diligence à la salle indiquée."""
        if origine.sorties.sortie_existe("bas"):
            raise ValueError("la sortie bas existe en {}".format(
                    origine.ident))

        if salle.sorties.sortie_existe("haut"):
            raise ValueError("la sortie haut existe en {}".format(
                    salle.ident))

        sortie = salle.sorties.ajouter_sortie("haut", "diligence", "la",
                origine, "bas")
        origine.sorties.ajouter_sortie("bas", "sortie", "la",
                salle, "haut")
        return sortie

    @staticmethod
    def deplacer(entree):
        """Déplace la diligence d'une salle, si possible."""
        origine = entree.sorties.get_sortie_par_nom_ou_direction(
                "bas").salle_dest
        terrain = origine.nom_terrain
        sorties = []
        for sortie in origine.sorties:
            if sortie and sortie.salle_dest and sortie.salle_dest.exterieur \
                    and sortie.salle_dest.nom_terrain == terrain and \
                    sortie.salle_dest is not entree and not \
                    sortie.salle_dest.sorties.sortie_existe("haut"):
                sorties.append(sortie)

        if not sorties:
            return

        sortie = choice(sorties)
        salle = sortie.salle_dest

        # Modification de la sortie
        entree.sorties.supprimer_sortie("bas")
        origine.sorties.supprimer_sortie("haut")
        salle.sorties.ajouter_sortie("haut", "diligence", "la",
                entree, "bas")
        entree.sorties.ajouter_sortie("bas", "sortie", "la",
                salle, "haut")
        origine.envoyer("Une diligence lourd lentement vers {}.".format(
                sortie.nom_complet))
        salle.envoyer("Une diligence arrive en roulant pesamment.")
        return salle
