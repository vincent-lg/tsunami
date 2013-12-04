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


"""Fichier contenant la classe FicheMatelot, détaillée plus bas."""

from abstraits.obase import BaseObj
from primaires.format.description import Description
from secondaires.navigation.equipage.constantes import *

class FicheMatelot(BaseObj):

    """Fiche d'un matelot à créer.

    La fiche comprend des informations sur les aptitudes et postes
    spécifiques d'un matelot au niveau prototype. Une fiche pourrait, par
    exemple, dire que le prototype 'marin_ctn' a comme poste par défaut
    'charpentier' et la compétence 'calfeutrage' à 'bon' (ce qui se
    traduit, pour le PNJ créé depuis cette fiche, en l'obtension du
    talent 'calfeutrage' à quelque chose comme 30%).

    """

    enregistrer = True
    type_achat = "matelot"
    def __init__(self, prototype):
        """Constructeur du matelot."""
        BaseObj.__init__(self)
        self.prototype = prototype
        self.nom_singulier = "un matelot"
        self.nom_pluriel = "matelots"
        self.poste_defaut = "matelot"
        self.description = Description(parent=self)
        self.aptitudes = {}
        self.m_valeur = 20

    def __getnewargs__(self):
        return (None, )

    def __repr__(self):
        return "<FicheMâtelot {}>".format(repr(self.cle))

    def __str__(self):
        return self.cle

    @property
    def cle(self):
        return self.prototype and self.prototype.cle or "aucune"

    @property
    def nom_achat(self):
        return self.nom_singulier

    def get_nom(self, nombre=1):
        """Retourne le nom complet en fonction du nombre."""
        if nombre == 0:
            raise ValueError("Nombre invalide")
        elif nombre == 1:
            return self.nom_singulier
        else:
            return str(nombre) + " " + self.nom_pluriel

    def ajouter_aptitude(self, nom_aptitude, nom_niveau):
        """Ajoute une aptitude."""
        nom_aptitude = supprimer_accents(nom_aptitude).lower()
        nom_niveau = supprimer_accents(nom_niveau).lower()
        aptitude = CLES_APTITUDES.get(nom_aptitude)
        if aptitude is None:
            raise KeyError("Aptitude inconnue {}".format(repr(nom_aptitude)))

        niveau = VALEURS_NIVEAUX.get(nom_niveau)
        if niveau is None:
            raise KeyError("Niveau inconnu {}".format(repr(nom_niveau)))

        self.aptitudes[aptitude] = niveau

    def creer_PNJ(self, salle=None, nb=1):
        """Crée le PNJ sur la fiche."""
        pnjs = []
        if self.prototype is None:
            raise ValueError("Le prototype de cette fiche est inconnu")

        for i in range(nb):
            pnj = importeur.pnj.creer_PNJ(self.prototype, salle)
            pnjs.append(pnj)

            # Modifie les aptitudes
            for aptitude, niveau in self.aptitudes.items():
                talents = TALENTS.get(aptitude, [])
                connaissance = CONNAISSANCES[niveau]
                for talent in talents:
                    pnj.talents[talent] = connaissance

            # Annonce l'arrivée du PNJ
            if salle:
                salle.envoyer("{} arrive.", pnj)

        return pnjs

    def recruter(self, personnage, navire):
        """Recrute le matelot sur la fiche."""
        salle = navire.salles[0, 0, 0]
        personnage.salle = salle
        salle.envoyer("{} arrive.", personnage)
        navire.equipage.ajouter_matelot(personnage)

    def acheter(self, quantite, magasin, transaction):
        """Achète les matelots dans la quantité spécifiée."""
        salle = magasin.parent
        acheteur = transaction.initiateur
        nom = "trans_" + str(id(transaction))
        importeur.diffact.ajouter_action(nom, 10, self.creer_PNJ,
                salle, quantite)

    def regarder(self, personnage):
        """Le personnage regarde le service (avant achat)."""
        desc = self.description.regarder(personnage, elt=self.prototype)
        desc += "\n\nPoste (par défaut) : " + self.poste_defaut
        if self.aptitudes:
            desc += "\nAptitudes :\n"
            for aptitude, niveau in self.aptitudes.items():
                nom = NOMS_APTITUDES[aptitude]
                nom_niveau = NOMS_NIVEAUX[niveau]
                desc += "\n  {:<15} : {:>10} ({} / 6)".format(
                        nom.capitalize(), nom_niveau, niveau + 1)

        return desc
