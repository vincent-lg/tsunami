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


"""Fichier contenant la classe Auberge, détaillée plus bas."""

from abstraits.obase import BaseObj
from primaires.format.fonctions import supprimer_accents
from secondaires.auberge.chambre import Chambre

class Auberge(BaseObj):

    """Classe représentant une auberge.

    Une auberge a une clé, une salle (dans laquelle la location est
    possible), un aubergiste et une liste de chambres. Les chambres
    louées ont l'attribut 'proprietaire' et 'duree' renseignée.

    """

    enregistrer = True
    def __init__(self, cle):
        """Constructeur du navire."""
        BaseObj.__init__(self)
        self.cle = cle
        self.comptoir = None
        self.titre = "Une auberge"
        self.cle_aubergiste = ""
        self.chambres = {}

    def __getnewargs__(self):
        return ("", )

    def __repr__(self):
        return "<Auberge {}>".format(self.cle)

    def __str__(self):
        return self.cle

    @property
    def ident_comptoir(self):
        """Returne l'identifiant du comptoir si existe."""
        return self.comptoir and self.comptoir.ident or "aucune"

    @property
    def pct_occupation(self):
        """Retourne le pourcentage d'occupation de l'auberge.

        Une auberge avec toutes ses chambres réservée aura 100%
        d'occupation.

        """
        if len(self.chambres) == 0:
            return 0

        occupees = [c for c in self.chambres.values() if c.proprietaire]
        return int(len(occupees) / len(self.chambres) * 100)

    @property
    def aff_chambres(self):
        """Affiche un résumé des chambres."""
        if len(self.chambres) == 0:
            return "   Aucune"

        msg = ""
        chambres = sorted([c for c in self.chambres.values()],
                key=lambda c: c.numero)
        for chambre in chambres:
            msg += "\n   {:>8} ({:>15}) pour {:>5} pièces par jour".format(
                    chambre.numero, chambre.ident_salle, chambre.prix_par_jour)
            if chambre.proprietaire:
                msg += ", louée par " + chambre.nom_proprietaire

        return msg.lstrip("\n")

    @property
    def numero_chambres(self):
        """Retourne les numéros de chambres."""
        return tuple(c.numero for c in self.chambres.values())

    @property
    def aubergiste(self):
        """Retourne, si trouvé, l'aubergiste dans la salle.

        Si l'aubergiste n'est pas trouvé, retourne None.

        """
        if self.comptoir is None:
            return None

        for pnj in self.comptoir.PNJ:
            if pnj.cle == self.cle_aubergiste:
                return pnj

        return None

    @property
    def parent(self):
        """Utile pour la compatibilité avec les transactions."""
        return self.comptoir

    def get_chambre_avec_numero(self, numero):
        """Retourne la chambre avec le numéro spécifié.

        La recherche se fait sans tenir compte de la casse ni des
        accents. Si la chambre n'est pas trouvée, retourne None.

        """
        numero = supprimer_accents(numero.lower())
        for chambre in self.chambres.values():
            if supprimer_accents(chambre.numero.lower()) == numero:
                return chambre

        return None

    def verifier_chambres(self):
        """Vérifie que les chambres louées n'ont pas expirées."""
        for chambre in self.chambres.values():
            if chambre.expiree:
                chambre.proprietaire = None
                chambre.expire_a = None

    def ajouter_chambre(self, numero, salle):
        """Ajoute une nouvelle chambre."""
        numero = numero.lower()
        if salle.ident in self.chambres:
            raise ValueError("Cette salle est déjà une chambre".format(
                    repr(salle.ident)))

        if numero in [chambre.numero for chambre in self.chambres.values()]:
            raise ValueError("le numéro de chambre '{}' est déjà " \
                    "utilisé".format(numero))

        chambre = Chambre(self, numero, salle)
        self.chambres[salle.ident] = chambre
        return chambre

    def supprimer_chambre(self, ident):
        """Supprime une chambre."""
        chambre = self.chambres.pop(ident)
        chambre.detruire()

    def detruire(self):
        """Destruction de l'auberge, on détruit ses chambres."""
        for chambre in self.chambres.values():
            chambre.detruire()
        BaseObj.detruire(self)
