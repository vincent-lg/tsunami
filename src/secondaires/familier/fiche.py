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


"""Fichier contenant la classe FicheFamilier, détaillée plus bas."""

from abstraits.obase import BaseObj

from secondaires.familier.script import ScriptFiche

class FicheFamilier(BaseObj):

    """Classe représentant une fiche de familier.

    Un familier est défini sur une fiche, tout comme les PNJ sont
    définis sur les prototypes ou comme les matelots sont définis
    sur des fiches de matelots. La fiche contient des informations
    générales sur le PNJ (chaque prototype de PNJ a une fiche).
    Par exemple, un cheval (prototype de PNJ 'cheval') peut avoir
    une fiche de familier ('cheval'). Dans cette fiche, il est déclaré
    que le cheval est un herbivore. Tous les chevau créés sur le
    prototype 'cheval' ('cheval_0', 'cheval_1', 'cheval_2', ...)
    pourront être des familiers qui utiliseront alors cette fiche.

    """

    enregistrer = True
    nom_scripting = "familier"
    type_achat = "familier"
    _nom = "fiche_familier"
    _version = 1

    def __init__(self, cle):
        """Constructeur de la fiche."""
        BaseObj.__init__(self)
        self.cle = cle
        self.regime = "herbivore"
        self.monture = False
        self.sorties_verticales = False
        self.aller_interieur = False
        self.stats_progres = [
                ["force", 10],
                ["agilite", 10],
                ["robustesse", 10],
                ["intelligence", 10],
        ]
        self.difficulte_apprivoisement = 10
        self.harnachements = []
        self.m_valeur = 50
        self.peut_manger = []
        self.aptitudes = {}
        self.script = ScriptFiche(self)
        self._construire()

    def __getnewargs__(self):
        return ("", )

    def __repr__(self):
        return "<FicheFamilier {}>".format(self.cle)

    def __str__(self):
        return self.cle

    @property
    def prototype(self):
        """Retourne le prototype de PNJ associé."""
        return importeur.pnj.prototypes.get(self.cle)

    @property
    def familiers(self):
        """Retourne la liste des familiers créés sur cette fiche.

        ATTENTION : cette méthode retourne les familiers, pas les
        PNJ. Un PNJ peut être créé sur le prototype de PNJ sans qu'il
        apparaisse dans cette liste.

        """
        familiers = list(importeur.familier.familiers.values())
        familiers = [f for f in familiers if f.cle == self.cle]
        return familiers

    @property
    def str_harnachements(self):
        return ", ".join(sorted(self.harnachements))

    @property
    def str_stats_progres(self):
        lignes = []
        stats = sorted(self.stats_progres, key=lambda c: c[1], reverse=True)
        total = sum(c[1] for c in self.stats_progres)
        for stat, probabilite in stats:
            pourcentage = round(probabilite / total * 100)
            lignes.append("   {} pour {} ({}%)".format(
                    stat, probabilite, pourcentage))

        return "\n".join(lignes)

    @property
    def nom_achat(self):
        return self.prototype and self.prototype.nom_singulier or "inconnu"

    @property
    def nom_singulier(self):
        return self.prototype and self.prototype.nom_singulier or "inconnu"

    @property
    def nom_pluriel(self):
        return self.prototype and self.prototype.nom_pluriel or "inconnus"

    def get_nom(self, nombre=1):
        """Retourne le nom complet en fonction du nombre."""
        if nombre == 0:
            raise ValueError("Nombre invalide")
        elif nombre == 1:
            return self.nom_singulier
        else:
            return str(nombre) + " " + self.nom_pluriel

    def acheter(self, quantite, magasin, transaction):
        """Achète les familiers dans la quantité spécifiée."""
        salle = magasin.parent
        acheteur = transaction.initiateur
        i = 0
        while i < quantite:
            i += 1
            pnj = importeur.pnj.creer_PNJ(self.prototype)
            pnj.salle = salle
            familier = importeur.familier.creer_familier(pnj)
            familier.maitre = acheteur
            familier.trouver_nom()
            salle.envoyer("{} arrive.", pnj)

    def regarder(self, personnage):
        """Le personnage regarde le familier avant achat."""
        desc = self.prototype.description.regarder(personnage,
                elt=self.prototype)
        return desc

    def detruire(self):
        """Destruction de la fiche de familier."""
        BaseObj.detruire(self)
        self.script.detruire()
